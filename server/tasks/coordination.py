import asyncio
import logging

from tasks.llm import llm_query_task
from utils.session import Session

logger = logging.getLogger(__name__)


def trigger_llm(session: Session):
    if session.tts_task is not None and not session.tts_task.done():
        session.tts_task.cancel()
        session.tts_task = None

    if session.llm_task is not None and not session.llm_task.done():
        session.llm_task.cancel()
        session.llm_task = None

    prompt = session.prompt
    session.prompt = None

    logger.warning(f'Accepted prompt {prompt}')

    session.llm_task = asyncio.create_task(llm_query_task(session, prompt))
