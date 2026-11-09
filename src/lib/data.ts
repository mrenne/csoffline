// Loads every collection once, checks the rules the schemas cannot express, and derives the
// reverse links (an idea's activities, an activity's domains). Every page reads content through `site()`.
// A failed check throws, which fails the build (spec, section 5.9).
import { getCollection, type CollectionEntry } from 'astro:content';

export type Domain = CollectionEntry<'domains'>;
export type Idea = CollectionEntry<'ideas'>;
export type Activity = CollectionEntry<'activities'>;
export type Guide = CollectionEntry<'guides'>;

export const DOMAIN_COUNT = 6;

// Printable files sit next to their activity: src/content/activities/<slug>/printables/<file>.
const printableFiles = import.meta.glob('/src/content/activities/*/printables/*', {
  query: '?url', import: 'default', eager: true,
}) as Record<string, string>;

export function printableUrl(activity: Activity, file: string): string | undefined {
  return printableFiles[`/src/content/activities/${activity.id}/${file.replace(/^\.?\//, '')}`];
}

type Site = Awaited<ReturnType<typeof load>>;
let cached: Promise<Site> | undefined;

export function site(): Promise<Site> {
  cached ??= load();
  return cached;
}

async function load() {
  const domains = (await getCollection('domains')).sort((a, b) => a.data.order - b.data.order);
  const ideas = (await getCollection('ideas')).sort((a, b) => a.data.name.localeCompare(b.data.name));
  const allActivities = (await getCollection('activities')).sort((a, b) => a.data.name.localeCompare(b.data.name));
  const guides = await getCollection('guides');

  const errors: string[] = [];
  const warnings: string[] = [];
  const ids = (list: { id: string }[]) => new Set(list.map((e) => e.id));
  const domainIds = ids(domains), ideaIds = ids(ideas);

  if (domains.length !== DOMAIN_COUNT) errors.push(`expected ${DOMAIN_COUNT} domains, found ${domains.length}`);
  for (const c of ideas) {
    for (const d of c.data.domains) if (!domainIds.has(d.id)) errors.push(`idea ${c.id}: unknown domain "${d.id}"`);
    for (const r of c.data.related) if (!ideaIds.has(r.id)) errors.push(`idea ${c.id}: unknown related idea "${r.id}"`);
  }
  for (const g of allActivities) {
    if (!domainIds.has(g.data.domain.id)) errors.push(`activity ${g.id}: unknown domain "${g.data.domain.id}"`);
    for (const c of [...g.data.ideas, ...g.data.variants.flatMap((v) => v.ideas)]) {
      if (!ideaIds.has(c.id)) errors.push(`activity ${g.id}: unknown idea "${c.id}"`);
    }
    for (const p of g.data.printables) {
      if (!printableUrl(g, p.file)) errors.push(`activity ${g.id}: printable file not found: ${p.file}`);
    }
    if (g.data.status === 'published') {
      if (!g.data.link && !g.data.printables.length) warnings.push(`activity ${g.id} has no printables yet`);
      if (!g.data.link && !guides.some((x) => x.id === g.id)) warnings.push(`activity ${g.id} has no guide.md`);
    }
  }
  if (errors.length) throw new Error('CS Offline content check failed:\n  - ' + errors.join('\n  - '));

  const activities = allActivities.filter((g) => g.data.status === 'published');
  // Student pages exist unless an activity is for educators only, and educator pages unless it is for students only.
  const studentActivities = activities.filter((a) => a.data.audience !== 'educators');
  const educatorActivities = activities.filter((a) => a.data.audience !== 'students');
  const domainOf = new Map(domains.map((d) => [d.id, d]));
  const ideaOf = new Map(ideas.map((c) => [c.id, c]));

  // An activity's home domain first, then any other domain its ideas belong to.
  const activityDomains = (g: Activity) => {
    const set = new Set([g.data.domain.id, ...g.data.ideas.flatMap((c) => ideaOf.get(c.id)!.data.domains.map((d) => d.id))]);
    return [domainOf.get(g.data.domain.id)!, ...domains.filter((d) => d.id !== g.data.domain.id && set.has(d.id))];
  };
  const activityIdeas = (g: Activity) => g.data.ideas.map((c) => ideaOf.get(c.id)!);
  const activitiesFor = (idea: Idea) => activities.filter((g) => g.data.ideas.some((c) => c.id === idea.id));
  const ideaDomains = (c: Idea) => c.data.domains.map((d) => domainOf.get(d.id)!);
  const ideasFor = (domain: Domain) => ideas.filter((c) => c.data.domains.some((d) => d.id === domain.id));
  // Activities whose home is this domain, and activities from other domains that also teach it.
  const activitiesIn = (domain: Domain) => activities.filter((g) => g.data.domain.id === domain.id);
  const activitiesAlso = (domain: Domain) => activities.filter((g) => g.data.domain.id !== domain.id && activityDomains(g).some((d) => d.id === domain.id));
  // Other activities that share at least one idea, most shared first.
  const pairsWith = (g: Activity) => {
    const mine = new Set(g.data.ideas.map((c) => c.id));
    return activities
      .filter((o) => o.id !== g.id)
      .map((o) => ({ activity: o, shared: o.data.ideas.filter((c) => mine.has(c.id)).length }))
      .filter((x) => x.shared > 0)
      .sort((a, b) => b.shared - a.shared)
      .map((x) => x.activity);
  };

  if (warnings.length && !globalThis.__csofflineWarned) {
    globalThis.__csofflineWarned = true;
    console.warn('CS Offline content warnings:\n  - ' + warnings.join('\n  - '));
  }

  return {
    domains, ideas, activities, guides,
    domain: (id: string) => domainOf.get(id)!,
    idea: (id: string) => ideaOf.get(id)!,
    guide: (id: string) => guides.find((x) => x.id === id),
    studentActivities, educatorActivities,
    activityDomains, activityIdeas, activitiesFor, ideaDomains, ideasFor, activitiesIn, activitiesAlso, pairsWith,
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
