# AGENTS.md

This repo holds teaching workspaces. Lessons and reference documents are HTML,
published to GitHub Pages. The prose inside them is **Korean**.

This file sets how that prose is written.

## A lesson is a manual, not an essay

The reader does not know the subject. They must still be able to follow it with effort.
So build no tension. Tell them things in order.

Dramatic emphasis, rhetorical questions and reveals carry no information.
Delete sentences like `여기가 오늘의 전부입니다`.

The basis is [ASD-STE100](https://www.asd-ste100.org/). It is an English standard,
so it does not transfer whole. The eleven rules below are the part that does.

## Rules

Rules marked `auto` are enforced by `tools/style-check.py`.
This file owns the numbers. To change one, edit here first, then match the script.

### Sentences

| | Rule | |
|---|---|---|
| 1 | Say one thing per sentence | |
| 2 | Keep sentences to 20 words or fewer, counting whitespace-separated chunks | auto |
| 3 | Keep one topic per paragraph, 6 sentences or fewer | auto |
| 4 | Use at most one em dash and one bracket pair per sentence | auto |

### Words

| | Rule | |
|---|---|---|
| 5 | Define each new term in one sentence where it first appears, and link the glossary | |
| 6 | Give each term one meaning. Call the same thing by the same name every time | |
| 7 | Stack at most three nouns together | auto |
| 8 | Prefer verbs to nominalisations. `검증할 수 있다`, not `검증의 가능성` | auto |

The glossary is `<topic>/reference/0000-glossary.html`. It owns that workspace's terms.
When a lesson defines a term, add it to the glossary too.
When the two definitions drift, the glossary wins.

### Claims

| | Rule | |
|---|---|---|
| 9 | Attach a source link to every claim | |
| 10 | Mark which claims are quoted and which are your own inference | |

Rule 10 buys trust. When you join two sources into a new conclusion, say so.
The `여기서부터는 추론입니다` block in `ai/lessons/0002-retrieval-loop.html` is the pattern.

### Quizzes

| | Rule | |
|---|---|---|
| 11 | Match answer options to the same character count, spaces included | |

A length difference leaks the answer. Count the options after writing them.

## Before you finish

Two commands must pass.

```sh
python3 tools/style-check.py <files you changed>   # 0 violations
python3 tools/build-index.py                       # regenerate the listing pages
```

Then check three things by eye.

- Every new term is in the glossary.
- Quiz options have equal character counts.
- No document links to a Markdown file by relative path.
  `tools/build-index.py` drops `.md` files and `learning-records/` from the deploy.
  A relative link 404s on the published site. Link the repo blob URL instead.

## Scope

**These rules apply to documents the learner reads.** That means `lessons/` and `reference/`.
`MISSION.md` counts too, because lessons link to it.

`NOTES.md`, `RESOURCES.md` and `learning-records/` are **working records**.
The rules are not enforced there. Run the checker on them if you like, but they need not pass.
Rule 6 still holds: when terms drift in the records, lessons drift with them.

Lessons already in `valley/` and `llmops/` predate these rules.
Leave them alone unless asked.

`tools/style-check.py` targets Korean prose. Its word counts and patterns assume Korean,
so it is not meaningful on this English file.

How each workspace is run lives in that workspace's `NOTES.md`.
Repo layout and build steps live in [README.md](./README.md).
