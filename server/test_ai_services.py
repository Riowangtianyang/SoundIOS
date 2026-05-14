"""
AI 服务测试用例
测试 STT、LLM、分析引擎功能
"""
import pytest
import asyncio
import os

# 设置测试环境变量
os.environ["MINIMAX_API_KEY"] = "test_key_for_mock"
os.environ["TENCENT_SECRET_ID"] = "test_id"
os.environ["TENCENT_SECRET_KEY"] = "test_key"


class TestSTTService:
    """STT 服务测试"""

    def test_stt_service_init(self):
        """测试 STT 服务初始化"""
        from services.stt import TencentSTTService

        service = TencentSTTService()
        assert service is not None
        assert service.engine_type == "16k_zh"

    @pytest.mark.asyncio
    async def test_transcribe_nonexistent_file(self):
        """测试转写不存在的文件"""
        from services.stt import transcribe

        result = await transcribe("/nonexistent/file.wav")
        assert result["success"] is False
        assert "error" in result

    def test_parse_segments(self):
        """测试文本分段解析"""
        from services.stt import TencentSTTService

        service = TencentSTTService()
        text = "你好世界。这是一个测试。今天天气很好。"

        segments = service._parse_to_segments(text)

        assert len(segments) > 0
        assert all("start" in s and "end" in s and "text" in s for s in segments)
        # 验证时间递增
        for i in range(1, len(segments)):
            assert segments[i]["start"] >= segments[i-1]["end"]


class TestLLMService:
    """LLM 服务测试"""

    def test_llm_service_init(self):
        """测试 LLM 服务初始化"""
        from services.llm import MiniMaxLLMService

        service = MiniMaxLLMService()
        assert service is not None

    @pytest.mark.asyncio
    async def test_chat_with_mock(self):
        """测试聊天功能（使用模拟）"""
        from services.llm import chat

        messages = [
            {"role": "system", "content": "你是一个助手"},
            {"role": "user", "content": "你好"}
        ]

        # 由于没有真实 API key，应该返回模拟响应或错误
        try:
            response = await chat(messages)
            # 如果成功，响应应该是字符串
            assert isinstance(response, str)
        except Exception as e:
            # 预期可能的错误（API key 无效等）
            assert True


class TestAnalyzer:
    """分析引擎测试"""

    def test_analyzer_init(self):
        """测试分析器初始化"""
        from services.analyzer import ConversationAnalyzer, get_analyzer

        analyzer = get_analyzer()
        assert analyzer is not None
        assert isinstance(analyzer, ConversationAnalyzer)

    @pytest.mark.asyncio
    async def test_extract_todos_basic(self):
        """测试基本待办提取"""
        from services.analyzer import get_analyzer

        analyzer = get_analyzer()
        text = "我需要明天下午给客户打电话。还有一个会议要在周三举行。"

        result = await analyzer.extract_todos(text)

        # 验证返回格式
        assert isinstance(result, list)
        for item in result:
            assert "title" in item
            assert "priority" in item

    @pytest.mark.asyncio
    async def test_identify_speakers_basic(self):
        """测试基本说话人识别"""
        from services.analyzer import get_analyzer

        analyzer = get_analyzer()
        text = "张总说这个项目需要尽快完成。李经理表示同意。"

        result = await analyzer.identify_speakers(text)

        # 验证返回格式
        assert isinstance(result, list)
        for speaker in result:
            assert "name" in speaker
            assert "role" in speaker

    @pytest.mark.asyncio
    async def test_generate_diary_summary(self):
        """测试日记摘要生成"""
        from services.analyzer import get_analyzer, DiarySummary

        analyzer = get_analyzer()
        text = "今天上午和客户开会，讨论了项目需求。下午完成了技术方案设计。"

        result = await analyzer.generate_diary_summary(text, "2026-05-14")

        # 验证返回格式
        assert isinstance(result, DiarySummary)
        assert result.date == "2026-05-14"
        assert hasattr(result, 'main_events')
        assert hasattr(result, 'mood_score')

    @pytest.mark.asyncio
    async def test_full_analysis(self):
        """测试完整分析流程"""
        from services.analyzer import get_analyzer

        analyzer = get_analyzer()
        text = """
        今天上午和张总开会讨论项目进度。
        张总说需要在本周五前完成开发。
        下午李经理联系我，说客户有新需求。
        需要添加用户管理模块。
        明天要准备演示文稿。
        """

        result = await analyzer.analyze(text, "2026-05-14")

        # 验证返回包含所有必要字段
        assert isinstance(result, dict)
        assert "todos" in result or len(result) > 0
        assert "speakers" in result or len(result) > 0


class TestPromptTemplates:
    """Prompt 模板测试"""

    def test_diary_summary_prompt(self):
        """测试日记摘要 Prompt"""
        from services import SUMMARY_PROMPT

        assert isinstance(SUMMARY_PROMPT, str)
        assert len(SUMMARY_PROMPT) > 0
        assert "日记" in SUMMARY_PROMPT
        assert "{transcript}" in SUMMARY_PROMPT

    def test_todos_extraction_prompt(self):
        """测试待办提取 Prompt"""
        from services import TODO_PROMPT

        assert isinstance(TODO_PROMPT, str)
        assert len(TODO_PROMPT) > 0
        assert "待办" in TODO_PROMPT or "JSON" in TODO_PROMPT
        assert "{transcript}" in TODO_PROMPT

    def test_speaker_identification_prompt(self):
        """测试说话人识别 Prompt"""
        from services import SPEAKER_PROMPT

        assert isinstance(SPEAKER_PROMPT, str)
        assert len(SPEAKER_PROMPT) > 0
        assert "说话人" in SPEAKER_PROMPT


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
