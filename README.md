# Freedoom Web

Freedoom Phase 1 running in the browser, packaged as a Vite project.

## Play

```bash
npm install
npm run dev
# → http://localhost:3011
```

Desktop: keyboard + mouse (F1 in-game for controls). Touch devices get an on-screen control overlay automatically.

## What's inside

| File | What it is | License |
|---|---|---|
| `public/index.js` / `index.wasm` / `index.data` / `oly.js` | [Dwasm](https://github.com/GMH-Code/Dwasm) — WebAssembly port of PrBoom+/PrBoomX by Gregory Maynard-Hoare | GPL-2.0 |
| `public/freedoom1.wad` | [Freedoom](https://freedoom.github.io/) Phase 1 v0.13.0 game data | BSD (see `public/FREEDOOM-COPYING.txt`) |
| `index.html` | Custom auto-start loader (fetches the IWAD, boots the engine) | GPL-2.0 |

## Licensing & attribution

- The game engine is **Dwasm** (<https://github.com/GMH-Code/Dwasm>), a WebAssembly port of PrBoom+ (<https://github.com/coelckers/prboom-plus>) and PrBoomX, distributed under the **GNU GPL v2**. Complete corresponding source code is available at the linked repositories.
- Game assets are **Freedoom Phase 1** (<https://freedoom.github.io/>), distributed under a **BSD-style license** (`public/FREEDOOM-COPYING.txt`, credits in `public/FREEDOOM-CREDITS.txt`).
- This project contains **no proprietary DOOM data or trademarks**. It is not affiliated with, endorsed by, or in any way connected to id Software, Bethesda Softworks, or ZeniMax Media.
