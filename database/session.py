from __future__ import annotations

import atexit
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import create_session

from Config import Config

os.system(f"docker container start {Config.db_name}")

engine = create_engine(Config.db_url)
session = create_session(engine)


@atexit.register
def close() -> None:
    session.close()
