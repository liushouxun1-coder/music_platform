"""
diagnostic.py - 检查 DeepSeek API 配置
运行此脚本诊断 API Key 设置问题
"""
import os
import sys

print("=" * 60)
print("🔍 DeepSeek API 配置诊断")
print("=" * 60)

# 1. 检查环境变量
api_key = os.environ.get("DEEPSEEK_API_KEY")
print(f"\n1. 环境变量 DEEPSEEK_API_KEY:")
if api_key:
    print(f"   ✅ 已设置: {api_key[:10]}...{api_key[-4:]}")
else:
    print(f"   ❌ 未设置")

# 2. 检查 .env 文件
print(f"\n2. 检查 .env 文件:")
if os.path.exists(".env"):
    print(f"   ✅ 找到 .env 文件")
    with open(".env", "r", encoding="utf-8") as f:
        content = f.read()
        if "DEEPSEEK_API_KEY" in content:
            for line in content.split("\n"):
                if "DEEPSEEK_API_KEY" in line and not line.startswith("#"):
                    key = line.split("=")[1].strip().strip('"').strip("'")
                    print(f"   ✅ 包含 API Key: {key[:10]}...{key[-4:]}")
        else:
            print(f"   ❌ .env 文件中未找到 DEEPSEEK_API_KEY")
else:
    print(f"   ❌ 未找到 .env 文件")

# 3. 测试 API 连接
print(f"\n3. 测试 API 连接:")
if api_key:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        # 发送一个简单请求测试
        response = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print(f"   ✅ API 连接成功！")
        print(f"   📊 模型: {response.model}")
        print(f"   💰 消耗 tokens: {response.usage.total_tokens}")
    except ImportError:
        print(f"   ❌ 未安装 openai SDK，运行: pip install openai")
    except Exception as e:
        print(f"   ❌ API 连接失败: {e}")
else:
    print(f"   ⏭️ 跳过（无 API Key）")

print(f"\n" + "=" * 60)
print("💡 解决方案:")
print("=" * 60)
print("""
方式1 - 环境变量（推荐）:
    Windows CMD:     set DEEPSEEK_API_KEY=sk-xxxxxxxx
    Windows Power:   $env:DEEPSEEK_API_KEY="sk-xxxxxxxx"
    Mac/Linux:       export DEEPSEEK_API_KEY=sk-xxxxxxxx

方式2 - .env 文件（项目级）:
    1. 在项目根目录创建 .env 文件
    2. 写入: DEEPSEEK_API_KEY=sk-xxxxxxxx
    3. 安装: pip install python-dotenv
    4. 在 app.py 顶部添加:
       from dotenv import load_dotenv
       load_dotenv()

方式3 - 硬编码（仅测试，不安全）:
    在 music_logic.py 中修改:
    self.llm = LLMEngineFactory.create_engine(
        api_key="sk-xxxxxxxx"
    )
""")
