# Freedoom Web — 구조 분석 노트

## 개요
- **게임**: Freedoom Phase 1 (v0.13.0) — DOOM 호환 100% 무료 IWAD
- **엔진**: Dwasm (PrBoom+/PrBoomX의 Emscripten WebAssembly 포트)
- **라이선스**: 엔진 GPL-2.0 / 에셋 BSD → **재배포·상업화(광고) 합법**, 소스 공개 의무만 준수
- Poki 게임들과 달리 다운로더 불필요 — 모든 파일이 합법적으로 재배포 가능

## 파일 구조 (Vite)
```
freedoom-web/
├── index.html          ← 커스텀 자동시작 로더 (직접 작성, 핵심 파일)
├── vite.config.js      ← 포트 3011, COOP/COEP 헤더
├── package.json
├── public/
│   ├── index.js        ← Emscripten 엔진 로더 (Dwasm 빌드)
│   ├── index.wasm      ← PrBoom+ 엔진 본체 (~2.5MB)
│   ├── index.data      ← Emscripten 패키지 데이터 (prboomx.wad 등, ~470KB)
│   ├── oly.js          ← 터치스크린 온스크린 컨트롤 오버레이
│   ├── freedoom1.wad   ← 게임 에셋 IWAD (~28MB)
│   ├── FREEDOOM-COPYING.txt / FREEDOOM-CREDITS.txt
└── NOTES.md
```

## 부팅 아키텍처 (index.html)
1. `fetch('freedoom1.wad')` — 스트리밍 다운로드 + 진행률 표시
2. `userFileDict['freedoom1.wad'] = ['i', Uint8Array]` 형태로 보관
3. 터치 기기면 `oly.js` 로드 후 `olySetup({...키맵...})` 호출
4. `index.js` 동적 삽입 → Emscripten 런타임 초기화
5. `Module.onRuntimeInitialized`에서 WAD를 MemFS(`FS.write`)에 기록
6. `Module.arguments = ['-iwad', 'freedoom1.wad']` 로 엔진 기동

### Module 커스텀 API (Dwasm 엔진이 직접 호출 — 제거 금지)
- `hideConsole()` / `showConsole()` — 엔진이 그래픽모드 진입/이탈 시 호출
- `captureMouse()` — 포인터락 요청 (터치모드에선 스킵)
- `winResized()` — 캔버스 해상도 변경 시 CSS 재계산
- `softExit(status)` — 게임 종료 처리
- `setStatus` 진행률 파싱 포맷: `"텍스트 (현재/전체)"`

## 조작
- 데스크탑: WASD + 마우스 (포인터락), F1 = 조작법
- 모바일: oly.js 오버레이 (방향키/WASD/발사/사용 버튼 자동 배치)
- 게임패드 지원 (엔진 내장)
- 로컬 세이브 지원 (IDBFS)

## 확장 포인트
- `freedoom2.wad` (Phase 2, DOOM2 호환)로 교체 가능 — `IWAD_NAME`만 변경
- PWAD/DEH/BEX 모드 지원: `userFileDict[이름] = ['p'|'d', data]` 추가 후
  `Module.arguments`에 `-file`/`-deh` 인자 추가
- URL 쿼리스트링이 엔진 인자로 전달 가능 (예: `?-skill&5`)

## Verse8 AI 프롬프트용 구조 설명
- 클래식 FPS, 4:3 레터박스 캔버스, WebGL 가속 소프트웨어 렌더링
- 에피소드/레벨 구조: E1M1~E4M9 (Phase 1 = 4 에피소드 × 9 맵)
- 밸런스 데이터는 WAD 내부 (THINGS/난이도별 스폰), DEH 패치로 오버라이드 가능

## 주의사항
- **이 프로젝트는 바이너리 포함 전체를 GitHub public 레포에 올려도 됨** (GPL/BSD)
- 단, 레포는 반드시 **public** 유지 (GPL 소스공개 의무 + Verse8 읽기)
- "DOOM" 상표 사용 금지 — 명칭은 항상 Freedoom
