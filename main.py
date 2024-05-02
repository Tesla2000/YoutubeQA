from __future__ import annotations

import scrapetube

from logic.add_questions_and_answers import add_questions_and_answers
from logic.add_videos_to_db import add_videos_to_db
from logic.create_lesson import create_lessons


def main() -> None:
    playlist_id = "PLWBKAf81pmOaP9naRiNAqug6EBnkPakvY"
    videos = tuple(scrapetube.get_playlist(playlist_id, long=True))
    print(len(videos))
    # add_videos_to_db(videos)
    # add_questions_and_answers()
    # create_lessons()


if __name__ == "__main__":
    main()
