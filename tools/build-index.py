#!/usr/bin/env python3
"""목록 페이지 생성기.

lessons/ · reference/ 의 HTML 문서를 훑어서 목록 페이지를 만든다:

    index.html              전체 목록 (워크스페이스별 섹션)
    <topic>/index.html      워크스페이스 목록

각 문서에서 뽑는 것 — kicker(또는 eyebrow), h1, subtitle(또는 standfirst).
즉 문서를 쓸 때 이미 적는 것들이라 목록용으로 따로 관리할 게 없다.
새 레슨을 추가하고 이 스크립트를 돌리면(또는 main 에 푸시하면) 목록에 들어온다.

문서에서 목록 표시를 조정하려면 <head> 에 메타 태그를 넣는다:

    <meta name="index-gloss" content="목록에 쓸 한 줄 설명">
    <meta name="index-order" content="20">   숫자 작을수록 먼저. 기본값은 파일명 순
    <meta name="index-hidden" content="true">  목록에서 제외

워크스페이스 정보는 <topic>/workspace.json 에서 읽는다.

    python3 tools/build-index.py          생성
    python3 tools/build-index.py --check  생성 결과가 커밋된 것과 같은지만 확인
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO_URL = "https://github.com/eatingbug/study"
GLOSS_TARGET = 70  # 이 길이를 넘기 전까지 문장 단위로 채운다 (한국어 기준 한두 문장)


# ── 문서에서 메타데이터 뽑기 ──────────────────────────────────────

def strip_tags(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def first_sentences(text: str, target: int = GLOSS_TARGET) -> str:
    """문장 경계에서 자른다. 최소 한 문장은 남긴다."""
    parts = re.findall(r"[^.!?]*[.!?]+|[^.!?]+$", text)
    out = ""
    for part in parts:
        if out and len(out) + len(part) > target:
            break
        out += part
    return out.strip() or text


def meta(source: str, name: str) -> str | None:
    m = re.search(
        r'<meta\s+name="%s"\s+content="([^"]*)"' % re.escape(name), source
    )
    return html.unescape(m.group(1)).strip() if m else None


def tagged(source: str, *classes: str) -> str:
    """주어진 class 중 먼저 나오는 요소의 텍스트."""
    for cls in classes:
        m = re.search(
            r'<(\w+)[^>]*\bclass="[^"]*\b%s\b[^"]*"[^>]*>(.*?)</\1>' % cls,
            source,
            re.S,
        )
        if m:
            return strip_tags(m.group(2))
    return ""


def trim_kicker(kicker: str) -> str:
    """워크스페이스 목록용. 앞머리의 'Lesson 0001 ·' 같은 조각은 번호와 중복이다."""
    head, sep, rest = kicker.partition("·")
    if sep and re.match(r"^(Lesson|Reference|레슨|참조)\b", head.strip()):
        return rest.strip()
    return kicker


def read_doc(path: Path, index: int) -> dict | None:
    source = path.read_text(encoding="utf-8")
    if (meta(source, "index-hidden") or "").lower() in ("true", "1", "yes"):
        return None

    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", source, re.S)
    title_tag = re.search(r"<title>(.*?)</title>", source, re.S)
    title = strip_tags(h1.group(1)) if h1 else (
        strip_tags(title_tag.group(1)) if title_tag else path.stem
    )

    gloss = meta(source, "index-gloss")
    if gloss is None:
        gloss = first_sentences(tagged(source, "subtitle", "standfirst"))

    order = meta(source, "index-order")
    return {
        "href": path.relative_to(path.parent.parent.parent).as_posix(),
        "file": path.name,
        "title": title,
        "kicker": tagged(source, "kicker", "eyebrow"),
        "gloss": gloss,
        "sort": (int(order) if order and order.lstrip("-").isdigit() else 0,
                 index, path.name),
    }


def collect(topic: Path, section: str) -> list[dict]:
    directory = topic / section
    if not directory.is_dir():
        return []
    docs = []
    for i, path in enumerate(sorted(directory.glob("*.html"))):
        if path.name == "index.html":
            continue
        doc = read_doc(path, i)
        if doc:
            docs.append(doc)
    return sorted(docs, key=lambda d: d["sort"])


def workspaces() -> list[dict]:
    found = []
    for config in sorted(ROOT.glob("*/workspace.json")):
        topic = config.parent
        info = json.loads(config.read_text(encoding="utf-8"))
        found.append({
            "dir": topic.name,
            "title": info.get("title", topic.name),
            "blurb": info.get("blurb", ""),
            "order": info.get("order", 0),
            "lessons": collect(topic, "lessons"),
            "reference": collect(topic, "reference"),
            "styles": [p.name for p in sorted((topic / "assets").glob("*.css"))],
        })
    return sorted(found, key=lambda w: (w["order"], w["dir"]))


# ── 페이지 만들기 ────────────────────────────────────────────────

E = html.escape
BANNER = "<!-- 이 파일은 tools/build-index.py 가 생성한다. 직접 고치지 말 것. -->"


def root_page(all_workspaces: list[dict]) -> str:
    sections = []
    for w in all_workspaces:
        chip = "레슨 %d · 참조 %d" % (len(w["lessons"]), len(w["reference"]))
        blocks = []
        for label, docs in (("Lessons", w["lessons"]), ("Reference", w["reference"])):
            if not docs:
                continue
            items = "\n".join(
                '''    <li><a href="./{href}">
      <span class="num">{kicker}</span>
      <span class="title">{title}</span>
      <span class="gloss">{gloss}</span>
    </a></li>'''.format(
                    href=E(d["href"]), kicker=E(d["kicker"]),
                    title=E(d["title"]), gloss=E(d["gloss"]),
                )
                for d in docs
            )
            blocks.append(
                "  <h3>%s</h3>\n  <ul class=\"docs\">\n%s\n  </ul>" % (label, items)
            )
        sections.append(
            '''<section class="topic">
  <div class="topic-head">
    <h2><a href="./{dir}/">{title}</a></h2>
    <span class="status">{chip}</span>
  </div>
  <p class="topic-why">{blurb}</p>

{blocks}
</section>'''.format(
                dir=E(w["dir"]), title=E(w["title"]), chip=E(chip),
                blurb=E(w["blurb"]), blocks="\n\n".join(blocks),
            )
        )

    return """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>study · 학습 워크스페이스</title>
<meta name="description" content="학습 워크스페이스의 레슨과 참조 문서 목록.">
%(banner)s
<style>
  :root {
    --ink:        #1a1a18;
    --ink-soft:   #55534e;
    --ink-faint:  #8a8781;
    --paper:      #fffef9;
    --paper-alt:  #f6f4ec;
    --rule:       #ded9cc;
    --accent:     #9c3d1e;
    --accent-bg:  #fbeee7;
    --font-serif: "Iowan Old Style", "Apple Garamond", "Source Serif 4", Palatino, "Apple SD Gothic Neo", serif;
    --font-sans:  -apple-system, BlinkMacSystemFont, "Helvetica Neue", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --ink: #e8e4da; --ink-soft: #a8a49a; --ink-faint: #77736a;
      --paper: #16150f; --paper-alt: #1f1e17; --rule: #35332a;
      --accent: #e8875c; --accent-bg: #2a1f18;
    }
  }
  *, *::before, *::after { box-sizing: border-box; }
  body {
    margin: 0 auto;
    padding: 4rem 2rem 8rem;
    max-width: 52rem;
    background: var(--paper);
    color: var(--ink);
    font: 1.05rem/1.7 var(--font-serif);
    word-break: keep-all;
    overflow-wrap: break-word;
    -webkit-font-smoothing: antialiased;
  }
  a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 0.15em; }

  .kicker {
    font: 0.75rem/1 var(--font-sans);
    letter-spacing: 0.16em; text-transform: uppercase;
    color: var(--ink-faint); margin: 0 0 0.9rem;
  }
  h1 { font-size: 2.1rem; line-height: 1.2; margin: 0 0 0.8rem; letter-spacing: -0.01em; }
  .subtitle { color: var(--ink-soft); max-width: 34rem; margin: 0 0 2.5rem; }

  section.topic {
    border-top: 1px solid var(--rule);
    padding-top: 2rem;
    margin-top: 3rem;
  }
  .topic-head {
    display: flex; flex-wrap: wrap; align-items: baseline;
    gap: 0.75rem; margin-bottom: 0.4rem;
  }
  .topic-head h2 { font-size: 1.5rem; margin: 0; letter-spacing: -0.01em; }
  .topic-head h2 a { color: inherit; text-decoration: none; }
  .topic-head h2 a:hover { color: var(--accent); }
  .status {
    font: 0.7rem/1 var(--font-sans); letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--ink-faint); border: 1px solid var(--rule);
    border-radius: 3px; padding: 0.3rem 0.45rem;
  }
  .topic-why { color: var(--ink-soft); font-size: 0.97rem; margin: 0 0 1.8rem; max-width: 34rem; }

  h3 {
    font: 0.72rem/1 var(--font-sans); letter-spacing: 0.14em; text-transform: uppercase;
    color: var(--ink-faint); margin: 2rem 0 0.9rem;
  }

  ul.docs { list-style: none; margin: 0; padding: 0; }
  ul.docs li { border-bottom: 1px solid var(--rule); }
  ul.docs li:first-child { border-top: 1px solid var(--rule); }
  ul.docs a {
    display: block; padding: 0.85rem 0.2rem;
    text-decoration: none; color: inherit;
  }
  ul.docs a:hover, ul.docs a:focus-visible {
    background: var(--accent-bg); outline: none;
  }
  ul.docs .num {
    font: 0.72rem/1 var(--font-sans); letter-spacing: 0.08em;
    color: var(--ink-faint); display: block; margin-bottom: 0.25rem;
  }
  ul.docs .title { font-weight: 600; color: var(--accent); }
  ul.docs .gloss { display: block; font-size: 0.92rem; color: var(--ink-soft); margin-top: 0.15rem; }

  footer {
    border-top: 1px solid var(--rule);
    margin-top: 4rem; padding-top: 1.5rem;
    font: 0.9rem/1.7 var(--font-sans); color: var(--ink-soft);
  }
  footer p { margin: 0 0 0.6rem; }
  footer kbd, footer code {
    font: 0.85em/1 ui-monospace, "SF Mono", Menlo, monospace;
    background: var(--paper-alt); border: 1px solid var(--rule);
    border-radius: 3px; padding: 0.15em 0.4em;
  }
</style>
</head>
<body>

<p class="kicker">Study workspace</p>
<h1>압축된 학습 결과물</h1>
<p class="subtitle">노트를 쌓는 게 아니라 다시 열게 되는 문서를 남긴다.
레슨은 한 번 하고 지나가고, 참조 문서는 계속 옆에 둔다.
저장소는 <a href="%(repo)s">eatingbug/study</a>.</p>

%(sections)s

<footer>
  <p>모든 문서는 인쇄용 스타일이 들어 있다 — 브라우저에서 그대로 <kbd>⌘P</kbd>.</p>
  <p>이 목록은 <code>tools/build-index.py</code> 가 문서에서 생성한다.
  새 레슨을 추가하고 <code>main</code> 에 푸시하면 자동으로 올라온다.</p>
</footer>

</body>
</html>
""" % {"banner": BANNER, "repo": REPO_URL, "sections": "\n\n".join(sections)}


def topic_page(w: dict) -> str:
    links = "\n".join(
        '<link rel="stylesheet" href="assets/%s">' % E(name) for name in w["styles"]
    )

    def listing(docs: list[dict], tag: str) -> str:
        items = "\n".join(
            '  <li><a href="{href}">{title}</a> — {gloss}{kicker}</li>'.format(
                href=E(d["href"].split("/", 1)[1]),
                title=E(d["title"]),
                gloss=E(d["gloss"]),
                kicker=(" <em>%s</em>" % E(trim_kicker(d["kicker"])))
                if trim_kicker(d["kicker"]) else "",
            )
            for d in docs
        )
        return "<%s>\n%s\n</%s>" % (tag, items, tag)

    blocks = []
    if w["lessons"]:
        blocks.append("<h2>레슨</h2>\n" + listing(w["lessons"], "ol"))
    if w["reference"]:
        blocks.append("<h2>참조 문서</h2>\n" + listing(w["reference"], "ul"))

    return """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s · 워크스페이스</title>
%(banner)s
%(links)s
</head>
<body>

<header class="masthead">
  <p class="kicker eyebrow">Workspace · %(dir_upper)s</p>
  <h1>%(title)s</h1>
  <p class="subtitle standfirst">%(blurb)s</p>
</header>

%(blocks)s

<p><a href="../">← 전체 워크스페이스</a></p>

</body>
</html>
""" % {
        "banner": BANNER, "links": links, "title": E(w["title"]),
        "dir_upper": E(w["dir"].upper()), "blurb": E(w["blurb"]),
        "blocks": "\n\n".join(blocks),
    }


# ── 실행 ─────────────────────────────────────────────────────────

def main() -> int:
    check = "--check" in sys.argv[1:]
    all_workspaces = workspaces()
    if not all_workspaces:
        print("workspace.json 이 있는 디렉터리를 찾지 못했다.", file=sys.stderr)
        return 1

    pages = {ROOT / "index.html": root_page(all_workspaces)}
    for w in all_workspaces:
        pages[ROOT / w["dir"] / "index.html"] = topic_page(w)

    stale = []
    for path, content in pages.items():
        rel = path.relative_to(ROOT)
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            print("변화 없음: %s" % rel)
            continue
        stale.append(str(rel))
        if not check:
            path.write_text(content, encoding="utf-8")
            print("생성: %s" % rel)

    for w in all_workspaces:
        print("  %s — 레슨 %d, 참조 %d"
              % (w["dir"], len(w["lessons"]), len(w["reference"])))

    if check and stale:
        print("\n목록이 문서와 어긋난다: %s" % ", ".join(stale), file=sys.stderr)
        print("python3 tools/build-index.py 를 돌리고 커밋할 것.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
