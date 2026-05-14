"""
MiniMax TTS 服务
文字转语音，使用 MiniMax API
"""
import os
from io import BytesIO
from typing import Optional
import openai

# MiniMax 客户端
_client = None

def get_tts_client():
    """获取 TTS 客户端单例"""
    global _client
    if _client is None:
        _client = openai.OpenAI(
            api_key=os.getenv("MINIMAX_API_KEY"),
            base_url="https://api.minimax.chat/v1"
        )
    return _client

def text_to_speech(
    text: str,
    voice_id: str = "male-qn-qingse",
    model: str = "speech-02-hd"
) -> BytesIO:
    """
    将文本转为语音

    Args:
        text: 要转换的文本
        voice_id: 语音 ID，默认使用男声
        model: 模型，默认 speech-02-hd

    Returns:
        BytesIO: 音频数据流
    """
    client = get_tts_client()

    response = client.audio.speech.create(
        model=model,
        voice_id=voice_id,
        input=text
    )

    audio_stream = BytesIO(response.content)
    return audio_stream

# 可用语音列表
AVAILABLE_VOICES = {
    "male-qn-qingse": "青年男声",
    "female-shaonv": "少女声",
    "male-bayi": "播音员男声",
    "female-tianme": "甜美女声"
}