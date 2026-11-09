// The CS Offline content model. See docs/system-spec.md, section 5.
// Front matter in every content file is checked against these schemas at build time.
// Cross-checks the schemas cannot express (exactly six domains, draft rules, printable
// files) live in src/lib/data.ts.
import { defineCollection, reference } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const gradeBand = z.enum(['6-8', '9-12']);
const status = z.enum(['draft', 'published']);
const range = z.object({ min: z.number().int().min(1), max: z.number().int().min(1) })
  .refine((r) => r.max >= r.min, { message: 'max must be at least min' });

// Folder-based entries (activities/<slug>/index.md, activities/<slug>/guide.md) take the folder name as id.
const folderId = ({ entry }: { entry: string }) => entry.split('/')[0];

// The six learning domains. Every activity has one home domain.
const domains = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/domains' }),
  schema: z.object({
    name: z.string(),
    summary: z.string(),
    color: z.enum(['orange', 'navy', 'sky', 'mint', 'lilac', 'rose']),
    icon: z.enum(['chip', 'puzzle', 'chart', 'spark', 'shield', 'scale']),
    order: z.number(),
  }),
});

const ideas = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/ideas' }),
  schema: z.object({
    name: z.string(),
    domains: z.array(reference('domains')).min(1),
    student_summary: z.string(),
    related: z.array(reference('ideas')).default([]),
    standards: z.array(z.string()).default([]),
  }),
});

const printable = z.object({
  title: z.string(),
  file: z.string(),
  paper: z.enum(['letter', 'a4', 'both']),
  color: z.enum(['color', 'bw', 'both']),
  copies: z.string(),
  source: z.string().optional(),
});

const variant = z.object({
  name: z.string(),
  summary: z.string(),
  ideas: z.array(reference('ideas')).default([]),
  grade_bands: z.array(gradeBand).optional(),
});

const activities = defineCollection({
  loader: glob({ pattern: '*/index.md', base: './src/content/activities', generateId: folderId }),
  schema: z.object({
    name: z.string(),
    domain: reference('domains'),
    summary: z.string(),
    ideas: z.array(reference('ideas')).min(1),
    // Some activities are games (card-game, trading-card-game, board-game); others are not.
    activity_type: z.enum(['card-game', 'trading-card-game', 'board-game', 'role-play', 'puzzle', 'simulation', 'discussion', 'other']),
    audience: z.enum(['students', 'educators', 'both']),
    // Where to get it, for an activity hosted or sold elsewhere.
    link: z.object({ label: z.string(), url: z.url() }).optional(),
    group_size: range.optional(),
    grouping: z.array(z.enum(['pairs', 'small-groups', 'whole-class'])).min(1).optional(),
    minutes: range.optional(),
    prep_minutes: z.number().int().min(0).optional(),
    grade_bands: z.array(gradeBand).min(1).optional(),
    materials: z.array(z.string()).default([]),
    printables: z.array(printable).default([]),
    variants: z.array(variant).default([]),
    standards: z.array(z.string()).default([]),
    status,
    author: z.object({
      name: z.string(),
      role: z.string().default('author'),
      bio: z.string().optional(),
      link: z.object({ label: z.string(), url: z.url() }).optional(),
    }),
    credits: z.string().optional(),
    notice: z.string().optional(),
    // Set only when the author chooses a license; nothing is assumed.
    license: z.string().optional(),
    license_url: z.url().optional(),
  }).refine((a) => a.link || (a.group_size && a.grouping && a.minutes && a.prep_minutes !== undefined && a.grade_bands), {
    message: 'group_size, grouping, minutes, prep_minutes, and grade_bands are required unless the activity has a link',
  }),
});

// The educator guide for an activity: activities/<slug>/guide.md. Body only.
const guides = defineCollection({
  loader: glob({ pattern: '*/guide.md', base: './src/content/activities', generateId: folderId }),
  schema: z.object({}),
});

const pathways = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/pathways' }),
  schema: z.object({
    name: z.string(),
    summary: z.string(),
    grade_bands: z.array(gradeBand).min(1),
    steps: z.array(z.object({ activity: reference('activities'), variant: z.string().optional(), note: z.string().optional() })).min(1),
    status,
  }),
});

export const collections = { domains, ideas, activities, guides, pathways };
