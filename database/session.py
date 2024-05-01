from __future__ import annotations

import atexit
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import create_session

from Config import Config

os.system(f"docker container start {Config.db_name}")

engine = create_engine(
    f"postgresql://{Config.db_username}:{Config.db_password}@localhost:5432/{Config.db_name}",
    echo=True,
)
session = create_session(engine)


@atexit.register
def close() -> None:
    session.close()
