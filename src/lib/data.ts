// Loads every collection once, checks the rules the schemas cannot express, and derives the
// reverse links (a concept's games, a game's topics). Every page reads content through `site()`.
// A failed check throws, which fails the build (spec, section 5.10).
import { getCollection, type CollectionEntry } from 'astro:content';

export type Topic = CollectionEntry<'topics'>;
export type Concept = CollectionEntry<'concepts'>;
export type World = CollectionEntry<'worlds'>;
export type Game = CollectionEntry<'games'>;
export type Guide = CollectionEntry<'guides'>;

export const TOPIC_COUNT = 6;

// Printable files sit next to their game: src/content/games/<slug>/printables/<file>.
const printableFiles = import.meta.glob('/src/content/games/*/printables/*', {
  query: '?url', import: 'default', eager: true,
}) as Record<string, string>;

export function printableUrl(game: Game, file: string): string | undefined {
  return printableFiles[`/src/content/games/${game.id}/${file.replace(/^\.?\//, '')}`];
}

type Site = Awaited<ReturnType<typeof load>>;
let cached: Promise<Site> | undefined;

export function site(): Promise<Site> {
  cached ??= load();
  return cached;
}

async function load() {
  const byOrder = (a: { data: { order: number } }, b: { data: { order: number } }) => a.data.order - b.data.order;
  const topics = (await getCollection('topics')).sort(byOrder);
  const concepts = (await getCollection('concepts')).sort((a, b) => a.data.name.localeCompare(b.data.name));
  const allWorlds = (await getCollection('worlds')).sort(byOrder);
  const allGames = (await getCollection('games')).sort((a, b) => a.data.name.localeCompare(b.data.name));
  const guides = await getCollection('guides');

  const errors: string[] = [];
  const warnings: string[] = [];
  const ids = (list: { id: string }[]) => new Set(list.map((e) => e.id));
  const topicIds = ids(topics), conceptIds = ids(concepts), worldIds = ids(allWorlds);

  if (topics.length !== TOPIC_COUNT) errors.push(`expected ${TOPIC_COUNT} topics, found ${topics.length}`);
  for (const c of concepts) {
    for (const t of c.data.topics) if (!topicIds.has(t.id)) errors.push(`concept ${c.id}: unknown topic "${t.id}"`);
    for (const r of c.data.related) if (!conceptIds.has(r.id)) errors.push(`concept ${c.id}: unknown related concept "${r.id}"`);
  }
  const worldStatus = new Map(allWorlds.map((w) => [w.id, w.data.status]));
  for (const g of allGames) {
    if (!worldIds.has(g.data.world.id)) errors.push(`game ${g.id}: unknown world "${g.data.world.id}"`);
    for (const c of [...g.data.concepts, ...g.data.variants.flatMap((v) => v.concepts)]) {
      if (!conceptIds.has(c.id)) errors.push(`game ${g.id}: unknown concept "${c.id}"`);
    }
    for (const p of g.data.printables) {
      if (!printableUrl(g, p.file)) errors.push(`game ${g.id}: printable file not found: ${p.file}`);
    }
    if (g.data.status === 'published') {
      if (worldStatus.get(g.data.world.id) === 'draft') errors.push(`game ${g.id} is published but its world is a draft`);
      if (!g.data.printables.length) warnings.push(`game ${g.id} has no printables yet`);
      if (!guides.some((x) => x.id === g.id)) warnings.push(`game ${g.id} has no guide.md`);
    }
  }
  if (errors.length) throw new Error('CS Worlds content check failed:\n  - ' + errors.join('\n  - '));

  const worlds = allWorlds.filter((w) => w.data.status === 'published');
  const games = allGames.filter((g) => g.data.status === 'published');

  const topicOf = new Map(topics.map((t) => [t.id, t]));
  const conceptOf = new Map(concepts.map((c) => [c.id, c]));
  const worldOf = new Map(allWorlds.map((w) => [w.id, w]));

  const gameTopics = (g: Game) => {
    const set = new Set(g.data.concepts.flatMap((c) => conceptOf.get(c.id)!.data.topics.map((t) => t.id)));
    return topics.filter((t) => set.has(t.id));
  };
  const gameConcepts = (g: Game) => g.data.concepts.map((c) => conceptOf.get(c.id)!);
  const gamesFor = (concept: Concept) => games.filter((g) => g.data.concepts.some((c) => c.id === concept.id));
  const conceptTopics = (c: Concept) => c.data.topics.map((t) => topicOf.get(t.id)!);
  const conceptsFor = (topic: Topic) => concepts.filter((c) => c.data.topics.some((t) => t.id === topic.id));
  const gamesInWorld = (w: World) => games.filter((g) => g.data.world.id === w.id);
  const worldConcepts = (w: World) => {
    const set = new Set(gamesInWorld(w).flatMap((g) => g.data.concepts.map((c) => c.id)));
    return concepts.filter((c) => set.has(c.id));
  };
  // Other games that share at least one concept, most shared first.
  const pairsWith = (g: Game) => {
    const mine = new Set(g.data.concepts.map((c) => c.id));
    return games
      .filter((o) => o.id !== g.id)
      .map((o) => ({ game: o, shared: o.data.concepts.filter((c) => mine.has(c.id)).length }))
      .filter((x) => x.shared > 0)
      .sort((a, b) => b.shared - a.shared)
      .map((x) => x.game);
  };

  if (warnings.length && !globalThis.__csworldsWarned) {
    globalThis.__csworldsWarned = true;
    console.warn('CS Worlds content warnings:\n  - ' + warnings.join('\n  - '));
  }

  return {
    topics, concepts, worlds, games, guides,
    topic: (id: string) => topicOf.get(id)!,
    concept: (id: string) => conceptOf.get(id)!,
    world: (id: string) => worldOf.get(id)!,
    guide: (id: string) => guides.find((x) => x.id === id),
    gameTopics, gameConcepts, gamesFor, conceptTopics, conceptsFor, gamesInWorld, worldConcepts, pairsWith,
  };
}

declare global {
  // eslint-disable-next-line no-var
  var __csworldsWarned: boolean | undefined;
}

// Split rendered Markdown into sections by its <h2> headings, keyed by heading id.
export function sections(html: string): Record<string, { title: string; html: string }> {
  const out: Record<string, { title: string; html: string }> = {};
  const parts = html.split(/(?=<h2[\s>])/);
  for (const part of parts) {
    const m = part.match(/^<h2[^>]*id="([^"]+)"[^>]*>(.*?)<\/h2>/s);
    if (m) out[m[1]] = { title: m[2].replace(/<[^>]+>/g, ''), html: part.slice(m[0].length) };
    else if (part.trim()) out['_intro'] = { title: '', html: part };
  }
  return out;
}
