from __future__ import annotations

from threading import Thread
from typing import Any
from typing import Sequence

from tqdm import tqdm

from Config import Config
from database.session import session
from logic._add_video_to_db import _add_video_to_db


def add_videos_to_db(videos: Sequence[dict[str, Any]]) -> None:
    step = Config.concurrent_transcription_threads
    for start in tqdm(
        range(0, len(videos), step),
        desc="Getting transcriptions...",
    ):
        threads = tuple(
            Thread(target=_add_video_to_db, args=(video,), daemon=True)
            for video in videos[start : start + step]
        )
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        session.commit()
