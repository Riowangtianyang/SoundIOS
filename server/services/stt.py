"""
MiniMax 语音转文字服务
基于 MiniMax OpenAI 兼容 API 实现音频转写
"""

import os
from typing import Optional, Dict, List

# MiniMax OpenAI 兼容 SDK
try:
    import openai
    OPENAI_SDK_AVAILABLE = True
except ImportError:
    OPENAI_SDK_AVAILABLE = False
    print("Warning: openai SDK not installed. Install with: pip install openai")


class MiniMaxSTTService:
    """MiniMax 语音识别服务"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        group_id: Optional[str] = None
    ):
        """
        初始化 MiniMax ASR 服务

        Args:
            api_key: MiniMax API Key（优先从环境变量获取）
            group_id: MiniMax Group ID
        """
        self.api_key = api_key or os.getenv("MINIMAX_API_KEY")
        self.group_id = group_id or os.getenv("MINIMAX_GROUP_ID")

        if not self.api_key:
            print("Warning: MINIMAX_API_KEY not found in environment variables")

        # 创建 OpenAI 客户端（MiniMax 兼容）
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url="https://api.minimax.chat/v1"
        )

    async def transcribe(self, audio_path: str) -> Dict:
        """
        使用 MiniMax ASR 转写音频文件

        Args:
            audio_path: 音频文件路径（支持 wav, mp3, m4a, opus 格式）

        Returns:
            {
                "text": "转写文本",
                "segments": [
                    {"start": 0, "end": 5, "text": "你好"},
                    {"start": 5, "end": 10, "text": "世界"}
                ],
                "success": True
            }
        """
        if not OPENAI_SDK_AVAILABLE:
            return {
                "text": "",
                "segments": [],
                "success": False,
                "error": "OpenAI SDK not installed"
            }

        if not self.api_key:
            return {
                "text": "",
                "segments": [],
                "success": False,
                "error": "MINIMAX_API_KEY not configured"
            }

        if not os.path.exists(audio_path):
            return {
                "text": "",
                "segments": [],
                "success": False,
                "error": f"Audio file not found: {audio_path}"
            }

        try:
            # 打开音频文件
            with open(audio_path, "rb") as audio_file:
                # 调用 MiniMax 语音转文字 API
                response = self.client.audio.transcriptions.create(
                    model="speech-01",
                    file=audio_file
                )

                # 解析结果
                result_text = response.text
                segments = self._parse_to_segments(result_text)

                return {
                    "text": result_text,
                    "segments": segments,
                    "success": True
                }

        except openai.APIError as e:
            return {
                "text": "",
                "segments": [],
                "success": False,
                "error": f"MiniMax API error: {str(e)}"
            }
        except Exception as e:
            return {
                "text": "",
                "segments": [],
                "success": False,
                "error": str(e)
            }

    async def transcribe_stream(self, audio_data: bytes, audio_format: str = "wav") -> Dict:
        """
        流式音频转写（用于实时录音）

        Args:
            audio_data: 音频数据 bytes
            audio_format: 音频格式

        Returns:
            转写结果 dict
        """
        if not OPENAI_SDK_AVAILABLE:
            return {
                "text": "",
                "segments": [],
                "success": False,
                "error": "OpenAI SDK not installed"
            }

        if not self.api_key:
            return {
                "text": "",
                "segments": [],
                "success": False,
                "error": "MINIMAX_API_KEY not configured"
            }

        try:
            import tempfile

            # 将 bytes 写入临时文件
            suffix = f".{audio_format}"
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                tmp.write(audio_data)
                tmp_path = tmp.name

            try:
                # 调用 MiniMax API
                with open(tmp_path, "rb") as audio_file:
                    response = self.client.audio.transcriptions.create(
                        model="speech-01",
                        file=audio_file
                    )

                    return {
                        "text": response.text,
                        "segments": self._parse_to_segments(response.text),
                        "success": True
                    }
            finally:
                # 清理临时文件
                os.unlink(tmp_path)

        except openai.APIError as e:
            return {
                "text": "",
                "segments": [],
                "success": False,
                "error": f"MiniMax API error: {str(e)}"
            }
        except Exception as e:
            return {
                "text": "",
                "segments": [],
                "success": False,
                "error": str(e)
            }

    def _parse_to_segments(self, text: str) -> List[Dict]:
        """
        将转写文本解析为分段格式

        由于 MiniMax API 不返回时间戳，这里根据句子长度做简单分割
        """
        if not text:
            return []

        # 按标点和换行分割
        sentences = []
        current = ""
        for char in text:
            current += char
            if char in '。！？；\n':
                if current.strip():
                    sentences.append(current.strip())
                current = ""

        if current.strip():
            sentences.append(current.strip())

        # 计算每个句子的时间（假设语速 150字/分钟）
        segments = []
        total_chars = len(text)
        time_per_char = 60.0 / 150.0  # 秒/字
        current_time = 0.0

        for sentence in sentences:
            start = current_time
            duration = len(sentence) * time_per_char
            end = current_time + duration

            segments.append({
                "start": round(start, 2),
                "end": round(end, 2),
                "text": sentence
            })

            current_time = end

        return segments

    def get_audio_duration(self, audio_path: str) -> float:
        """
        获取音频文件时长（秒）

        Args:
            audio_path: 音频文件路径

        Returns:
            时长（秒）
        """
        try:
            # 使用 wave 模块读取 wav 文件
            import wave
            with wave.open(audio_path, 'rb') as w:
                frames = w.getnframes()
                rate = w.getframerate()
                duration = frames / float(rate)
                return duration
        except Exception:
            # 对于非 wav 文件，返回估算值
            # 假设 mp3/m4a 码率为 128kbps
            file_size = os.path.getsize(audio_path)
            bitrate = 128 * 1000  # 128kbps
            duration = (file_size * 8) / bitrate
            return duration


# 全局单例
_stt_service: Optional[MiniMaxSTTService] = None


def get_stt_service(
    api_key: Optional[str] = None,
    group_id: Optional[str] = None
) -> MiniMaxSTTService:
    """
    获取 STT 服务单例

    Args:
        api_key: MiniMax API Key
        group_id: MiniMax Group ID

    Returns:
        MiniMaxSTTService 实例
    """
    global _stt_service
    if _stt_service is None:
        _stt_service = MiniMaxSTTService(api_key, group_id)
    return _stt_service


# 便捷函数
async def transcribe(audio_path: str) -> Dict:
    """
    使用 MiniMax ASR 转写音频

    Returns: {"text": "转写文本", "segments": [{"start": 0, "end": 5, "text": "你好"}]}
    """
    service = get_stt_service()
    return await service.transcribe(audio_path)
