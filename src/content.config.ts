// The CS Worlds content model. See docs/system-spec.md, section 5.
// Front matter in every content file is checked against these schemas at build time.
// Cross-checks the schemas cannot express (exactly six topics, draft rules, printable
// files) live in src/lib/data.ts.
import { defineCollection, reference } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const gradeBand = z.enum(['6-8', '9-12']);
const status = z.enum(['draft', 'published']);
const range = z.object({ min: z.number().int().min(1), max: z.number().int().min(1) })
  .refine((r) => r.max >= r.min, { message: 'max must be at least min' });

// Folder-based entries (worlds/<slug>/index.md, games/<slug>/index.md) take the folder name as id.
const folderId = ({ entry }: { entry: string }) => entry.split('/')[0];

const topics = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/topics' }),
  schema: z.object({
    name: z.string(),
    summary: z.string(),
    color: z.enum(['orange', 'navy', 'sky', 'mint', 'lilac', 'rose']),
    icon: z.enum(['chip', 'puzzle', 'chart', 'spark', 'shield', 'scale']),
    order: z.number(),
  }),
});

const concepts = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/concepts' }),
  schema: z.object({
    name: z.string(),
    topics: z.array(reference('topics')).min(1),
    student_summary: z.string(),
    related: z.array(reference('concepts')).default([]),
    standards: z.array(z.string()).default([]),
  }),
});

const worlds = defineCollection({
  loader: glob({ pattern: '*/index.md', base: './src/content/worlds', generateId: folderId }),
  schema: ({ image }) => z.object({
    name: z.string(),
    tagline: z.string(),
    // Optional until the visual identity is decided (spec, open decision 4).
    art: image().optional(),
    art_alt: z.string().optional(),
    map_position: z.object({ x: z.number(), y: z.number() }).optional(),
    order: z.number(),
    status,
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
  concepts: z.array(reference('concepts')).default([]),
  grade_bands: z.array(gradeBand).optional(),
});

const games = defineCollection({
  loader: glob({ pattern: '*/index.md', base: './src/content/games', generateId: folderId }),
  schema: z.object({
    name: z.string(),
    world: reference('worlds'),
    summary: z.string(),
    concepts: z.array(reference('concepts')).min(1),
    game_type: z.enum(['card', 'board', 'role-play', 'puzzle', 'other']),
    players: range,
    grouping: z.array(z.enum(['pairs', 'small-groups', 'whole-class'])).min(1),
    minutes: range,
    prep_minutes: z.number().int().min(0),
    grade_bands: z.array(gradeBand).min(1),
    materials: z.array(z.string()).default([]),
    printables: z.array(printable).default([]),
    variants: z.array(variant).default([]),
    standards: z.array(z.string()).default([]),
    status,
    credits: z.string().optional(),
    license: z.string().default('CC BY-NC-SA 4.0'),
  }),
});

// The educator guide for a game: games/<slug>/guide.md. Body only.
const guides = defineCollection({
  loader: glob({ pattern: '*/guide.md', base: './src/content/games', generateId: folderId }),
  schema: z.object({}),
});

const pathways = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/pathways' }),
  schema: z.object({
    name: z.string(),
    summary: z.string(),
    grade_bands: z.array(gradeBand).min(1),
    steps: z.array(z.object({ game: reference('games'), variant: z.string().optional(), note: z.string().optional() })).min(1),
    status,
  }),
});

export const collections = { topics, concepts, worlds, games, guides, pathways };
