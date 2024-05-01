from __future__ import annotations

from itertools import chain

from langchain_community.document_transformers import DoctranQATransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy import select

from database.Entities import QA
from database.Entities import Text
from database.Entities import Video
from database.session import session

_llm = DoctranQATransformer(openai_api_model="gpt-3.5-turbo")
_splitter = RecursiveCharacterTextSplitter(chunk_size=4000)


def _add_questions_and_answers(video: Video) -> None:
    if video.qas:
        return
    video_text = _extract_text(video.id)
    docs = _splitter.create_documents([video_text])
    qa_docs = _llm.transform_documents(docs)
    question_answer_pairs = tuple(
        chain.from_iterable(doc.metadata["questions_and_answers"] for doc in qa_docs)
    )
    qas = list(
        QA(question=pair["question"], answer=pair["answer"])
        for pair in question_answer_pairs
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
