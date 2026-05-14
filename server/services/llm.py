"""
MiniMax LLM 服务集成
基于 MiniMax Chat Completion API 实现 AI 对话和分析功能
"""

import os
import json
import asyncio
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class MiniMaxModel(Enum):
    """MiniMax 支持的模型"""
    ABAB5_5_CHAT = "abab5.5-chat"
    ABAB5_CHAT = "abab5-chat"
    ABAB6_CHAT = "abab6-chat"


@dataclass
class Message:
    """对话消息"""
    role: str  # system, user, assistant
    content: str


class MiniMaxLLMService:
    """MiniMax LLM 服务类"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.minimax.chat/v1/text/chatcompletion_v2",
        model: str = "abab5.5-chat",
        timeout: int = 60
    ):
        """
        初始化 MiniMax LLM 服务

        Args:
            api_key: MiniMax API Key（优先从环境变量获取）
            base_url: API 地址
            model: 模型名称
            timeout: 请求超时时间（秒）
        """
        self.api_key = api_key or os.getenv("MINIMAX_API_KEY")
        self.base_url = base_url
        self.model = model
        self.timeout = timeout

        if not self.api_key:
            print("Warning: MINIMAX_API_KEY not found in environment variables")

    async def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """
        调用 MiniMax LLM 进行对话

        Args:
            messages: 消息列表 [{"role": "user", "content": "..."}]
            system_prompt: 系统提示词
            temperature: 温度参数（0-1，越高越随机）
            max_tokens: 最大生成 token 数

        Returns:
            AI 回复文本
        """
        if not self.api_key:
            return self._get_demo_response(messages)

        try:
            import aiohttp

            # 构造完整的消息列表
            full_messages = []
            if system_prompt:
                full_messages.append({"role": "system", "content": system_prompt})
            full_messages.extend(messages)

            # 构造请求体
            payload = {
                "model": self.model,
                "messages": full_messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            # 发送请求
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }

                async with session.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return self._parse_response(result)
                    else:
                        error_text = await response.text()
                        raise Exception(f"MiniMax API error: {response.status} - {error_text}")

        except asyncio.TimeoutError:
            raise Exception("MiniMax API request timeout")
        except Exception as e:
            raise Exception(f"MiniMax API error: {str(e)}")

    async def chat_stream(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2048
    ):
        """
        流式调用 MiniMax LLM

        Args:
            messages: 消息列表
            system_prompt: 系统提示词
            temperature: 温度参数
            max_tokens: 最大 token 数

        Yields:
            逐步返回的文本片段
        """
        if not self.api_key:
            # 返回示例
            yield "【演示模式】"
            yield "API Key 未配置，返回模拟响应。"
            return

        try:
            import aiohttp

            full_messages = []
            if system_prompt:
                full_messages.append({"role": "system", "content": system_prompt})
            full_messages.extend(messages)

            payload = {
                "model": self.model,
                "messages": full_messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True
            }

            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }

                async with session.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"MiniMax API error: {response.status}")

                    # 处理流式响应
                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        if not line:
                            continue

                        # SSE 格式处理
                        if line.startswith('data:'):
                            data_str = line[5:].strip()
                            if data_str == '[DONE]':
                                break

                            try:
                                data = json.loads(data_str)
                                delta = data.get('choices', [{}])[0].get('delta', {})
                                content = delta.get('content', '')
                                if content:
                                    yield content
                            except json.JSONDecodeError:
                                continue

        except Exception as e:
            yield f"Error: {str(e)}"

    def _parse_response(self, result: Dict) -> str:
        """解析 API 响应"""
        try:
            choices = result.get('choices', [])
            if choices:
                return choices[0].get('message', {}).get('content', '')
            return ""
        except Exception:
            return str(result)

    def _get_demo_response(self, messages: List[Dict]) -> str:
        """获取演示响应（当 API Key 未配置时）"""
        last_message = messages[-1] if messages else {}
        content = last_message.get('content', '')

        # 简单演示
        if '摘要' in content or 'summary' in content.lower():
            return """【演示模式 - 日记摘要】
1. 今日主要事件：
   - 上午与团队开会讨论项目进度
   - 中午与客户张总进行商务洽谈
   - 下午处理技术方案评审

2. 今日状态评价：8分（高效完成多项任务）

3. 重要收获：
   - 项目方案获得客户认可
   - 确定了下周交付计划

4. 需要跟进：
   - 准备项目演示材料
   - 联系王经理确认细节"""

        elif '待办' in content or 'todo' in content.lower():
            return """[
  {"title": "准备项目演示材料", "description": "完成PPT制作，包含技术方案和案例展示", "due_date": "2026-05-20", "priority": 2},
  {"title": "联系王经理", "description": "确认项目交付细节和时间安排", "due_date": "2026-05-15", "priority": 1},
  {"title": "跟进客户反馈", "description": "整理张总的反馈意见并制定改进方案", "due_date": "2026-05-18", "priority": 2}
]"""

        elif '说话人' in content or 'speaker' in content.lower():
            return """- 说话人1（张三）：项目经理，负责项目整体推进
- 说话人2（李四）：技术负责人，负责技术方案
- 说话人3（张总）：客户方决策者"""

        elif '沟通' in content or 'communication' in content.lower():
            return """【沟通建议】

1. 沟通效果好的地方：
   - 项目讨论时条理清晰
   - 能够有效倾听对方意见
   - 关键信息确认及时

2. 需要改进的地方：
   - 部分技术细节解释不够通俗
   - 会议时间控制可以更精准

3. 针对各方的建议：
   - 对团队：可以增加互动讨论环节
   - 对客户：注意用业务语言而非纯技术语言"""

        else:
            return f"【演示模式】已收到消息：{content[:50]}..."

    async def analyze_conversation(
        self,
        transcript: str,
        analysis_type: str = "full"
    ) -> Dict[str, Any]:
        """
        分析对话内容

        Args:
            transcript: 对话转写文本
            analysis_type: 分析类型（full/summary/todos/speakers）

        Returns:
            分析结果
        """
        prompts = {
            "summary": SUMMARY_PROMPT,
            "todos": TODO_PROMPT,
            "speakers": SPEAKER_PROMPT,
            "communication": COMMUNICATION_PROMPT,
            "full": FULL_ANALYSIS_PROMPT
        }

        prompt = prompts.get(analysis_type, prompts["full"])
        prompt = prompt.format(transcript=transcript)

        response = await self.chat([
            {"role": "user", "content": prompt}
        ])

        return {
            "analysis_type": analysis_type,
            "response": response,
            "transcript": transcript
        }


# Prompt 模板定义
SUMMARY_PROMPT = """你是一个个人日记助手。用户给你一天的对话记录，请生成：
1. 今日主要事件（3-5条）
2. 今日状态评价（1-10分）
3. 重要收获或决定
4. 需要跟进的事项

对话记录：
{transcript}

请按以下格式输出：
## 日记摘要

### 今日主要事件
1. ...
2. ...
3. ...

### 状态评价
X分（简短评价）

### 重要收获
...

### 待跟进事项
- ...
- ..."""

TODO_PROMPT = """从以下对话中提取所有待办事项，格式为 JSON 数组：
[{{"title": "任务标题", "description": "任务描述", "due_date": "截止日期（如有）", "priority": 1-3}}]

规则：
- 只提取明确的行动项（包含动词的任务）
- 不要提取已完成的事项
- 如果提到截止日期，务必记录
- 优先级：1=高，2=中，3=低

对话：
{transcript}

只输出 JSON 数组，不要包含其他内容。"""

SPEAKER_PROMPT = """分析以下对话，识别所有说话人及其角色。

规则：
- 如果有名字，使用名字
- 如果有角色（如"客户"、"老板"），使用角色
- 如果无法确定，使用"说话人1"、"说话人2"
- 简要描述每个人的发言内容特点

对话：
{transcript}

请按以下格式输出：
## 说话人识别

### 说话人列表
1. [姓名/角色]：发言特点描述
2. ...

### 人物关系
- ... (如果有明确关系的话)"""

COMMUNICATION_PROMPT = """基于今天的对话，给出沟通改进建议。

请分析：
1. 哪些地方沟通效果好（具体举例）
2. 哪些地方可以改进
3. 针对各个对话对象的沟通建议

对话：
{transcript}

请按以下格式输出：
## 沟通建议

### 做得好
- ...

### 可改进
- ...

### 针对建议
- [说话人名]：... """

FULL_ANALYSIS_PROMPT = """你是一个专业的个人助理。请分析以下对话内容，生成完整的分析报告。

对话：
{transcript}

请生成以下内容：
1. 日记摘要
2. 待办事项列表（JSON格式）
3. 说话人识别
4. 沟通建议

确保输出完整、专业的分析报告。"""


# 全局单例
_llm_service: Optional[MiniMaxLLMService] = None


def get_llm_service(
    api_key: Optional[str] = None,
    model: str = "abab5.5-chat"
) -> MiniMaxLLMService:
    """
    获取 LLM 服务单例

    Args:
        api_key: MiniMax API Key
        model: 模型名称

    Returns:
        MiniMaxLLMService 实例
    """
    global _llm_service
    if _llm_service is None:
        _llm_service = MiniMaxLLMService(api_key, model=model)
    return _llm_service


# 便捷函数
async def chat(messages: List[Dict], system_prompt: str = "") -> str:
    """
    调用 MiniMax LLM

    Args:
        messages: [{"role": "user", "content": "..."}]
        system_prompt: 系统提示词

    Returns:
        AI 回复文本
    """
    service = get_llm_service()
    return await service.chat(messages, system_prompt)