# study

학습 워크스페이스 모음. 각 디렉터리가 하나의 주제이고,
[Matt Pocock의 `teach` 스킬](https://github.com/mattpocock) 규약을 따른다.

목표는 노트를 쌓는 것이 아니라 **압축된 학습 결과물**을 남기는 것이다 —
레슨은 한 번 하고 지나가지만, 참조 문서는 계속 다시 열게 된다.

## 웹에서 보기

<https://eatingbug.github.io/study/>

레슨과 참조 문서를 브라우저에서 바로 읽을 수 있다. `main` 에 푸시하면
[GitHub Actions 워크플로](./.github/workflows/pages.yml)가 목록을 다시 만들고
정적 사이트로 배포한다 (Jekyll 빌드 없음 — 루트의 `.nojekyll` 참조).

> **처음 한 번만:** 저장소 Settings → Pages → **Source** 를 `GitHub Actions` 로 바꿔야
> 워크플로가 배포 권한을 얻는다. 그 뒤로는 푸시할 때마다 자동으로 갱신된다.

사이트 구조는 디렉터리 구조 그대로다 — 루트에 전체 목록,
`/llmops/` 와 `/valley/` 에 워크스페이스별 목록.

**사이트에 올라가는 것은 HTML(레슨·참조 문서)과 `assets/` 뿐이다.**
빌더가 올릴 파일을 골라내는 방식은 allow-list다 — `lessons/` · `reference/` 의
HTML과 `assets/` 의 정적 파일만 복사한다. 그래서 메모·노트북·실습 산출물이
저장소에 새로 생겨도 **자동으로 공개되지 않는다.** 마크다운 문서
(`MISSION.md` · `NOTES.md` · `RESOURCES.md` · `GLOSSARY.md`)와 `learning-records/`
도 여기서 걸러진다 — 학습 기록은 사이트의 일부가 아니고, GitHub에서
렌더링해 읽는 편이 낫다.

### 새 레슨을 추가하면

목록 페이지(`index.html` · `<topic>/index.html`)는 손으로 쓰지 않는다.
`tools/build-index.py` 가 `lessons/` · `reference/` 의 문서를 훑어서 만든다 —
배포할 때마다 다시 생성하므로 **파일을 추가하고 푸시하면 목록에 자동으로 올라온다.**

각 문서에서 뽑는 것은 문서를 쓸 때 이미 적는 것들이다.

| 목록에 나오는 것 | 어디서 오는가 |
|---|---|
| 제목 | `<h1>` (없으면 `<title>`) |
| 곁줄 (Lesson 0001 · 약 20분) | `class="kicker"` 또는 `class="eyebrow"` |
| 한 줄 설명 | `class="subtitle"` 또는 `class="standfirst"` 의 첫 문장들 |
| 순서 | 파일명 순 (`0001-` · `0002-` …) |

목록에 나가는 모습을 문서에서 조정하려면 `<head>` 에 메타 태그를 넣는다.

```html
<meta name="index-gloss"  content="목록에 쓸 한 줄 설명">
<meta name="index-order"  content="-10">    <!-- 기본값 0. 음수는 앞으로, 양수는 뒤로 -->
<meta name="index-hidden" content="true">   <!-- 목록에서 빼고 배포도 안 한다 -->
```

`index-order` 를 안 쓰면 0으로 보고 파일명 순으로 놓는다. 그래서 특정 문서를
맨 앞으로 당기려면 음수를, 맨 뒤로 밀려면 양수를 준다.
`index-hidden` 을 붙인 문서는 목록에서 빠지는 것으로 끝나지 않고
**배포본에서도 제외된다** — 초안을 URL로 주워갈 수 없다.

새 주제를 시작할 때는 `<topic>/workspace.json` 만 만들면 목록에 섹션이 생긴다.

```json
{ "title": "LLMOps", "blurb": "한 줄 소개", "order": 1 }
```

로컬에서 목록을 미리 보거나 최신으로 맞추려면:

```sh
python3 tools/build-index.py              # 목록 생성
python3 tools/build-index.py --check      # 커밋된 목록이 문서와 맞는지만 확인
python3 tools/build-index.py --stage _site  # 배포될 파일 그대로 모아 보기
```

`<topic>/assets/*.css` 는 자동으로 링크되므로 워크스페이스 목록은 그 주제의 문서와
같은 스타일로 나온다.

## `/teach` 스킬

레슨을 만드는 것은 [Matt Pocock의 `teach` 스킬](https://github.com/mattpocock/skills)이다.
스킬 자체를 [`.claude/skills/teach/`](./.claude/skills/teach) 에 **복사해 커밋해 두었다.**
Claude Code 세션은 어느 환경에서 열든 이 저장소를 클론하므로,
웹(claude.ai/code) · 모바일 · 데스크탑 앱 · 터미널 CLI 어디서 열어도
플러그인 설치 없이 `/teach` 가 바로 잡힌다.

```
/teach                     학습 기록을 읽고 다음에 배울 것을 정한다
/teach DCF 할인율 계산      배울 것을 직접 지정한다
```

워크스페이스를 정해서 쓰려면 그 디렉터리에서 세션을 열거나,
어떤 워크스페이스인지 말해 주면 된다 — 스킬은 현재 디렉터리를
학습 워크스페이스로 보고 `MISSION.md` · `learning-records/` 를 읽는다.

### 스킬 갱신

[`tools/sync-mattpocock-skills.sh`](./tools/sync-mattpocock-skills.sh) 가 upstream에서
스킬 파일을 다시 가져온다. 핀으로 고정된 커밋을 쓰므로 돌려도 조용히 바뀌지 않는다.

```sh
./tools/sync-mattpocock-skills.sh              # 고정된 커밋 그대로 다시 가져오기
./tools/sync-mattpocock-skills.sh --ref main   # 최신으로 갱신 (스크립트의 REF 도 같이 고친다)
./tools/sync-mattpocock-skills.sh grill-me     # 다른 스킬을 추가로 가져오기
```

가져온 뒤 `git diff` 로 무엇이 바뀌었는지 확인하고 커밋한다.
`.claude/settings.json` 의 `enabledPlugins` 는 로컬 CLI에서 Matt Pocock 스킬 모음
전체를 플러그인으로 쓸 때를 위해 남겨 둔 것이고, `/teach` 만 쓰는 데는 필요하지 않다.

## 워크스페이스

| 주제 | 내용 | 상태 |
|---|---|---|
| [`ai/`](./ai) | AI 엔지니어 — 학습 시스템으로 전문성 쌓기 | 진행 중 (레슨 2) |
| [`llmops/`](./llmops) | LLM 운영 체계 — 평가·관측성·비용·배포 | `ai/` 로 흡수 (레슨 2, 참조용) |
| [`valley/`](./valley) | 기업가치 평가 — DCF·할인율 | 진행 중 (레슨 8) |

## 각 워크스페이스의 구조

```
<topic>/
├── workspace.json      제목·소개·순서. 목록 페이지가 이걸 읽는다
├── index.html          워크스페이스 목록 (생성물 — 직접 고치지 않는다)
├── MISSION.md          왜 이걸 배우는가. 모든 레슨이 여기로 소급된다
├── NOTES.md            학습 선호·제약·결정 기록
├── RESOURCES.md        고신뢰 1차 자료 + 커뮤니티 + 아직 못 채운 Gap
├── GLOSSARY.md         이 주제의 표준 용어 (이해가 증명된 것만 등재)
├── lessons/            0001-*.html — 한 번에 하나씩, 짧게, 인터랙티브
├── reference/          압축된 참조 문서. 프린트해서 옆에 두는 용도
├── learning-records/   무엇을 알게 됐고 그래서 다음에 뭘 배울지 (ADR 형식)
└── assets/             레슨이 공유하는 스타일시트·퀴즈 위젯 등
```

레슨과 참조 문서는 HTML이다. 위의 [배포된 사이트](https://eatingbug.github.io/study/)에서 읽거나
로컬 파일을 브라우저에서 바로 열면 된다. 인쇄용 스타일도 들어 있다.

```sh
open llmops/lessons/0001-llmops-map-and-self-audit.html
```

각 워크스페이스의 `index.html` 은 그 워크스페이스의 목록 페이지고,
루트의 `index.html` 은 전체 목록이다. 둘 다 생성물이니 직접 고치지 말고
`tools/build-index.py` 를 돌린다.

## 저장소에 넣지 않는 것

- `raw/` — 저작권 있는 원본 자료(유료 구독 콘텐츠 등). 로컬에만 둔다.
- 실습에 쓴 사내 데이터·로그·CSV. 결과 **숫자**만 학습기록에 옮겨 적는다.

자세한 규칙은 [`.gitignore`](./.gitignore) 참조.
