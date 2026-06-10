# V8m (freedoom-web)

Freedoom Phase 1 running in the browser, packaged as a Vite project for Verse8.

## Play

```bash
npm install
npm run dev
# → http://localhost:3011
```

Desktop: keyboard + mouse (F1 in-game for controls). Touch devices get an on-screen control overlay automatically.

## Features

- **Tap to start** — complies with mobile autoplay policies and ad-gesture rules.
- **Rewarded-ad revive (Verse8)** — when the player dies, an overlay offers an
  in-place revive via `Verse8Ads.showRewarded({ placementId: "revive-hero" })`.
  The engine is patched to notify the page on death and expose a revive export
  (see `engine-patches/`). Outside Verse8 (`unsupported_env`) the game falls
  back to the vanilla death flow. Append `?simulateads` to the URL to test the
  flow without the ad platform.
- Touch controls on mobile, gamepad support, local saves.

## What's inside

| File | What it is | License |
|---|---|---|
| `public/index.js` / `index.wasm` / `index.data` | [Dwasm](https://github.com/GMH-Code/Dwasm) (PrBoom+/PrBoomX WebAssembly port by Gregory Maynard-Hoare) built with the patch in `engine-patches/` | GPL-2.0 |
| `public/oly.js` | Dwasm touchscreen control overlay | GPL-2.0 |
| `public/freedoom1.wad` | [Freedoom](https://freedoom.github.io/) Phase 1 v0.13.0 game data | BSD (see `public/FREEDOOM-COPYING.txt`) |
| `index.html` | Loader: tap-to-start, IWAD fetch → MemFS, Verse8 ads revive UI | GPL-2.0 |
| `engine-patches/` | Source patch + rebuild instructions for the engine binaries (GPL source disclosure) | GPL-2.0 |

## Licensing & attribution

- The game engine is **Dwasm** (<https://github.com/GMH-Code/Dwasm>), a WebAssembly port of PrBoom+ (<https://github.com/coelckers/prboom-plus>) and PrBoomX, distributed under the **GNU GPL v2**. Complete corresponding source code is available at the linked repositories.
- Game assets are **Freedoom Phase 1** (<https://freedoom.github.io/>), distributed under a **BSD-style license** (`public/FREEDOOM-COPYING.txt`, credits in `public/FREEDOOM-CREDITS.txt`).
- This project contains **no proprietary DOOM data or trademarks**. It is not affiliated with, endorsed by, or in any way connected to id Software, Bethesda Softworks, or ZeniMax Media.
