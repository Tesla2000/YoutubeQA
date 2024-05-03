from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config:
    db_name = os.getenv("POSTGRES_DB")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_username = os.getenv("POSTGRES_USER")
    db_url = f"postgresql://{db_username}:{db_password}@localhost:5432/{db_name}"
    root = Path(__file__).parent
    output_lesson_directory = root / "output_lessons"
    concurrent_transcription_threads = 5
    concurrent_question_answers_threads = 5


for variable in dir(Config):
    value = getattr(Config, variable)
    if isinstance(value, Path) and value.suffix == "" and not value.exists():
        value.mkdir(parents=True)
