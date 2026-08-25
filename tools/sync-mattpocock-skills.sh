#!/usr/bin/env bash
# Vendor skills from mattpocock/skills into .claude/skills/.
#
# 프로젝트 스킬은 저장소에 커밋되어 있어야 웹·모바일·데스크탑 세션에서도
# 그대로 로드된다 (각 세션은 저장소를 새로 클론한다). 그래서 플러그인을
# 설치하는 대신 스킬 파일을 그대로 가져와 커밋한다.
#
#   ./tools/sync-mattpocock-skills.sh                 # 핀 고정된 커밋으로 teach 동기화
#   ./tools/sync-mattpocock-skills.sh --ref main      # 최신 main 으로 갱신
#   ./tools/sync-mattpocock-skills.sh grill-me        # 다른 스킬 추가로 가져오기
#
# 가져온 뒤에는 반드시 diff 를 확인하고 커밋한다.
set -euo pipefail

REPO="https://github.com/mattpocock/skills.git"
# 마지막으로 동기화한 upstream 커밋. --ref 로 갱신했다면 이 값도 같이 고친다.
REF="6654f6b60cd9d5be8b54c6fafe44346dabeb3b76"

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills=()

while [ $# -gt 0 ]; do
  case "$1" in
    --ref) REF="$2"; shift 2 ;;
    -h|--help) sed -n '2,14p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) skills+=("$1"); shift ;;
  esac
done
[ ${#skills[@]} -eq 0 ] && skills=(teach)

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

git clone --quiet --filter=blob:none --no-checkout "$REPO" "$tmp/skills"
git -C "$tmp/skills" fetch --quiet origin "$REF"
git -C "$tmp/skills" checkout --quiet FETCH_HEAD
resolved="$(git -C "$tmp/skills" rev-parse HEAD)"

for skill in "${skills[@]}"; do
  src="$(find "$tmp/skills/skills" -mindepth 2 -maxdepth 2 -type d -name "$skill" | head -1)"
  if [ -z "$src" ]; then
    echo "no such skill upstream: $skill" >&2
    exit 1
  fi
  dest="$root/.claude/skills/$skill"
  rm -rf "$dest"
  cp -r "$src" "$dest"
  cp "$tmp/skills/LICENSE" "$dest/LICENSE"
  echo "synced $skill  <-  ${src#"$tmp/skills/"}"
done

echo "upstream commit: $resolved"
