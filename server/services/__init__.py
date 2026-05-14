"""
AI Services Package
AI 个人记忆助手的 AI 服务模块

包含：
- stt.py: 腾讯云 ASR 语音转文字服务
- llm.py: MiniMax LLM 对话服务
- analyzer.py: AI 分析引擎
"""

from .stt import TencentSTTService, transcribe, get_stt_service
from .llm import (
    MiniMaxLLMService,
    chat,
    get_llm_service,
    SUMMARY_PROMPT,
    TODO_PROMPT,
    SPEAKER_PROMPT,
    COMMUNICATION_PROMPT
)
from .analyzer import (
    ConversationAnalyzer,
    TodoItem,
    Speaker,
    DiarySummary,
    get_analyzer,
    analyze_conversation
)

__all__ = [
    # STT
    'TencentSTTService',
    'transcribe',
    'get_stt_service',
    # LLM
    'MiniMaxLLMService',
    'chat',
    'get_llm_service',
    'SUMMARY_PROMPT',
    'TODO_PROMPT',
    'SPEAKER_PROMPT',
    'COMMUNICATION_PROMPT',
    # Analyzer
    'ConversationAnalyzer',
    'TodoItem',
    'Speaker',
    'DiarySummary',
    'get_analyzer',
    'analyze_conversation',
]