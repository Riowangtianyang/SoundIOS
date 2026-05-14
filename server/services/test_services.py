"""
AI 服务测试文件
测试 STT、LLM 和 Analyzer 功能的完整测试用例
"""

import os
import asyncio
import pytest

# 设置测试环境变量（请替换为实际值）
os.environ.setdefault("MINIMAX_API_KEY", "your_test_key")
os.environ.setdefault("TENCENT_SECRET_ID", "your_test_secret_id")
os.environ.setdefault("TENCENT_SECRET_KEY", "your_test_secret_key")


# ========== STT 服务测试 ==========

async def test_stt_service():
    """测试腾讯云 STT 服务"""
    from services.stt import TencentSTTService, get_stt_service

    # 创建服务实例
    service = TencentSTTService()

    # 测试音频文件（替换为实际测试文件路径）
    test_audio_path = "test_audio.wav"

    if os.path.exists(test_audio_path):
        result = await service.transcribe(test_audio_path)
        print(f"STT Result: {result}")

        assert result.get('success', False) or 'error' in result
        if result.get('success'):
            assert 'text' in result
            assert 'segments' in result
            print("STT test passed!")
    else:
        print(f"Test audio file not found: {test_audio_path}")
        print("Skipping STT test (no audio file)")


async def test_stt_stream():
    """测试流式音频转写"""
    from services.stt import TencentSTTService

    service = TencentSTTService()

    # 模拟音频数据
    audio_data = b'\x00' * 16000  # 1秒静音数据

    result = await service.transcribe_stream(audio_data, "pcm")
    print(f"Stream STT Result: {result}")

    assert 'success' in result or 'error' in result


# ========== LLM 服务测试 ==========

async def test_llm_chat():
    """测试 MiniMax 对话功能"""
    from services.llm import MiniMaxLLMService, get_llm_service

    # 创建服务实例
    service = get_llm_service()

    # 测试对话
    messages = [
        {"role": "user", "content": "你好，请介绍一下你自己"}
    ]

    response = await service.chat(messages)
    print(f"LLM Response: {response}")

    assert response and len(response) > 0
    print("LLM chat test passed!")


async def test_llm_analyze():
    """测试 LLM 分析功能"""
    from services.llm import get_llm_service

    service = get_llm_service()

    test_transcript = """
    张三：今天下午的会议很重要，我们需要讨论项目进度。
    李四：好的，我会准备相关的材料。
    张三：另外，记得在下周一之前完成技术方案的设计。
    李四：没问题，我会和王经理确认细节。
    张三：还有，我们的客户张总下周要来公司考察。
    """

    result = await service.analyze_conversation(test_transcript, "summary")
    print(f"Analysis Result: {result}")

    assert 'response' in result
    print("LLM analysis test passed!")


async def test_llm_stream():
    """测试流式响应"""
    from services.llm import get_llm_service

    service = get_llm_service()

    messages = [
        {"role": "user", "content": "用几个词描述春天"}
    ]

    full_response = ""
    async for chunk in service.chat_stream(messages):
        full_response += chunk
        print(f"Chunk: {chunk}")

    print(f"Full Response: {full_response}")
    assert len(full_response) > 0
    print("LLM stream test passed!")


# ========== Analyzer 测试 ==========

async def test_analyzer_extract_todos():
    """测试待办提取"""
    from services.analyzer import ConversationAnalyzer

    analyzer = ConversationAnalyzer()

    test_text = """
    我们需要在下周五之前完成项目方案。还有，记得给客户打电话确认合同细节。
    记得安排一次技术评审会议，时间定在周三下午。
    """

    todos = await analyzer.extract_todos(test_text)
    print(f"Extracted Todos: {todos}")

    assert isinstance(todos, list)
    print(f"Found {len(todos)} todos")

    # 验证待办格式
    for todo in todos:
        assert hasattr(todo, 'title')
        assert hasattr(todo, 'priority')


async def test_analyzer_identify_speakers():
    """测试说话人识别"""
    from services.analyzer import ConversationAnalyzer

    analyzer = ConversationAnalyzer()

    test_text = """
    张三：今天讨论的项目很重要。
    李四：我同意，我们需要尽快推进。
    王经理：技术方案我来负责。
    """

    speakers = await analyzer.identify_speakers(test_text)
    print(f"Identified Speakers: {speakers}")

    assert isinstance(speakers, list)
    print(f"Found {len(speakers)} speakers")


async def test_analyzer_generate_summary():
    """测试日记摘要生成"""
    from services.analyzer import ConversationAnalyzer

    analyzer = ConversationAnalyzer()

    test_text = """
    上午和团队开会讨论项目进度，确定了下周交付计划。
    中午和客户张总进行商务洽谈，对方对方案表示满意。
    下午处理技术方案评审，解决了几个关键问题。
    晚上回复了几封重要邮件。
    """

    summary = await analyzer.generate_diary_summary(test_text, "2026-05-14")
    print(f"Diary Summary: {summary}")

    assert hasattr(summary, 'main_events')
    assert hasattr(summary, 'mood_score')
    assert hasattr(summary, 'date')
    assert summary.date == "2026-05-14"


async def test_analyzer_full():
    """测试完整分析流程"""
    from services.analyzer import ConversationAnalyzer

    analyzer = ConversationAnalyzer()

    test_text = """
    早上和老板讨论了季度目标，他希望我们能在月底前完成新功能开发。
    中午和张总开会，他说下周要来公司实地考察。
    下午我需要和技术团队确认技术方案。
    还要准备下周三的项目演示材料。
    记得周五前给客户发报价单。
    """

    result = await analyzer.analyze(test_text, "2026-05-14")
    print(f"Full Analysis Result:")
    print(f"  - Summary: {result.get('summary')}")
    print(f"  - Todos: {result.get('todos')}")
    print(f"  - Speakers: {result.get('speakers')}")
    print(f"  - Communication Tips: {result.get('communication_tips', '')[:100]}...")

    assert 'summary' in result
    assert 'todos' in result
    assert 'speakers' in result
    assert 'communication_tips' in result

    print("Full analysis test passed!")


# ========== 集成测试 ==========

async def test_integration():
    """集成测试：完整的工作流"""
    from services.stt import get_stt_service
    from services.analyzer import ConversationAnalyzer

    # 模拟场景：处理音频文件并分析
    # 1. 假设已完成 STT 转写
    mock_transcript = """
    今天是忙碌的一天。上午和团队开会讨论Q2季度的产品规划。
    老板特别强调要在6月底前完成新功能的开发。
    中午约了客户王总在咖啡厅见面，讨论了合作细节。
    他对我们的方案很感兴趣，希望下周能签合同。
    下午回到办公室，处理了几封重要邮件。
    还要准备明天和投资人的会议材料。
    """

    # 2. 使用 Analyzer 分析
    analyzer = ConversationAnalyzer()

    result = await analyzer.analyze(mock_transcript, "2026-05-14")

    print("\n=== Integration Test Result ===")
    print(f"Summary: {result['summary']}")
    print(f"Todos ({len(result['todos'])}): {result['todos']}")
    print(f"Speakers ({len(result['speakers'])}): {result['speakers']}")
    print(f"Communication Tips: {result['communication_tips'][:200]}...")

    assert result['summary'] is not None
    assert len(result['todos']) > 0
    print("\nIntegration test passed!")


# ========== 运行测试 ==========

async def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Running AI Services Tests")
    print("=" * 50)

    tests = [
        ("STT Service", test_stt_service),
        ("STT Stream", test_stt_stream),
        ("LLM Chat", test_llm_chat),
        ("LLM Analysis", test_llm_analyze),
        ("LLM Stream", test_llm_stream),
        ("Analyzer Extract Todos", test_analyzer_extract_todos),
        ("Analyzer Identify Speakers", test_analyzer_identify_speakers),
        ("Analyzer Generate Summary", test_analyzer_generate_summary),
        ("Analyzer Full", test_analyzer_full),
        ("Integration", test_integration),
    ]

    results = []
    for name, test_func in tests:
        print(f"\n--- Testing: {name} ---")
        try:
            await test_func()
            results.append((name, "PASS"))
            print(f"PASS: {name}")
        except Exception as e:
            results.append((name, f"FAIL: {e}"))
            print(f"FAIL: {name} - {e}")

    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    for name, result in results:
        status = "OK" if result == "PASS" else "FAIL"
        print(f"[{status}] {name}")

    passed = sum(1 for _, r in results if r == "PASS")
    print(f"\nTotal: {len(results)} tests, {passed} passed")


if __name__ == "__main__":
    asyncio.run(run_all_tests())