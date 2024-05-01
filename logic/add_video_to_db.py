from __future__ import annotations

from typing import Any
from typing import Union

from sqlalchemy import select
from youtube_transcript_api import NoTranscriptFound
from youtube_transcript_api import YouTubeTranscriptApi

from database.Entities import Text
from database.Entities import Video
from database.session import session


def add_video_to_db(video: dict[str, Any], commit: bool = False) -> None:
    video_id = video["videoId"]
    if session.execute(select(Video.id).where(Video.id == video_id)).fetchall():
        return
    title = video["title"]["runs"][0]["text"]
    playlist_id = video["navigationEndpoint"]["watchEndpoint"]["playlistId"]
    channel_name = video["shortBylineText"]["runs"][0]["text"]
    length = int(video["lengthSeconds"])
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except NoTranscriptFound:
        return
    texts = list(
        Text(text=item["text"], start_time=item["start"], duration=item["duration"])
        for item in transcript
    )
    video_instance = Video(
        id=video_id,
        title=title,
        channel_name=channel_name,
        length=length,
        playlist_id=playlist_id,
        texts=texts,
    )
    session.add_all(texts)
    session.add(video_instance)
    if commit:
        session.commit()
