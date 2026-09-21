#!/usr/bin/env python3
"""
style-check.py — 레슨 문체 검사기.

ASD-STE100(Simplified Technical English)의 규칙 중
한국어에 옮길 수 있는 것만 골라 기계적으로 검사한다.

검사 항목
  1. 문장 길이      : 20어절 초과 경고, 25어절 초과 위반
  2. 문단 문장 수   : <p> 하나에 6문장 초과 위반
  3. 줄표(—)        : 문장당 1개 초과 위반  (STE의 세미콜론 금지를 옮긴 것)
  4. 괄호           : 문장당 1개 초과 경고
  5. 긴 복합명사    : 13자 이상 붙어 있는 토큰 경고 (명사 3개 초과 나열 추정)
  6. 명사화         : "~의 가능성 / ~함으로써 / ~에 대한" 등 경고

HTML 과 마크다운을 모두 읽는다. 마크다운에서는 코드 블록과 표를 건너뛴다.
큰따옴표 안의 글은 5·6번 검사에서 제외한다. 인용과 반례는 고쳐 쓸 대상이 아니다.

사용:  python3 tools/style-check.py lessons/*.html reference/*.html AGENTS.md
"""

import re
import sys

SENT_WORDS_WARN = 20
SENT_WORDS_FAIL = 25
PARA_SENT_FAIL = 6
LONG_TOKEN = 13

NOMINALISATION = [
    "의 가능성", "함으로써", "에 대한", "에 있어", "하는 것이 가능",
    "의 여부", "를 통하여", "를 통해서",
]

BLOCK = re.compile(
    r"</(p|li|td|th|h1|h2|h3|div|blockquote|button|span|tr|table|ul|ol)>", re.I)
TAG = re.compile(r"<[^>]+>")
SCRIPT = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)
PARA = re.compile(r"<p\b[^>]*>(.*?)</p>", re.S | re.I)
ENTITY = re.compile(r"&[a-z]+;")

FENCE = re.compile(r"^```.*?^```", re.S | re.M)
TABLE_ROW = re.compile(r"^\s*\|.*$", re.M)
MD_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
INLINE_CODE = re.compile(r"`[^`]*`")
MD_HEAD = re.compile(r"^\s*#{1,6}\s*", re.M)
MD_BULLET = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+", re.M)
QUOTED = re.compile(r"[\"\u201c\u2018\u2019\u201d][^\"\u201c\u2018\u2019\u201d]*[\"\u201c\u2018\u2019\u201d]")


def strip(html):
    """블록 요소의 끝은 문장의 끝으로 본다. 표·목록이 한 문장으로 붙는 것을 막는다."""
    html = SCRIPT.sub(" ", html)
    html = BLOCK.sub(". ", html)
    html = TAG.sub(" ", html)
    html = ENTITY.sub(" ", html)
    return re.sub(r"\s+", " ", html).strip()


def strip_md(text):
    """마크다운을 산문만 남긴다. 코드 블록과 표는 산문이 아니므로 버린다."""
    text = FENCE.sub(" ", text)
    text = TABLE_ROW.sub(" ", text)
    text = INLINE_CODE.sub(" ", text)
    text = MD_LINK.sub(r"\1", text)
    text = MD_HEAD.sub("", text)
    text = MD_BULLET.sub("", text)
    # 빈 줄과 줄바꿈은 문단·문장의 끝으로 본다.
    text = re.sub(r"\n{2,}", ". ", text)
    text = re.sub(r"\n", ". ", text)
    return re.sub(r"\s+", " ", text).strip()


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", text)
    out = []
    for p in parts:
        p = p.strip()
        # 표를 걷어낸 자리에 남는 마침표만 있는 조각은 문장이 아니다.
        if p and re.search(r"[0-9A-Za-z가-힣]", p):
            out.append(p)
    return out


def check(path):
    raw = open(path, encoding="utf-8").read()
    is_md = path.lower().endswith((".md", ".markdown"))
    body = strip_md(raw) if is_md else strip(raw)
    problems = []

    # 1 + 3 + 4 + 5 + 6 : 문장 단위 검사
    for sent in sentences(body):
        words = sent.split()
        n = len(words)
        if n > SENT_WORDS_FAIL:
            problems.append(("FAIL", f"문장 {n}어절 (>{SENT_WORDS_FAIL})", sent))
        elif n > SENT_WORDS_WARN:
            problems.append(("warn", f"문장 {n}어절 (>{SENT_WORDS_WARN})", sent))

        if sent.count("—") > 1:
            problems.append(("FAIL", f"줄표 {sent.count('—')}개", sent))
        if sent.count("(") > 1:
            problems.append(("warn", f"괄호 {sent.count('(')}쌍", sent))

        # 인용과 반례는 고쳐 쓸 대상이 아니다. 따옴표 안은 빼고 본다.
        unquoted = QUOTED.sub(" ", sent)

        for w in unquoted.split():
            bare = re.sub(r"[^가-힣]", "", w)
            if len(bare) >= LONG_TOKEN:
                problems.append(("warn", f"긴 복합명사 '{bare}'", sent))

        for pat in NOMINALISATION:
            if pat in unquoted:
                problems.append(("warn", f"명사화 '{pat}'", sent))

    # 2 : 문단 검사. 마크다운은 빈 줄로 문단을 나눈다.
    if is_md:
        # 빈 줄로 나누고, 목록 항목은 각각 한 문단으로 본다.
        # 항목 일곱 개짜리 목록은 일곱 문장짜리 문단이 아니다.
        chunks = re.split(r"\n\s*\n", FENCE.sub(" ", raw))
        blocks = []
        for chunk in chunks:
            if re.search(r"^\s*(?:[-*+]|\d+\.)\s+", chunk, re.M):
                blocks += [strip_md(i) for i in
                           re.split(r"\n(?=\s*(?:[-*+]|\d+\.)\s+)", chunk)]
            else:
                blocks.append(strip_md(chunk))
    else:
        blocks = [strip(b) for b in PARA.findall(raw)]
    for block in blocks:
        ns = len(sentences(block))
        if ns > PARA_SENT_FAIL:
            problems.append(("FAIL", f"문단 {ns}문장 (>{PARA_SENT_FAIL})", block[:70]))

    return problems


def main():
    paths = sys.argv[1:]
    if not paths:
        print(__doc__)
        return 1

    total_fail = 0
    for path in paths:
        problems = check(path)
        fails = [p for p in problems if p[0] == "FAIL"]
        warns = [p for p in problems if p[0] == "warn"]
        total_fail += len(fails)

        mark = "OK  " if not fails else "FAIL"
        print(f"{mark} {path}  위반 {len(fails)} · 경고 {len(warns)}")
        for level, why, sent in fails + warns:
            tag = "  ✗" if level == "FAIL" else "  ·"
            print(f"{tag} {why}: {sent[:80]}")

    print()
    print(f"총 위반 {total_fail}건")
    return 1 if total_fail else 0


if __name__ == "__main__":
    sys.exit(main())
