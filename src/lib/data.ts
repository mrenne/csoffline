// Loads every collection once, checks the rules the schemas cannot express, and derives the
// reverse links (a concept's games, a game's domains). Every page reads content through `site()`.
// A failed check throws, which fails the build (spec, section 5.9).
import { getCollection, type CollectionEntry } from 'astro:content';

export type Domain = CollectionEntry<'domains'>;
export type Concept = CollectionEntry<'concepts'>;
export type Game = CollectionEntry<'games'>;
export type Guide = CollectionEntry<'guides'>;

export const DOMAIN_COUNT = 6;

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
  const domains = (await getCollection('domains')).sort((a, b) => a.data.order - b.data.order);
  const concepts = (await getCollection('concepts')).sort((a, b) => a.data.name.localeCompare(b.data.name));
  const allGames = (await getCollection('games')).sort((a, b) => a.data.name.localeCompare(b.data.name));
  const guides = await getCollection('guides');

  const errors: string[] = [];
  const warnings: string[] = [];
  const ids = (list: { id: string }[]) => new Set(list.map((e) => e.id));
  const domainIds = ids(domains), conceptIds = ids(concepts);

  if (domains.length !== DOMAIN_COUNT) errors.push(`expected ${DOMAIN_COUNT} domains, found ${domains.length}`);
  for (const c of concepts) {
    for (const d of c.data.domains) if (!domainIds.has(d.id)) errors.push(`concept ${c.id}: unknown domain "${d.id}"`);
    for (const r of c.data.related) if (!conceptIds.has(r.id)) errors.push(`concept ${c.id}: unknown related concept "${r.id}"`);
  }
  for (const g of allGames) {
    if (!domainIds.has(g.data.domain.id)) errors.push(`game ${g.id}: unknown domain "${g.data.domain.id}"`);
    for (const c of [...g.data.concepts, ...g.data.variants.flatMap((v) => v.concepts)]) {
      if (!conceptIds.has(c.id)) errors.push(`game ${g.id}: unknown concept "${c.id}"`);
    }
    for (const p of g.data.printables) {
      if (!printableUrl(g, p.file)) errors.push(`game ${g.id}: printable file not found: ${p.file}`);
    }
    if (g.data.status === 'published') {
      if (!g.data.printables.length) warnings.push(`game ${g.id} has no printables yet`);
      if (!guides.some((x) => x.id === g.id)) warnings.push(`game ${g.id} has no guide.md`);
    }
  }
  if (errors.length) throw new Error('CS Offline content check failed:\n  - ' + errors.join('\n  - '));

  const games = allGames.filter((g) => g.data.status === 'published');
  const domainOf = new Map(domains.map((d) => [d.id, d]));
  const conceptOf = new Map(concepts.map((c) => [c.id, c]));

  // A game's home domain first, then any other domain its concepts belong to.
  const gameDomains = (g: Game) => {
    const set = new Set([g.data.domain.id, ...g.data.concepts.flatMap((c) => conceptOf.get(c.id)!.data.domains.map((d) => d.id))]);
    return [domainOf.get(g.data.domain.id)!, ...domains.filter((d) => d.id !== g.data.domain.id && set.has(d.id))];
  };
  const gameConcepts = (g: Game) => g.data.concepts.map((c) => conceptOf.get(c.id)!);
  const gamesFor = (concept: Concept) => games.filter((g) => g.data.concepts.some((c) => c.id === concept.id));
  const conceptDomains = (c: Concept) => c.data.domains.map((d) => domainOf.get(d.id)!);
  const conceptsFor = (domain: Domain) => concepts.filter((c) => c.data.domains.some((d) => d.id === domain.id));
  // Games whose home is this domain, and games from other domains that also teach it.
  const gamesIn = (domain: Domain) => games.filter((g) => g.data.domain.id === domain.id);
  const gamesAlso = (domain: Domain) => games.filter((g) => g.data.domain.id !== domain.id && gameDomains(g).some((d) => d.id === domain.id));
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

  if (warnings.length && !globalThis.__csofflineWarned) {
    globalThis.__csofflineWarned = true;
    console.warn('CS Offline content warnings:\n  - ' + warnings.join('\n  - '));
  }

  return {
    domains, concepts, games, guides,
    domain: (id: string) => domainOf.get(id)!,
    concept: (id: string) => conceptOf.get(id)!,
    guide: (id: string) => guides.find((x) => x.id === id),
    gameDomains, gameConcepts, gamesFor, conceptDomains, conceptsFor, gamesIn, gamesAlso, pairsWith,
  };
}

declare global {
  // eslint-disable-next-line no-var
  var __csofflineWarned: boolean | undefined;
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
