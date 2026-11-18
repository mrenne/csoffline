// @ts-check
import { defineConfig } from 'astro/config';

// GitHub Pages serves the site at the custom domain https://www.csoffline.org/ (set in the repo's
// Settings > Pages). Without a custom domain, use site 'https://mrenne.github.io' and base '/csoffline'.
export default defineConfig({
  site: 'https://www.csoffline.org',
  base: '/',
  trailingSlash: 'always',
  build: { format: 'directory' },
});
