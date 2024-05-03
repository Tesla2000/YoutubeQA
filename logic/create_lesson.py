from __future__ import annotations

import json
from itertools import chain

from sqlalchemy import select

from Config import Config
from database.Entities import Video
from database.session import session

_python_template = r"""import random
import langchain_openai
import langchain_core
def generate_questions() -> list[str]:
    questions = {question_list}
    return random.sample(questions, min(len(questions), 5))


def generate_answers(question: str, answer: str, _: str) -> bool | str:
    reference_answers = dict(zip({question_list}, {answer_list}))
    chat = langchain_openai.ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
    chat_answer = chat.invoke(
        [
            langchain_core.messages.SystemMessage(content="You will be given question, reference answer pair and users answer. "
                                  'You have to decide if the answer is correct. '
                                  'If it is respond with a single work "Correct" otherwise return a hint about the answer. '),
            langchain_core.messages.SystemMessage(content='The question: ' + question + '\n'
                                  'The reference answer: ' + reference_answers[question]),
            langchain_core.messages.HumanMessage(
                content=answer
            )
        ]
    ).content
    if chat_answer.startswith("Correct"):
        return True
    return chat_answer
"""


def create_lessons() -> None:
    for video in chain.from_iterable(session.execute(select(Video)).fetchall()):
        title = video.title.replace("/", "").replace(".", "")
        Config.output_lesson_directory.joinpath("approved_lessons").joinpath(
            title
        ).with_suffix(".json").write_text(
            json.dumps(
                {
                    "description": "",
                    "author": "fratajczak124@gmail.com",
                    "basic_requirements": [],
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
                question_list=_conv_fun(list(item.question for item in video.qas)),
                answer_list=_conv_fun(list(item.answer for item in video.qas)),
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


def _conv_fun(string_list: list[str]) -> str:
    return (
        str(string_list)
        .replace(" you are ", " the speaker is ")
        .replace(" you ", " the speaker ")
    )


if __name__ == "__main__":
    create_lessons()
