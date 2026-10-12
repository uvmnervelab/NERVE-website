// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';
import react from '@astrojs/react';

// https://astro.build/config
export default defineConfig({
  site: 'https://nervelab.w3.uvm.edu',
	base: process.env.BASE_PATH || '/',
  compressHTML: true,
  build: {
    inlineStylesheets: 'always',
  },
  vite: {
    // @ts-expect-error -- @tailwindcss/vite is typed against Vite 7; Astro 5 uses Vite 6. Works at runtime.
    plugins: [tailwindcss()],
    build: {
      assetsInlineLimit: 10240, // 10KB to inline achievements.css (7.5KB)
    }
  },

  integrations: [react()]
});
