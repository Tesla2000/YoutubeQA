from __future__ import annotations

import json
from itertools import chain

from sqlalchemy import select

from Config import Config
from database.Entities import Video
from database.session import session

_python_template = """
def generate_questions() -> list[str]:
    return {question_list}


def generate_answers(question: str, answer: str, _: str) -> bool | str:
    return True
"""


def create_lessons() -> None:
    for video in chain.from_iterable(session.execute(select(Video)).fetchall()):
        title = video.title.replace("/", "")
        Config.output_lesson_directory.joinpath("approved_lessons").joinpath(
            title
        ).with_suffix(".json").write_text(
            json.dumps(
                {
                    "description": "",
                    "author": "fratajczak124@gmail.com",
                    "basic_requrements": [],
                    "additional_requirements": [],
                    "section": "anthony explains",
                },
                indent=2,
            )
        )
        Config.output_lesson_directory.joinpath("final_tests").joinpath(
            title
        ).with_suffix(".json").write_text(
            json.dumps({"html_file": "Answer the question and submit"}, indent=2)
        )
        Config.output_lesson_directory.joinpath("final_tests_code").joinpath(
            title
        ).with_suffix(".py").write_text(
            _python_template.format(
                question_list=str(list(item.question for item in video.qas))
            )
        )
        training_material_folder = (
            Config.output_lesson_directory.joinpath("training_materials")
            .joinpath(title)
            .joinpath("anthony explains")
        )
        training_material_folder.mkdir(exist_ok=True, parents=True)
        training_material_folder.joinpath("0").with_suffix(".json").write_text(
            json.dumps(
                {
                    "expected_step_times": [video.length],
                    "author": "fratajczak124@gmail.com",
                    "video_path": {
                        "default": f"https://www.youtube.com/watch?v={video.id}"
                    },
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    create_lessons()
