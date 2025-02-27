from typing import Literal, List

from pydantic import BaseModel
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession


class WhisperConfig(BaseModel):
    model: Literal['medium.en', 'small.en', 'large-v3']
    language: Literal['en', 'cs']


class LLMConfig(BaseModel):
    model: str
    system_prompt: str
    repeat_penalty: float
    temperature: float
    tools: List[str]


class TTSConfig(BaseModel):
    backend: Literal['kokoro']
    voice: str


class AppConfig(BaseModel):
    prevalidate_prompt: bool
    inactivity_timeout_ms: int


class SessionConfig(BaseModel):
    llm: LLMConfig
    whisper: WhisperConfig
    tts: TTSConfig
    app: AppConfig


async def get_previous_or_default_config(db: AsyncSession):
    from db.models import Chat
    most_recent_chat = (await db.execute(select(Chat).order_by(desc(Chat.started_at)))).scalar()

    if most_recent_chat is not None:
        return most_recent_chat.config_db

    with open('./config.json', 'r') as f:
        return SessionConfig.model_validate_json(f.read()).model_dump()
