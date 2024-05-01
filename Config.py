from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config:
    db_name = os.getenv("POSTGRES_DB")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_username = os.getenv("POSTGRES_USER")
    root = Path(__file__).parent
    concurrent_transcription_threads = 5
    concurrent_question_answers_threads = 20


for variable in dir(Config):
    value = getattr(Config, variable)
    if isinstance(value, Path) and value.is_dir():
        value.mkdir(parents=True, exist_ok=True)
