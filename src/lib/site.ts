// Site-wide constants and helpers.

export const SITE = {
  name: 'CS Worlds',
  description: 'Explore computer science, computational thinking, data science, AI literacy, cybersecurity, and ethics through unplugged games.',
  author: 'Mike Renne',
  repo: 'https://github.com/mrenne/csworlds',
  license: { name: 'CC BY-NC-SA 4.0', url: 'https://creativecommons.org/licenses/by-nc-sa/4.0/' },
};

/** A path inside the site, with the GitHub Pages base path in front. Pass paths without the base. */
export function url(path = ''): string {
  const base = import.meta.env.BASE_URL.replace(/\/+$/, '');
  return `${base}/${path.replace(/^\/+/, '')}`;
}

export const GAME_TYPE: Record<string, string> = {
  card: 'Card game', board: 'Board game', 'role-play': 'Role-play', puzzle: 'Puzzle', other: 'Game',
};
export const GROUPING: Record<string, string> = {
  pairs: 'Pairs', 'small-groups': 'Small groups', 'whole-class': 'Whole class',
};
export const range = (r: { min: number; max: number }, unit = '') =>
  (r.min === r.max ? `${r.min}` : `${r.min}–${r.max}`) + (unit ? ` ${unit}` : '');
export const grades = (bands: string[]) => bands.map((b) => `Grades ${b.replace('-', '–')}`).join(', ');
