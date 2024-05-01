from __future__ import annotations

from typing import List

from sqlalchemy import Computed
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from database.Base import Base
from database.session import engine


class Video(Base):
    __tablename__ = "video"
    id: Mapped[str] = mapped_column("id", String(11), primary_key=True)
    title: Mapped[str] = mapped_column("title", String(100))
    channel_name: Mapped[str] = mapped_column("channel", String(30))
    length: Mapped[int] = mapped_column("length", Integer)
    playlist_id: Mapped[str] = mapped_column("playlist", String, nullable=True)
    texts: Mapped[List["Text"]] = relationship(
        back_populates="video", cascade="all, delete-orphan"
    )
    qas: Mapped[List["QA"]] = relationship(
        back_populates="video", cascade="all, delete-orphan"
    )


class Text(Base):
    __tablename__ = "text"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    text: Mapped[str] = mapped_column("text", String)
    start_time: Mapped[float] = mapped_column("start_time", Float)
    duration: Mapped[float] = mapped_column("duration", Float)
    end_time: Mapped[float] = mapped_column(
        "end_time", Float, Computed("start_time + duration"), init=False
    )

    video_id: Mapped[str] = mapped_column(ForeignKey("video.id"))
    video: Mapped[Video] = relationship(back_populates="texts")


class QA(Base):
    __tablename__ = "QA"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    question: Mapped[str] = mapped_column("question", String)
    answer: Mapped[str] = mapped_column("answer", String)

    video_id: Mapped[str] = mapped_column(ForeignKey("video.id"))
    video: Mapped[Video] = relationship(back_populates="qas")


Base.metadata.create_all(engine)

if __name__ == "__main__":
    pass
    # Text.__table__.drop(engine)
    # QA.__table__.drop(engine)
    # Video.__table__.drop(engine)
