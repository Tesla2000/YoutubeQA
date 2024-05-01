from __future__ import annotations

from itertools import chain

from sqlalchemy import select

from database.Entities import Text
from database.session import session


def extract_text(video_id: str) -> str:
    return " ".join(
        chain.from_iterable(
            session.execute(
                select(Text.text)
                .where(Text.video_id == video_id)
                .order_by(Text.start_time)
            ).fetchall()
        )
    )
