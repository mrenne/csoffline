// Site-wide constants and helpers.

export const SITE = {
  name: 'CS Offline',
  description: 'Teach and learn computer science, computational thinking, data science, AI literacy, cybersecurity, and ethics through unplugged activities, with little or no technology.',
  author: 'Mike Renne',
  authorUrl: 'https://www.linkedin.com/in/michaelrenne/',
  repo: 'https://github.com/mrenne/csoffline',
};

/** A path inside the site, with the GitHub Pages base path in front. Pass paths without the base. */
export function url(path = ''): string {
  const base = import.meta.env.BASE_URL.replace(/\/+$/, '');
  return `${base}/${path.replace(/^\/+/, '')}`;
}

export const ACTIVITY_TYPE: Record<string, string> = {
  'card-game': 'Card game', 'trading-card-game': 'Trading card game', 'board-game': 'Board game', 'pencil-and-paper-game': 'Pencil-and-paper game',
  'role-play': 'Role-play', puzzle: 'Puzzle', simulation: 'Simulation', discussion: 'Discussion', other: 'Activity',
};
export const AUDIENCE: Record<string, string> = {
  students: 'Students', educators: 'Educators', both: 'Students and educators',
};
export const GROUPING: Record<string, string> = {
  pairs: 'Pairs', 'small-groups': 'Small groups', 'whole-class': 'Whole class',
};
export const range = (r: { min: number; max: number }, unit = '') =>
  (r.min === r.max ? `${r.min}` : `${r.min}–${r.max}`) + (unit ? ` ${r.max === 1 && unit === 'people' ? 'person' : unit}` : '');
export const grades = (bands: string[]) => bands.map((b) => `Grades ${b.replace('-', '–')}`).join(', ');
