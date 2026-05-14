#!/usr/bin/env python3
"""快速安装依赖并运行测试"""
import subprocess
import sys

# 安装 aiohttp
print("安装 aiohttp...")
subprocess.run([sys.executable, "-m", "pip", "install", "aiohttp", "--break-system-packages", "-q"])

# 运行测试
print("\n运行 AI 服务测试...")
result = subprocess.run([sys.executable, "-m", "pytest", "test_ai_services.py", "-v", "--tb=line", "-p", "no:cacheprovider"], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(result.stderr)