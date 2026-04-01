import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [tailwindcss()],

  server: {
    host: '0.0.0.0',
    strictPort: true,
    port: 5173,
  },

  css: {
    devSourcemap: false,
  },

  build: {
    outDir: 'dist',
    emptyOutDir: true,
    cssCodeSplit: false,
    sourcemap: false,
    manifest: true,
    rollupOptions: {
      input: 'src/main.js',
      output: {
        entryFileNames: 'js/main.js',
        assetFileNames: (asset) => {
          if (asset.name && asset.name.endsWith('.css')) return 'css/style.css'
          return 'assets/[name].[hash][extname]'
        },
      },
    },
  },
})