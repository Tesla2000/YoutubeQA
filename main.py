from __future__ import annotations

from threading import Thread

import scrapetube
from tqdm import tqdm

from Config import Config
from database.session import session
from logic.add_video_to_db import add_video_to_db


def main() -> None:
    playlist_id = "PLWBKAf81pmOaP9naRiNAqug6EBnkPakvY"
    videos = tuple(scrapetube.get_playlist(playlist_id))
    for start in tqdm(range(0, len(videos), Config.concurrent_threads)):
        threads = tuple(
            Thread(target=add_video_to_db, args=(video,), daemon=True)
            for video in videos[start : start + Config.concurrent_threads]
        )
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        session.commit()


if __name__ == "__main__":
    main()
