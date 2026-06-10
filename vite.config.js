import { defineConfig } from 'vite'

export default defineConfig({
  publicDir: 'public',
  server: {
    port: 3013,
    headers: {
      'Cross-Origin-Embedder-Policy': 'require-corp',
      'Cross-Origin-Opener-Policy': 'same-origin',
    },
  },
  preview: {
    port: 3013,
    headers: {
      'Cross-Origin-Embedder-Policy': 'require-corp',
      'Cross-Origin-Opener-Policy': 'same-origin',
    },
  },
  build: {
    outDir: 'dist',
    chunkSizeWarningLimit: 5000,
  },
  assetsInclude: ['**/*.wasm', '**/*.wad', '**/*.data'],
})
