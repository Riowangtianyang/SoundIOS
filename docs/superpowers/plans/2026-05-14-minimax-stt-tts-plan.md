# SoundIOS MiniMax STT/TTS 迁移计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 逐任务实现此计划。

**目标：** STT 改用 MiniMax，添加 TTS 功能

**架构：** 
- STT: 使用 MiniMax 语音识别 API 替换腾讯云
- TTS: 新增服务，AI 回复转为语音

**技术栈：** MiniMax API, Python

---

## 文件结构

| 文件 | 操作 | 说明 |
|------|------|------|
| `server/services/stt.py` | 修改 | 腾讯云 → MiniMax |
| `server/services/tts.py` | 新建 | MiniMax TTS 服务 |
| `server/api/chat.py` | 修改 | 添加语音回复选项 |
| `server/.env` | 修改 | 添加 MiniMax API Key |
| `server/.env.example` | 修改 | 添加 TTS 配置说明 |

---

## STT 迁移要点

```python
# MiniMax STT 使用 OpenAI 兼容接口
import openai
client = openai.OpenAI(api_key=os.getenv("MINIMAX_API_KEY"), base_url="https://api.minimax.chat/v1")

# 语音转文字
audio_file = open("recording.m4a", "rb")
transcript = client.audio.transcriptions.create(model="speech-01", file=audio_file)
```

---

## TTS 实现要点

```python
# MiniMax TTS
audio = client.audio.speech.create(
    model="speech-02-hd",
    voice_id="male-qn-qingse",
    input="你好，有什么可以帮你的？"
)
audio_response = BytesIO(audio.content)
```

---

## 验证

```bash
# STT 测试
python -c "from services.stt import get_stt_service; print('STT OK')"

# TTS 测试
python -c "from services.tts import get_tts_service; print('TTS OK')"

# API 测试
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d '{"messages":[{"role":"user","content":"你好"}]}'
```
