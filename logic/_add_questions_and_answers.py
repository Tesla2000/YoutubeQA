from __future__ import annotations

from itertools import chain

from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy import select

from database.Entities import QA
from database.Entities import Text
from database.Entities import Video
from database.session import session

_prompt = PromptTemplate.from_template(
    """Given a transcript of youtube video create question-answer pairs. 
Questions and answers must be related strictly to programing topics.\n
Return a JSON object with questions as keys and answers aa values.\n
Return at most 10 pairs.\nTRANSCRIPT:\n
```{text}```\n
QUESTION_ANSWER_PAIRS:\n"""
)
_llm = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo-16k")
_chain = _prompt | _llm
_splitter = RecursiveCharacterTextSplitter(
    chunk_size=14000, chunk_overlap=100, length_function=_llm.get_num_tokens
)


def _add_questions_and_answers(video: Video) -> None:
    if video.qas:
        return
    video_text = _extract_text(video.id)
    docs = _splitter.create_documents([video_text])
    question_answer_pairs = _chain.invoke({"text": docs}).content
    raw_qas: dict[str, str] = eval(question_answer_pairs.replace('"\n', '",\n'))
    if "Q1" in raw_qas:
        raw_qas = dict(
            (raw_qas[f"Q{i}"], raw_qas[f"A{i}"])
            for i in range(1, 1 + len(raw_qas) // 2)
        )
    qas = list(
        QA(question=question, answer=answer) for question, answer in raw_qas.items()
    )
    session.add_all(qas)
    video.qas = qas


def _extract_text(video_id: str) -> str:
    return " ".join(
        chain.from_iterable(
            session.execute(
                select(Text.text)
                .where(Text.video_id == video_id)
                .order_by(Text.start_time)
            ).fetchall()
        )
    )
