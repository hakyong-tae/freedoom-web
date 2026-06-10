# V8m (Freedoom Web) — 구조 분석 노트

> 게임명 V8m = "V8doom" 줄임말 (8 = oo). 커스텀 아트는 `public/custom.wad` (PWAD)로 교체 예정 —
> 존재하면 자동 로드되어 원본 위에 덮임 (TITLEPIC, M_DOOM, M_* 메뉴 그래픽 등).

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
1. 페이지 로드 즉시 `fetch('freedoom1.wad')` 백그라운드 다운로드 (진행률 표시)
2. **탭투스타트**: 다운로드 완료 시 시작 버튼 활성화 — 사용자 제스처로만 부팅
   (모바일 오디오 자동재생 정책 + Verse8 광고 제스처 규칙 충족)
3. `userFileDict['freedoom1.wad'] = ['i', Uint8Array]` 형태로 보관
4. 터치 기기면 `oly.js` 로드 후 `olySetup({...키맵...})` 호출
5. `index.js` 동적 삽입 → Emscripten 런타임 초기화
6. `Module.onRuntimeInitialized`에서 WAD를 MemFS(`FS.write`)에 기록
7. `Module.arguments = ['-iwad', 'freedoom1.wad']` 로 엔진 기동

## 광고 부활 시스템 (Verse8 Ads)
엔진 자체를 패치해서 빌드 (engine-patches/ 참조, emsdk 6.0.0):
- **C→JS**: `P_KillMobj`에서 콘솔플레이어 사망 시 `Module.onPlayerDeath()` 호출
  - 부두돌(Boom 맵 스크립팅용 더미 플레이어) 필터: `target->player->mo == target`
  - 데모 재생/넷게임 중엔 발화 안 함
- **JS→C** (EMSCRIPTEN_KEEPALIVE export):
  - `Module._JS_PlayerIsDead()` — 부활 제안 유효성 폴링 (400ms 워처가 오버레이 자동 철회)
  - `Module._JS_RevivePlayer()` — 그 자리 부활 (체력/충돌플래그/스테이트/시점/무기 복원 + 3초 무적 `pw_invulnerability`)
  - `Module._JS_GetHealth()` — 현재 체력 (인게임 아니면 -1)
  - `Module._JS_FullHeal()` — 체력 100% 회복 (생존+미만일 때만 1 반환)

## 광고 풀힐 버튼 (full-heal placement)
- 캔버스 우하단(상태바 SUPPLY 명판 위)에 떠 있는 HTML 버튼 — 상태바는 캔버스 안 그림이라 직접 클릭 불가
- 5분 쿨다운 (`localStorage.lastHealAd`), 쿨다운 중엔 M:SS 카운트다운 표시
- 체력 100%거나 인게임 아니면 비활성, `unsupported_env`면 세션 동안 숨김
- rewarded → `_JS_FullHeal()` → 쿨다운 시작 + 픽업 플래시 피드백
- **플로우**: 사망 → 오버레이("광고 보고 부활"/"포기") → `Verse8Ads.showRewarded({placementId:'revive-hero'})`
  - `rewarded` → `_JS_RevivePlayer()` / `dismissed` → 토스트+재시도 / `unsupported_env` → 세션 동안 부활 UI 비활성(바닐라 사망 흐름)
- 보상이 저가치(부활 1회)라 서버 검증은 생략 (Verse8 docs 권고)
- 로컬 테스트: URL에 `?simulateads` → 가짜 rewarded 응답으로 전체 플로우 시뮬레이션

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
