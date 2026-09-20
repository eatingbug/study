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

사용:  python3 tools/style-check.py lessons/*.html reference/*.html
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


def strip(html):
    """블록 요소의 끝은 문장의 끝으로 본다. 표·목록이 한 문장으로 붙는 것을 막는다."""
    html = SCRIPT.sub(" ", html)
    html = BLOCK.sub(". ", html)
    html = TAG.sub(" ", html)
    html = ENTITY.sub(" ", html)
    return re.sub(r"\s+", " ", html).strip()


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def check(path):
    raw = open(path, encoding="utf-8").read()
    problems = []

    # 1 + 3 + 4 + 5 + 6 : 문장 단위 검사
    for sent in sentences(strip(raw)):
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

        for w in words:
            bare = re.sub(r"[^가-힣]", "", w)
            if len(bare) >= LONG_TOKEN:
                problems.append(("warn", f"긴 복합명사 '{bare}'", sent))

        for pat in NOMINALISATION:
            if pat in sent:
                problems.append(("warn", f"명사화 '{pat}'", sent))

    # 2 : 문단 검사
    for body in PARA.findall(raw):
        ns = len(sentences(strip(body)))
        if ns > PARA_SENT_FAIL:
            problems.append(("FAIL", f"문단 {ns}문장 (>{PARA_SENT_FAIL})", strip(body)[:70]))

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
