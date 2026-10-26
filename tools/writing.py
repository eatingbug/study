#!/usr/bin/env python3
"""Asia/Seoul 기준 일일 글감·주간 블로그의 빈 틀을 만든다. 기존 파일은 보존한다."""

import argparse
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind', choices=('daily', 'weekly', 'post'))
    parser.add_argument('--slug', help='post 파일명에 쓸 소문자 영문·숫자·하이픈')
    parser.add_argument('--date', type=date.fromisoformat,
                        default=datetime.now(ZoneInfo('Asia/Seoul')).date(),
                        help='기준 날짜 YYYY-MM-DD (기본: 서울 오늘)')
    args = parser.parse_args()
    if args.kind == 'post':
        if not args.slug or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.slug):
            parser.error('post에는 --slug my-topic 형식의 영문 slug가 필요합니다.')
    elif args.slug is not None:
        parser.error('--slug는 post에만 사용할 수 있습니다.')
    day = args.date
    year, week, _ = day.isocalendar()
    week_name = f'{year}-W{week:02d}'
    monday = day - timedelta(days=day.weekday())
    fields = {
        'date': day.isoformat(), 'week': week_name,
        'week_start': monday.isoformat(),
        'week_end': (monday + timedelta(days=6)).isoformat(),
    }
    content = (ROOT / 'templates' / f'{args.kind}.md').read_text(encoding='utf-8')
    for key, value in fields.items():
        content = content.replace('{{' + key + '}}', value)
    if args.kind == 'post':
        name = f"{fields['week_end']}-{args.slug}"
        directory = 'posts'
    else:
        name = day.isoformat() if args.kind == 'daily' else week_name
        directory = args.kind
    target = ROOT / 'writing' / directory / f'{name}.md'
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with target.open('x', encoding='utf-8') as stream:
            stream.write(content)
    except FileExistsError:
        print(f'기존 파일 보존: {target}')
    else:
        print(f'빈 틀 생성 (완료·발행 처리 없음): {target}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
