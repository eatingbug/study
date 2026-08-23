#!/usr/bin/env python3
"""목록 페이지 생성기 겸 사이트 빌더.

lessons/ · reference/ 의 HTML 문서를 훑어서 목록 페이지를 만든다:

    index.html              전체 목록 (워크스페이스별 섹션)
    <topic>/index.html      워크스페이스 목록

각 문서에서 뽑는 것 — kicker(또는 eyebrow), h1, subtitle(또는 standfirst).
즉 문서를 쓸 때 이미 적는 것들이라 목록용으로 따로 관리할 게 없다.
새 레슨을 추가하고 이 스크립트를 돌리면(또는 main 에 푸시하면) 목록에 들어온다.

문서에서 목록 표시를 조정하려면 <head> 에 메타 태그를 넣는다:

    <meta name="index-gloss" content="목록에 쓸 한 줄 설명">
    <meta name="index-order" content="-10">    기본값 0. 음수는 앞으로, 양수는 뒤로.
                                               같은 값끼리는 파일명 순.
    <meta name="index-hidden" content="true">  목록에서 빼고 배포도 하지 않는다

워크스페이스 정보는 <topic>/workspace.json 에서 읽는다.

    python3 tools/build-index.py              목록 생성
    python3 tools/build-index.py --check      생성 결과가 커밋된 것과 같은지만 확인
    python3 tools/build-index.py --stage DIR  배포할 파일만 DIR 로 모은다
"""

import argparse
import html
import json
import re
import shutil
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO_URL = "https://github.com/eatingbug/study"
GLOSS_TARGET = 70  # 이 길이를 넘기 전까지 문장 단위로 채운다 (한국어 기준 한두 문장)

# 배포하는 것 — HTML 문서와 그것이 참조하는 정적 파일. allow-list 다.
# 여기에 없는 확장자는 새로 생겨도 사이트에 올라가지 않는다.
ASSET_SUFFIXES = {
    ".css", ".js", ".mjs", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp",
    ".avif", ".ico", ".woff", ".woff2", ".ttf", ".otf", ".pdf",
}
SECTIONS = ("lessons", "reference")

# 텍스트를 뽑을 때 닫는 태그가 없는 요소들 — 깊이를 세면 안 된다.
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}


# ── 문서에서 메타데이터 뽑기 ──────────────────────────────────────

class FirstElementText(HTMLParser):
    """태그 이름 또는 class 토큰으로 찾은 첫 요소의 텍스트.

    정규식으로 하면 (1) class="page-subtitle" 이 subtitle 로 잡히고
    (2) 안에 같은 이름의 태그가 중첩되면 첫 닫는 태그에서 잘린다.
    그래서 실제 파서로 깊이를 세며 읽는다.
    """

    def __init__(self, tag: str | None = None, css_class: str | None = None):
        super().__init__(convert_charrefs=True)
        self.tag = tag
        self.css_class = css_class
        self.depth = 0
        self.parts: list[str] = []
        self.done = False

    def _matches(self, tag: str, attrs: list[tuple[str, str | None]]) -> bool:
        if self.tag is not None:
            return tag == self.tag
        classes = (dict(attrs).get("class") or "").split()
        return self.css_class in classes

    def handle_starttag(self, tag, attrs):
        if self.done:
            return
        if tag in VOID_TAGS:
            if self.depth:
                self.parts.append(" ")  # <br> 를 문장 사이 공백으로
            return
        if self.depth:
            self.depth += 1
        elif self._matches(tag, attrs):
            self.depth = 1

    def handle_startendtag(self, tag, attrs):
        pass  # <br/> 같은 자기완결 태그는 깊이에 영향이 없다

    def handle_endtag(self, tag):
        if self.depth and not self.done:
            self.depth -= 1
            if self.depth == 0:
                self.done = True

    def handle_data(self, data):
        if self.depth and not self.done:
            self.parts.append(data)

    @property
    def text(self) -> str:
        return re.sub(r"\s+", " ", "".join(self.parts)).strip()


class MetaTags(HTMLParser):
    """<meta name=... content=...> 전부. 속성 순서·인용 부호에 의존하지 않는다."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.values: dict[str, str] = {}

    def handle_starttag(self, tag, attrs):
        if tag != "meta":
            return
        attr = dict(attrs)
        name, content = attr.get("name"), attr.get("content")
        if name and content is not None and name not in self.values:
            self.values[name.strip()] = content.strip()

    handle_startendtag = handle_starttag


def element_text(source: str, *, tag: str | None = None,
                 css_class: str | None = None) -> str:
    parser = FirstElementText(tag=tag, css_class=css_class)
    parser.feed(source)
    return parser.text


def by_class(source: str, *candidates: str) -> str:
    """주어진 class 를 순서대로 찾아 처음 걸리는 것의 텍스트."""
    for name in candidates:
        text = element_text(source, css_class=name)
        if text:
            return text
    return ""


def first_sentences(text: str, target: int = GLOSS_TARGET) -> str:
    """문장 경계에서 자른다. 최소 한 문장은 남긴다."""
    parts = re.findall(r"[^.!?]*[.!?]+|[^.!?]+$", text)
    out = ""
    for part in parts:
        if out and len(out) + len(part) > target:
            break
        out += part
    return out.strip() or text


def trim_kicker(kicker: str) -> str:
    """워크스페이스 목록용. 'Lesson 0001' 같은 앞머리는 목록 번호와 중복이다."""
    label = r"(?:Lesson|Reference|레슨|참조)\s*[\w.-]*"
    if re.fullmatch(label, kicker.strip()):
        return ""
    return re.sub(r"^%s\s*·\s*" % label, "", kicker.strip())


def read_doc(path: Path, index: int) -> dict:
    source = path.read_text(encoding="utf-8")
    meta = MetaTags()
    meta.feed(source)
    tags = meta.values

    title = (element_text(source, tag="h1")
             or element_text(source, tag="title")
             or path.stem)

    gloss = tags.get("index-gloss")
    if gloss is None:
        gloss = first_sentences(by_class(source, "subtitle", "standfirst"))

    order = tags.get("index-order", "")
    return {
        "path": path,
        "title": title,
        "kicker": by_class(source, "kicker", "eyebrow"),
        "gloss": gloss,
        "hidden": tags.get("index-hidden", "").lower() in ("true", "1", "yes"),
        "sort": (int(order) if re.fullmatch(r"-?\d+", order) else 0,
                 index, path.name),
    }


def collect(topic: Path, section: str) -> list[dict]:
    directory = topic / section
    if not directory.is_dir():
        return []
    docs = [read_doc(p, i)
            for i, p in enumerate(sorted(directory.glob("*.html")))
            if p.name != "index.html"]
    return sorted(docs, key=lambda d: d["sort"])


def workspaces() -> list[dict]:
    found = []
    for config in sorted(ROOT.glob("*/workspace.json")):
        topic = config.parent
        info = json.loads(config.read_text(encoding="utf-8"))
        docs = {s: collect(topic, s) for s in SECTIONS}
        found.append({
            "dir": topic.name,
            "path": topic,
            "title": info.get("title", topic.name),
            "blurb": info.get("blurb", ""),
            "order": info.get("order", 0),
            "docs": docs,
            "listed": {s: [d for d in docs[s] if not d["hidden"]] for s in SECTIONS},
            "styles": [p.name for p in sorted((topic / "assets").glob("*.css"))],
        })
    return sorted(found, key=lambda w: (w["order"], w["dir"]))


# ── 페이지 만들기 ────────────────────────────────────────────────

E = html.escape
BANNER = "<!-- 이 파일은 tools/build-index.py 가 생성한다. 직접 고치지 말 것. -->"


def root_page(all_workspaces: list[dict]) -> str:
    sections = []
    for w in all_workspaces:
        lessons, reference = w["listed"]["lessons"], w["listed"]["reference"]
        chip = "레슨 %d · 참조 %d" % (len(lessons), len(reference))
        blocks = []
        for label, docs in (("Lessons", lessons), ("Reference", reference)):
            if not docs:
                continue
            items = "\n".join(
                '''    <li><a href="./{href}">
      <span class="num">{kicker}</span>
      <span class="title">{title}</span>
      <span class="gloss">{gloss}</span>
    </a></li>'''.format(
                    href=E(d["path"].relative_to(ROOT).as_posix()),
                    kicker=E(d["kicker"]), title=E(d["title"]),
                    gloss=E(d["gloss"]),
                )
                for d in docs
            )
            blocks.append(
                '  <h3>%s</h3>\n  <ul class="docs">\n%s\n  </ul>' % (label, items)
            )
        sections.append(
            '''<section class="topic">
  <div class="topic-head">
    <h2><a href="./{dir}/index.html">{title}</a></h2>
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
  ul.docs .num:empty { display: none; }
  ul.docs .title { font-weight: 600; color: var(--accent); }
  ul.docs .gloss { display: block; font-size: 0.92rem; color: var(--ink-soft); margin-top: 0.15rem; }
  ul.docs .gloss:empty { display: none; }

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
        items = []
        for d in docs:
            href = d["path"].relative_to(w["path"]).as_posix()
            line = '  <li><a href="%s">%s</a>' % (E(href), E(d["title"]))
            if d["gloss"]:
                line += " — %s" % E(d["gloss"])
            kicker = trim_kicker(d["kicker"])
            if kicker:
                line += " <em>%s</em>" % E(kicker)
            items.append(line + "</li>")
        return "<%s>\n%s\n</%s>" % (tag, "\n".join(items), tag)

    blocks = []
    if w["listed"]["lessons"]:
        blocks.append("<h2>레슨</h2>\n" + listing(w["listed"]["lessons"], "ol"))
    if w["listed"]["reference"]:
        blocks.append("<h2>참조 문서</h2>\n" + listing(w["listed"]["reference"], "ul"))

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

<p><a href="../index.html">← 전체 워크스페이스</a></p>

</body>
</html>
""" % {
        "banner": BANNER, "links": links, "title": E(w["title"]),
        "dir_upper": E(w["dir"].upper()), "blurb": E(w["blurb"]),
        "blocks": "\n\n".join(blocks),
    }


# ── 배포본 모으기 ────────────────────────────────────────────────

def stage(all_workspaces: list[dict], target: Path) -> list[Path]:
    """배포할 파일만 target 으로 복사한다.

    allow-list 다 — 여기서 고른 것만 사이트에 올라간다. 새 마크다운·메모·
    노트북·실습 산출물이 저장소에 생겨도 자동으로 공개되지 않는다.
    index-hidden 을 붙인 문서는 목록에서 빠지는 것으로 끝나지 않고
    파일 자체가 배포되지 않는다.
    """
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    copied = []

    def copy(source: Path) -> None:
        destination = target / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied.append(destination.relative_to(target))

    for name in (".nojekyll", "index.html"):
        if (ROOT / name).exists():
            copy(ROOT / name)

    for w in all_workspaces:
        if (w["path"] / "index.html").exists():
            copy(w["path"] / "index.html")
        for section in SECTIONS:
            for doc in w["docs"][section]:
                if doc["hidden"]:
                    print("배포 제외 (index-hidden): %s"
                          % doc["path"].relative_to(ROOT))
                    continue
                copy(doc["path"])
        for directory in (w["path"] / "assets", *(w["path"] / s for s in SECTIONS)):
            if not directory.is_dir():
                continue
            for path in sorted(directory.rglob("*")):
                if path.is_file() and path.suffix.lower() in ASSET_SUFFIXES:
                    copy(path)

    return sorted(copied)


# ── 실행 ─────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="생성 결과가 커밋된 것과 같은지만 확인한다")
    parser.add_argument("--stage", metavar="DIR",
                        help="배포할 파일만 DIR 로 모은다")
    args = parser.parse_args()

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
        if path.exists() and path.read_text(encoding="utf-8") == content:
            print("변화 없음: %s" % rel)
            continue
        stale.append(str(rel))
        if not args.check:
            path.write_text(content, encoding="utf-8")
            print("생성: %s" % rel)

    for w in all_workspaces:
        hidden = sum(d["hidden"] for s in SECTIONS for d in w["docs"][s])
        print("  %s — 레슨 %d, 참조 %d%s"
              % (w["dir"], len(w["listed"]["lessons"]),
                 len(w["listed"]["reference"]),
                 ", 숨김 %d" % hidden if hidden else ""))

    if args.check and stale:
        print("\n목록이 문서와 어긋난다: %s" % ", ".join(stale), file=sys.stderr)
        print("python3 tools/build-index.py 를 돌리고 커밋할 것.", file=sys.stderr)
        return 1

    if args.stage:
        copied = stage(all_workspaces, Path(args.stage).resolve())
        print("\n---- 배포 대상 (%d) ----" % len(copied))
        for path in copied:
            print(path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
