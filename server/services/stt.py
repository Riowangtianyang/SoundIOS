"""
腾讯云 ASR 语音转文字服务
基于腾讯云语音识别 API 实现音频转写
"""

import base64
import hashlib
import time
import hmac
import json
import os
from typing import Optional, Dict, List
from pathlib import Path

# 腾讯云 SDK
try:
    from tencentcloud.common import credential
    from tencentcloud.asr.v20190704 import asr_client
    from tencentcloud.common.profile import http_profile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    TENANCENT_SDK_AVAILABLE = True
except ImportError:
    TENANCENT_SDK_AVAILABLE = False
    print("Warning: tencentcloud-sdk not installed. Install with: pip install tencentcloud-sdk-python")


class TencentSTTService:
    """腾讯云语音识别服务"""

    def __init__(
        self,
        secret_id: Optional[str] = None,
        secret_key: Optional[str] = None,
        app_id: Optional[str] = None
    ):
        """
        初始化腾讯云 ASR 服务

        Args:
            secret_id: 腾讯云 SecretId（优先从环境变量获取）
            secret_key: 腾讯云 SecretKey
            app_id: 腾讯云 AppId
        """
        self.secret_id = secret_id or os.getenv("TENCENT_SECRET_ID")
        self.secret_key = secret_key or os.getenv("TENCENT_SECRET_KEY")
        self.app_id = app_id or os.getenv("TENCENT_APP_ID")

        if not self.secret_id or not self.secret_key:
            print("Warning: Tencent credentials not found in environment variables")

        # API 配置
        self.model_type = 16  # 16k 采样率模型
        self.engine_type = "16k_zh"  # 中文16k引擎

    async def transcribe(self, audio_path: str) -> Dict:
        """
        使用腾讯云 ASR 转写音频文件

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
        if not TENANCENT_SDK_AVAILABLE:
            return {
                "text": "",
                "segments": [],
                "success": False,
                "error": "Tencent SDK not installed"
            }

        if not os.path.exists(audio_path):
            return {
                "text": "",
                "segments": [],
                "success": False,
                "error": f"Audio file not found: {audio_path}"
            }

        try:
            # 读取音频文件并转为 base64
            with open(audio_path, 'rb') as f:
                audio_data = f.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')

            # 获取文件扩展名判断格式
            ext = Path(audio_path).suffix.lower()
            format_map = {
                '.wav': 'wav',
                '.mp3': 'mp3',
                '.m4a': 'm4a',
                '.opus': 'opus',
                '.pcm': 'pcm'
            }
            audio_format = format_map.get(ext, 'wav')

            # 创建凭证
            cred_obj = credential.Credential(self.secret_id, self.secret_key)

            # 创建 HTTP profile
            http_profile_obj = http_profile.HttpProfile()
            http_profile_obj.endpoint = "asr.tencentcloudapi.com"

            # 创建客户端
            client_profile = http_profile.ClientProfile()
            client_profile.httpProfile = http_profile_obj
            client = asr_client.AsrClient(cred_obj, "ap-guangzhou", client_profile)

            # 构造请求参数
            req_params = {
                "EngineType": self.engine_type,
                "VoiceFormat": audio_format,
                "Data": audio_base64,
                "DataLen": len(audio_data)
            }

            # 调用 API
            resp = client.SentenceRecognition(req_params)

            # 解析结果
            if resp.Success:
                result_text = resp.Result
                segments = self._parse_to_segments(result_text)

                return {
                    "text": result_text,
                    "segments": segments,
                    "success": True,
                    "confidence": getattr(resp, 'Confidence', 1.0)
                }
            else:
                return {
                    "text": "",
                    "segments": [],
                    "success": False,
                    "error": resp.ErrorMsg if hasattr(resp, 'ErrorMsg') else "Unknown error"
                }

        except TencentCloudSDKException as e:
            return {
                "text": "",
                "segments": [],
                "success": False,
                "error": f"Tencent SDK error: {str(e)}"
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
        if not TENANCENT_SDK_AVAILABLE:
            return {
                "text": "",
                "segments": [],
                "success": False,
                "error": "Tencent SDK not installed"
            }

        try:
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')

            cred_obj = credential.Credential(self.secret_id, self.secret_key)
            http_profile_obj = http_profile.HttpProfile()
            http_profile_obj.endpoint = "asr.tencentcloudapi.com"

            client_profile = http_profile.ClientProfile()
            client_profile.httpProfile = http_profile_obj
            client = asr_client.AsrClient(cred_obj, "ap-guangzhou", client_profile)

            req_params = {
                "EngineType": self.engine_type,
                "VoiceFormat": audio_format,
                "Data": audio_base64,
                "DataLen": len(audio_data)
            }

            resp = client.SentenceRecognition(req_params)

            if resp.Success:
                return {
                    "text": resp.Result,
                    "segments": self._parse_to_segments(resp.Result),
                    "success": True
                }
            else:
                return {
                    "text": "",
                    "segments": [],
                    "success": False,
                    "error": resp.ErrorMsg if hasattr(resp, 'ErrorMsg') else "Unknown error"
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

        由于腾讯云 API 不返回时间戳，这里根据句子长度做简单分割
        实际项目中可以使用腾讯云的 v2 接口获取时间戳
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
_stt_service: Optional[TencentSTTService] = None


def get_stt_service(
    secret_id: Optional[str] = None,
    secret_key: Optional[str] = None,
    app_id: Optional[str] = None
) -> TencentSTTService:
    """
    获取 STT 服务单例

    Args:
        secret_id: 腾讯云 SecretId
        secret_key: 腾讯云 SecretKey
        app_id: 腾讯云 AppId

    Returns:
        TencentSTTService 实例
    """
    global _stt_service
    if _stt_service is None:
        _stt_service = TencentSTTService(secret_id, secret_key, app_id)
    return _stt_service


# 便捷函数
async def transcribe(audio_path: str) -> Dict:
    """
    使用腾讯云 ASR 转写音频

    Returns: {"text": "转写文本", "segments": [{"start": 0, "end": 5, "text": "你好"}]}
    """
    service = get_stt_service()
    return await service.transcribe(audio_path)