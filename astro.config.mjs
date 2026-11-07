// @ts-check
import { defineConfig } from 'astro/config';

// GitHub Pages serves the site at https://mrenne.github.io/csoffline/.
// With a custom domain, set `site` to it and `base` to '/'.
export default defineConfig({
  site: 'https://mrenne.github.io',
  base: '/csoffline',
  trailingSlash: 'always',
  build: { format: 'directory' },
});
