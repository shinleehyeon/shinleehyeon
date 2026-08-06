#!/usr/bin/env python3
"""Update age / next-birthday countdown in README.md."""

from __future__ import annotations

import re
from datetime import date, datetime, timezone, timedelta
from pathlib import Path

BIRTHDAY = date(2008, 1, 3)
KST = timezone(timedelta(hours=9))
README = Path(__file__).resolve().parents[2] / "README.md"
SECTION = re.compile(
    r"<!--START_SECTION:age-->.*?<!--END_SECTION:age-->",
    re.DOTALL,
)


def calc(today: date) -> tuple[int, int, date]:
    age = today.year - BIRTHDAY.year - (
        (today.month, today.day) < (BIRTHDAY.month, BIRTHDAY.day)
    )
    next_bday = date(today.year, BIRTHDAY.month, BIRTHDAY.day)
    if next_bday <= today:
        next_bday = date(today.year + 1, BIRTHDAY.month, BIRTHDAY.day)
    days_left = (next_bday - today).days
    return age, days_left, next_bday


def main() -> None:
    today = datetime.now(KST).date()
    age, days_left, next_bday = calc(today)

    if days_left == 0:
        line = f"> 🎂 오늘 생일! 만 **{age}**세가 되었습니다"
    else:
        line = f"> 🎂 만 **{age}**세 · 다음 생일까지 **D-{days_left}**"

    block = f"<!--START_SECTION:age-->\n{line}\n<!--END_SECTION:age-->"
    text = README.read_text(encoding="utf-8")
    if not SECTION.search(text):
        raise SystemExit("age section markers not found in README.md")

    updated = SECTION.sub(block, text)
    README.write_text(updated, encoding="utf-8")
    print(f"updated: age={age}, d-day={days_left}")


if __name__ == "__main__":
    main()
