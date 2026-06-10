import { defineConfig } from 'vite'

// NOTE: no COOP/COEP headers — the engine build doesn't use SharedArrayBuffer,
// and cross-origin isolation would break the Verse8 ads SDK overlay/iframe.
export default defineConfig({
  publicDir: 'public',
  server: {
    port: 3013,
  },
  preview: {
    port: 3013,
  },
  build: {
    outDir: 'dist',
    chunkSizeWarningLimit: 5000,
  },
  assetsInclude: ['**/*.wasm', '**/*.wad', '**/*.data'],
})
