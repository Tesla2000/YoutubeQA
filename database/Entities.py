from __future__ import annotations

from datetime import time
from datetime import timedelta
from typing import List

from sqlalchemy import Column
from sqlalchemy import Computed
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Interval
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database._Base import _Base
from database.session import engine


class Video(_Base):
    __tablename__ = "video"
    id: Mapped[str] = Column("id", String(11), primary_key=True)
    title: Mapped[str] = Column("title", String(100))
    channel: Mapped[str] = Column("channel", String(30))
    playlist: Mapped[str] = Column("playlist", String, nullable=True)
    texts: Mapped[List["Text"]] = relationship(back_populates="video")
    qas: Mapped[List["QA"]] = relationship(back_populates="video")


class Text(_Base):
    __tablename__ = "text"
    id: Mapped[int] = Column("id", Integer, primary_key=True)
    text: Mapped[str] = Column("text", String)
    start_time: Mapped[time] = Column("start_time", Time)
    end_time: Mapped[time] = Column("end_time", Time)
    duration: Mapped[timedelta] = Column(
        "duration", Interval, Computed("end_time - start_time")
    )

    video_id: Mapped[str] = mapped_column(ForeignKey("video.id"))
    video: Mapped[Video] = relationship(back_populates="texts")


class QA(_Base):
    __tablename__ = "QA"
    id: Mapped[int] = Column("id", Integer, primary_key=True)
    question: Mapped[str] = Column("question", String)
    answer: Mapped[str] = Column("answer", String)

    video_id: Mapped[str] = mapped_column(ForeignKey("video.id"))
    video: Mapped[Video] = relationship(back_populates="qas")


_Base.metadata.create_all(engine)
