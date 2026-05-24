"""
llm_engine.py - LLM 引擎层
单一职责：只负责 LLM 调用，不读取 .env（由工厂统一管理）
"""
import random
from typing import List, Dict, Optional, Generator
from dataclasses import dataclass
from abc import ABC, abstractmethod

# 尝试导入 openai
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


@dataclass
class LLMResponse:
    """LLM 响应结构"""
    content: str
    reasoning: str = ""
    confidence: float = 0.9
    sources: List[str] = None

    def __post_init__(self):
        if self.sources is None:
            self.sources = []


class BaseLLMEngine(ABC):
    """LLM 引擎抽象基类"""

    @abstractmethod
    def recommend_by_mood(self, mood: str, songs: List[Dict]) -> LLMResponse:
        pass

    @abstractmethod
    def recommend_by_scene(self, scene: str, songs: List[Dict]) -> LLMResponse:
        pass

    @abstractmethod
    def generate_playlist_insight(self, songs: List[Dict]) -> LLMResponse:
        pass

    @abstractmethod
    def answer_knowledge_question(self, question: str, knowledge: Optional[Dict] = None) -> LLMResponse:
        pass


class DeepSeekEngine(BaseLLMEngine):
    """DeepSeek 真实 API 引擎 —— 纯调用，不读配置"""

    def __init__(self, api_key: str, model: str = "deepseek-v4-pro"):
        if OpenAI is None:
            raise ImportError("请先安装 openai SDK: pip install openai")
        if not api_key:
            raise ValueError("api_key 不能为空")

        self.model = model
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def _call_api(self, system_prompt: str, user_prompt: str, enable_thinking: bool = True) -> LLMResponse:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        try:
            kwargs = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "max_tokens": 4096
            }
            if enable_thinking and self.model == "deepseek-v4-pro":
                kwargs["extra_body"] = {"thinking": {"type": "enabled"}}
                kwargs["reasoning_effort"] = "high"

            response = self.client.chat.completions.create(**kwargs)
            message = response.choices[0].message
            content = message.content or ""
            reasoning = getattr(message, "reasoning_content", "") or "基于DeepSeek模型生成"

            return LLMResponse(content=content, reasoning=reasoning, confidence=0.92)

        except Exception as e:
            return LLMResponse(
                content=f"AI 服务暂时不可用：{str(e)}",
                reasoning="API调用失败",
                confidence=0.0
            )

    def recommend_by_mood(self, mood: str, songs: List[Dict]) -> LLMResponse:
        songs_info = "\n".join([
            f"{i+1}. 《{s['title']}》- {s['artist']} | 流派：{s['genre'][0]} | BPM：{s['tempo']} | 能量值：{s['energy']:.2f} | 描述：{s['description']}"
            for i, s in enumerate(songs[:6])
        ])

        user_prompt = f"""用户想要"{mood}"情绪的音乐。\n\n可用歌曲：\n{songs_info}\n\n请生成：1. 为什么这类音乐适合该情绪 2. 每首歌曲点评 3. 播放顺序建议"""

        return self._call_api(
            system_prompt="你是一位专业的音乐推荐师和音乐心理学家。用温暖专业的中文回答，适当使用emoji。",
            user_prompt=user_prompt,
            enable_thinking=True
        )

    def recommend_by_scene(self, scene: str, songs: List[Dict]) -> LLMResponse:
        songs_info = "\n".join([
            f"{i+1}. 《{s['title']}》- {s['artist']} | 流派：{s['genre'][0]} | BPM：{s['tempo']} | 能量值：{s['energy']:.2f}"
            for i, s in enumerate(songs[:6])
        ])

        user_prompt = f"""用户正在"{scene}"场景，需要匹配的音乐。\n\n可用歌曲：\n{songs_info}\n\n请生成场景适配分析和歌曲点评。"""

        return self._call_api(
            system_prompt="你是一位专业的音乐推荐师。用实用亲切的中文回答。",
            user_prompt=user_prompt,
            enable_thinking=True
        )

    def generate_playlist_insight(self, songs: List[Dict]) -> LLMResponse:
        songs_info = "\n".join([
            f"{i+1}. 《{s['title']}》- {s['artist']} | 情绪：{', '.join(s['mood'])} | BPM：{s['tempo']} | 能量：{s['energy']:.2f}"
            for i, s in enumerate(songs)
        ])

        user_prompt = f"""请为以下播放列表生成洞察：\n\n{songs_info}\n\n生成诗意描述、数据洞察和聆听建议。"""

        return self._call_api(
            system_prompt="你是一位音乐评论家。用富有文学性的中文回答。",
            user_prompt=user_prompt,
            enable_thinking=False
        )

    def answer_knowledge_question(self, question: str, knowledge: Optional[Dict] = None) -> LLMResponse:
        context = ""
        if knowledge:
            context = f"\n相关知识：{knowledge['answer']}\n分类：{knowledge['category']}"

        user_prompt = f"""用户问题：{question}{context}\n\n请深入浅出地回答，举例说明。"""

        return self._call_api(
            system_prompt="你是一位资深音乐学者。用通俗易懂但专业准确的中文回答。",
            user_prompt=user_prompt,
            enable_thinking=True
        )

    def stream_response(self, text: str) -> Generator[str, None, None]:
        words = text.split()
        for i in range(0, len(words), 3):
            yield " ".join(words[i:i+3]) + " "


class MockLLMEngine(BaseLLMEngine):
    """模拟 LLM 引擎（无需 API Key）"""

    def __init__(self):
        self._mood_templates = {
            "欢快": ["基于您对{mood}音乐的需求，我为您精选了节奏明快、旋律上扬的歌曲。", "为您推荐{mood}风格音乐：这类音乐往往具有跳跃的节奏型。"],
            "悲伤": ["理解您需要{mood}的音乐陪伴。我筛选了采用小调式、缓慢节奏的作品。", "为您准备的{mood}音乐清单：这些歌曲运用钢琴、大提琴等哀婉音色。"],
            "激昂": ["为您挑选{mood}音乐：这类作品通常具有强烈的节奏驱动。", "推荐{mood}风格：通过强烈的鼓点、电吉他失真音色。"],
            "平静": ["为您精选{mood}音乐：采用氛围音乐和极简主义手法。", "推荐{mood}风格：60 BPM左右的节奏接近人体静息心率。"],
            "愉悦": ["为您推荐{mood}音乐：融合放克、迪斯科元素的流行乐。", "挑选{mood}风格：这些歌曲通常采用 call and response 结构。"],
        }
        self._scene_templates = {
            "跑步": ["针对{scene}场景，推荐节奏在120-160 BPM的音乐。", "{scene}音乐推荐：选择能量值>0.7的电子乐或摇滚。"],
            "睡眠": ["为{scene}场景精选：50-60 BPM的氛围音乐。", "{scene}助眠音乐：通过白噪音、自然音效。"],
            "放松": ["{scene}疗愈音乐：融合新世纪音乐和民族乐器。", "推荐{scene}风格：慢板古典乐和氛围电子的融合。"],
        }
        self._extensions = {
            "乐理": "音乐理论是理解音乐语言的钥匙。",
            "历史": "了解音乐的历史背景，能帮助我们理解不同时代人们的情感表达方式。",
            "流派": "音乐流派的演变反映了社会文化的变迁。",
            "技巧": "演奏技巧的提升需要长期练习。",
            "乐器": "不同乐器有独特的音色DNA。",
        }

    def recommend_by_mood(self, mood: str, songs: List[Dict]) -> LLMResponse:
        template = random.choice(self._mood_templates.get(mood, self._mood_templates["欢快"]))
        intro = template.format(mood=mood)
        song_comments = [f"{i+1}. 《{s['title']}》- {s['artist']}：{s['description'][:40]}..." for i, s in enumerate(songs[:5])]
        content = f"{intro}\n\n" + "\n".join(song_comments) + f"\n\n总时长约{sum(s['duration'] for s in songs[:5])//60}分钟。"
        return LLMResponse(content=content, reasoning="Mock引擎模拟", confidence=0.8)

    def recommend_by_scene(self, scene: str, songs: List[Dict]) -> LLMResponse:
        template = random.choice(self._scene_templates.get(scene, self._scene_templates["放松"]))
        intro = template.format(scene=scene)
        song_comments = [f"{i+1}. 《{s['title']}》- {s['artist']} ({s['duration_str']})" for i, s in enumerate(songs[:5])]
        content = f"{intro}\n\n" + "\n".join(song_comments)
        return LLMResponse(content=content, reasoning="Mock引擎模拟", confidence=0.8)

    def generate_playlist_insight(self, songs: List[Dict]) -> LLMResponse:
        moods = set()
        for s in songs:
            moods.update(s.get('mood', []))
        content = f"这个播放列表展现了{random.choice(list(moods)) if moods else '多元'}的情绪主线。\n\n包含{len(songs)}首歌曲，跨越{len(set(s['genre'][0] for s in songs))}种流派。"
        return LLMResponse(content=content, reasoning="Mock引擎模拟", confidence=0.75)

    def answer_knowledge_question(self, question: str, knowledge: Optional[Dict] = None) -> LLMResponse:
        if knowledge:
            extension = self._extensions.get(knowledge['category'], "音乐的世界无穷无尽。")
            content = f"{knowledge['answer']}\n\n延伸思考：{extension}"
            return LLMResponse(content=content, reasoning="基于知识库", confidence=0.9)
        else:
            content = f"关于「{question}」，这是一个很有深度的音乐话题！建议您从基础乐理开始探索。"
            return LLMResponse(content=content, reasoning="Mock通用回答", confidence=0.6)

    def stream_response(self, text: str) -> Generator[str, None, None]:
        for word in text.split():
            yield word + " "


class LLMEngineFactory:
    """
    LLM 引擎工厂 —— 唯一负责读取配置、创建引擎的地方
    业务层（music_logic.py）只调用 create()，不读 .env
    """

    @staticmethod
    def create() -> BaseLLMEngine:
        """
        根据 .env 配置创建对应的 LLM 引擎
        必须在项目入口（app.py）先执行 load_dotenv() 后调用
        """
        import os

        engine_type = os.environ.get("LLM_ENGINE", "mock").lower().strip()

        if engine_type == "deepseek":
            api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
            model = os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-pro").strip()

            if not api_key or api_key == "sk-your-key-here":
                print("⚠️ DEEPSEEK_API_KEY 未设置或仍为默认值，回退到 Mock 引擎")
                return MockLLMEngine()

            try:
                engine = DeepSeekEngine(api_key=api_key, model=model)
                print(f"✅ DeepSeek 引擎已启动 | 模型: {model}")
                return engine
            except Exception as e:
                print(f"⚠️ DeepSeek 连接失败: {e}，回退到 Mock 引擎")
                return MockLLMEngine()

        elif engine_type == "qwen":
            print("⚠️ Qwen 引擎尚未实现，回退到 Mock 引擎")
            return MockLLMEngine()

        elif engine_type == "wenxin":
            print("⚠️ Wenxin 引擎尚未实现，回退到 Mock 引擎")
            return MockLLMEngine()

        else:
            print("ℹ️ 使用 Mock 引擎（无需 API Key）")
            return MockLLMEngine()
