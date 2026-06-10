import { resolve } from 'node:path';
import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  resolve: { alias: { $lib: resolve('src/lib') } },
  plugins: [svelte()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
});
