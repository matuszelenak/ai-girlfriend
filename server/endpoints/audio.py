from fastapi import APIRouter
from starlette.responses import FileResponse

from providers import providers
from providers.base import TextToSpeechProvider

audio_router = APIRouter()


@audio_router.get('/audio/{chat_id}/{uuid}')
async def get_audio(chat_id: str, uuid: str):
    return FileResponse(f'/tts_output/{chat_id}/{uuid}', media_type='audio/wav')



@audio_router.get('/voices')
async def get_voices():
    tts_provider: TextToSpeechProvider = providers.get('tts')
    if tts_provider:
        voices = await tts_provider.get_voices()

        return voices

    return []
