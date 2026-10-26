# 글쓰기 작업대

[일일·주간 루프](../docs/learning-loop.md)에 따라 원문 댓글을 연결하고 직접 쓴 글을 발행 준비한다.

```sh
python3 tools/writing.py daily
python3 tools/writing.py weekly
python3 tools/writing.py post --slug my-topic
```

- `daily/YYYY-MM-DD.md`: 오늘 배운 레슨·주간 이슈 댓글 원문 링크·적용 결과.
- `weekly/YYYY-Www.md`: ISO 주차별 사용자가 직접 쓴 주간 본문과 발행 링크.
- `posts/YYYY-MM-DD-slug.md`: Jekyll 포스트 준비본. 제목·카테고리와 검토한 본문을 채운다.

기준은 Asia/Seoul이다. 빈 파일은 쓰기 실적이 아니다.
이 폴더는 GitHub Pages에 배포되지 않지만 Git 저장소의 공개 범위를 따른다.
