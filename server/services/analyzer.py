"""
AI 分析引擎 - 对话内容分析与提取
整合 STT 和 LLM 服务，实现日记摘要、待办提取等功能
"""

import json
import re
from typing import Dict, List, Optional, Any
from datetime import datetime, date
from dataclasses import dataclass, asdict

from .llm import (
    chat as llm_chat,
    get_llm_service,
    SUMMARY_PROMPT,
    TODO_PROMPT,
    SPEAKER_PROMPT,
    COMMUNICATION_PROMPT
)


@dataclass
class TodoItem:
    """待办事项"""
    title: str
    description: str
    due_date: Optional[str] = None
    priority: int = 2  # 1=高, 2=中, 3=低
    completed: bool = False
    source: str = ""  # 来源于哪个对话


@dataclass
class Speaker:
    """说话人"""
    name: str
    role: str = ""
    characteristics: str = ""
    conversations_count: int = 0


@dataclass
class DiarySummary:
    """日记摘要"""
    date: str
    main_events: List[str]
    mood_score: int  # 1-10
    mood_comment: str
    key_decisions: List[str]
    follow_ups: List[str]
    raw_analysis: str = ""


class ConversationAnalyzer:
    """对话分析器"""

    def __init__(self, llm_service=None):
        """
        初始化分析器

        Args:
            llm_service: LLM 服务实例（可选）
        """
        self.llm_service = llm_service

    async def analyze(
        self,
        transcript_text: str,
        date_str: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        综合分析对话文本

        Args:
            transcript_text: 转写文本
            date_str: 日期字符串（格式：YYYY-MM-DD）

        Returns:
            {
                "summary": DiarySummary,
                "todos": List[TodoItem],
                "speakers": List[Speaker],
                "communication_tips": str
            }
        """
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        # 并行执行多个分析任务
        tasks = [
            self.generate_diary_summary(transcript_text, date_str),
            self.extract_todos(transcript_text),
            self.identify_speakers(transcript_text),
            self.get_communication_suggestions(transcript_text)
        ]

        results = await self._run_parallel(tasks)

        return {
            "summary": results[0] if len(results) > 0 and not isinstance(results[0], Exception) else None,
            "todos": results[1] if len(results) > 1 and not isinstance(results[1], Exception) else [],
            "speakers": results[2] if len(results) > 2 and not isinstance(results[2], Exception) else [],
            "communication_tips": results[3] if len(results) > 3 and not isinstance(results[3], Exception) else ""
        }

    async def _run_parallel(self, tasks: List) -> List:
        """并行执行多个异步任务"""
        import asyncio
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def extract_todos(self, text: str) -> List[TodoItem]:
        """
        提取待办事项

        Args:
            text: 转写文本

        Returns:
            待办事项列表
        """
        if not text or len(text.strip()) < 10:
            return []

        prompt = TODO_PROMPT.format(transcript=text)

        try:
            response = await self._call_llm(prompt)

            # 解析 JSON
            todos = self._parse_todos_json(response)
            return todos

        except Exception as e:
            print(f"Extract todos error: {e}")
            # 使用规则提取作为 fallback
            return self._extract_todos_by_rules(text)

    def _parse_todos_json(self, response: str) -> List[TodoItem]:
        """解析 LLM 返回的 JSON"""
        try:
            # 提取 JSON 部分
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                todos = []
                for item in data:
                    todo = TodoItem(
                        title=item.get('title', ''),
                        description=item.get('description', ''),
                        due_date=item.get('due_date'),
                        priority=item.get('priority', 2),
                        source="llm_analysis"
                    )
                    todos.append(todo)
                return todos
        except json.JSONDecodeError:
            pass

        return []

    def _extract_todos_by_rules(self, text: str) -> List[TodoItem]:
        """使用规则提取待办（备用方法）"""
        todos = []

        # 关键词模式
        patterns = [
            r'(要|需要|必须|应该)\s+(.{2,30}?)',
            r'安排\s+(.{2,30}?)',
            r'记得\s+(.{2,30}?)',
            r'提醒我\s+(.{2,30}?)',
            r'(完成|做完|做好)\s+(.{2,30}?)',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                title = match.group(1).strip() if match.lastindex else match.group(0).strip()
                if len(title) > 3 and title not in [t.title for t in todos]:
                    todos.append(TodoItem(
                        title=title,
                        description=f"从对话中提取：{match.group(0)}",
                        priority=2
                    ))

        return todos[:10]  # 限制数量

    async def identify_speakers(self, text: str) -> List[Speaker]:
        """
        识别说话人

        Args:
            text: 转写文本

        Returns:
            说话人列表
        """
        if not text or len(text.strip()) < 10:
            return []

        prompt = SPEAKER_PROMPT.format(transcript=text)

        try:
            response = await self._call_llm(prompt)

            # 解析说话人
            speakers = self._parse_speakers(response, text)
            return speakers

        except Exception as e:
            print(f"Identify speakers error: {e}")
            return []

    def _parse_speakers(self, response: str, text: str) -> List[Speaker]:
        """解析 LLM 返回的说话人信息"""
        speakers = []

        # 尝试解析结构化响应
        lines = response.split('\n')
        current_speaker = None

        for line in lines:
            # 检查是否是新说话人
            name_match = re.match(r'\d+[\.\、\s]+（(.+?)）', line)
            if name_match:
                name = name_match.group(1)
                current_speaker = Speaker(
                    name=name,
                    characteristics=line.split('：')[1] if '：' in line else ''
                )
                speakers.append(current_speaker)

        # 如果解析失败，尝试简单识别
        if not speakers:
            # 检查是否有明显的名字
            name_patterns = [
                r'([A-Z][a-z]{1,10})\s*[:：]',
                r'对\s+([A-Z][a-z]{1,10})',
                r'和\s+([A-Z][a-z]{1,10})'
            ]

            names_found = set()
            for pattern in name_patterns:
                matches = re.findall(pattern, text)
                names_found.update(matches)

            for name in list(names_found)[:5]:
                speakers.append(Speaker(name=name))

        return speakers

    async def generate_diary_summary(
        self,
        text: str,
        date_str: str
    ) -> DiarySummary:
        """
        生成日记摘要

        Args:
            text: 转写文本
            date_str: 日期

        Returns:
            DiarySummary 对象
        """
        if not text or len(text.strip()) < 10:
            return DiarySummary(
                date=date_str,
                main_events=["今日无有效对话记录"],
                mood_score=5,
                mood_comment="数据不足",
                key_decisions=[],
                follow_ups=[]
            )

        prompt = SUMMARY_PROMPT.format(transcript=text)

        try:
            response = await self._call_llm(prompt)

            # 解析响应
            summary = self._parse_summary_response(response, date_str)
            summary.raw_analysis = response
            return summary

        except Exception as e:
            print(f"Generate summary error: {e}")
            return DiarySummary(
                date=date_str,
                main_events=["生成摘要失败"],
                mood_score=5,
                mood_comment="分析出错",
                key_decisions=[],
                follow_ups=[]
            )

    def _parse_summary_response(self, response: str, date_str: str) -> DiarySummary:
        """解析 LLM 返回的日记摘要"""
        main_events = []
        mood_score = 5
        mood_comment = ""
        key_decisions = []
        follow_ups = []

        lines = response.split('\n')

        current_section = None
        for line in lines:
            line = line.strip()

            if '主要事件' in line or '## 日记' in line:
                current_section = 'events'
            elif '状态评价' in line or '评分' in line or 'Mood' in line:
                current_section = 'mood'
            elif '重要收获' in line or '收获' in line or '决定' in line:
                current_section = 'decisions'
            elif '待跟进' in line or '跟进' in line or '待办' in line:
                current_section = 'followups'

            if current_section == 'events' and line and line[0].isdigit():
                main_events.append(line)
            elif current_section == 'mood' and line:
                # 提取评分
                score_match = re.search(r'(\d+)', line)
                if score_match:
                    mood_score = min(10, max(1, int(score_match.group(1))))
                mood_comment = line
            elif current_section == 'decisions' and line and not line.startswith('#'):
                key_decisions.append(line)
            elif current_section == 'followups' and line and not line.startswith('#'):
                follow_ups.append(line)

        return DiarySummary(
            date=date_str,
            main_events=main_events or ["今日对话记录已分析"],
            mood_score=mood_score,
            mood_comment=mood_comment,
            key_decisions=key_decisions,
            follow_ups=follow_ups,
            raw_analysis=response
        )

    async def get_communication_suggestions(self, text: str) -> str:
        """
        获取沟通建议

        Args:
            text: 转写文本

        Returns:
            沟通建议文本
        """
        if not text or len(text.strip()) < 10:
            return "对话数据不足，无法提供建议。"

        prompt = COMMUNICATION_PROMPT.format(transcript=text)

        try:
            response = await self._call_llm(prompt)
            return response
        except Exception as e:
            print(f"Communication suggestions error: {e}")
            return "无法生成沟通建议。"

    async def _call_llm(self, prompt: str) -> str:
        """调用 LLM 服务"""
        if self.llm_service:
            return await self.llm_service.chat([
                {"role": "user", "content": prompt}
            ])
        else:
            service = get_llm_service()
            return await service.chat([{"role": "user", "content": prompt}])


# 全局单例
_analyzer: Optional[ConversationAnalyzer] = None


def get_analyzer() -> ConversationAnalyzer:
    """获取分析器单例"""
    global _analyzer
    if _analyzer is None:
        _analyzer = ConversationAnalyzer()
    return _analyzer


# 便捷函数
async def analyze_conversation(
    transcript_text: str,
    date_str: Optional[str] = None
) -> Dict[str, Any]:
    """便捷函数：分析对话"""
    analyzer = get_analyzer()
    return await analyzer.analyze(transcript_text, date_str)