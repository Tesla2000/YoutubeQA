from __future__ import annotations

from itertools import chain
from itertools import filterfalse
from threading import Thread
from typing import Optional
from typing import Sequence

from sqlalchemy import select
from tqdm import tqdm

from Config import Config
from database.Entities import Video
from database.session import session
from logic._add_questions_and_answers import _add_questions_and_answers


def add_questions_and_answers(videos: Optional[Sequence[Video]] = None) -> None:
    if videos is None:
        videos = _get_videos()
    videos = tuple(filterfalse(lambda video: video.qas, videos))
    step = Config.concurrent_question_answers_threads
    for start in tqdm(
        range(0, len(videos), step),
        desc="Adding questions and answers...",
    ):
        threads = tuple(
            Thread(target=_add_questions_and_answers, args=(video,), daemon=True)
            for video in videos[start : start + step]
        )
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        session.commit()
        pass


def _get_videos() -> Sequence[Video]:
    return tuple(chain.from_iterable(session.execute(select(Video)).fetchall()))


if __name__ == "__main__":
    add_questions_and_answers()
