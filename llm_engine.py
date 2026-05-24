"""精简版 LLM 引擎"""
import os, random
from typing import List, Dict, Optional, Generator
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


@dataclass
class LLMResponse:
    content: str
    reasoning: str = ""
    confidence: float = 0.9
    sources: List[str] = field(default_factory=list)


class BaseLLMEngine(ABC):
    @abstractmethod
    def recommend_by_mood(self, mood: str, songs: List[Dict]) -> LLMResponse: pass
    @abstractmethod
    def recommend_by_scene(self, scene: str, songs: List[Dict]) -> LLMResponse: pass
    @abstractmethod
    def generate_playlist_insight(self, songs: List[Dict]) -> LLMResponse: pass
    @abstractmethod
    def answer_knowledge_question(self, question: str, knowledge: Optional[Dict] = None) -> LLMResponse: pass


class DeepSeekEngine(BaseLLMEngine):
    def __init__(self, api_key: str, model: str = "deepseek-v4-pro"):
        if OpenAI is None: raise ImportError("pip install openai")
        if not api_key: raise ValueError("api_key 不能为空")
        self.model, self.client = model, OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def _call(self, system: str, user: str, thinking: bool = True) -> LLMResponse:
        msgs = [{"role": "system", "content": system}, {"role": "user", "content": user}]
        kwargs = {"model": self.model, "messages": msgs, "stream": False, "max_tokens": 4096}
        if thinking and self.model == "deepseek-v4-pro":
            kwargs["extra_body"] = {"thinking": {"type": "enabled"}}
        try:
            r = self.client.chat.completions.create(**kwargs)
            m = r.choices[0].message
            return LLMResponse(m.content or "", getattr(m, "reasoning_content", "") or "DeepSeek生成", 0.92)
        except Exception as e:
            return LLMResponse(f"AI 服务不可用：{e}", "API失败", 0.0)

    def recommend_by_mood(self, mood: str, songs: List[Dict]) -> LLMResponse:
        info = "\n".join([f"{i+1}. 《{s['title']}》- {s['artist']} | {s['genre'][0]} | BPM:{s['tempo']} | 能量:{s['energy']:.2f} | {s['description']}" for i, s in enumerate(songs[:6])])
        return self._call("你是专业音乐推荐师和音乐心理学家。用温暖专业的中文回答，适当使用emoji。",
                         f'用户想要"{mood}"情绪的音乐。\n可用歌曲：\n{info}\n\n请生成：1.为什么适合该情绪 2.每首点评 3.播放顺序建议')

    def recommend_by_scene(self, scene: str, songs: List[Dict]) -> LLMResponse:
        info = "\n".join([f"{i+1}. 《{s['title']}》- {s['artist']} | {s['genre'][0]} | BPM:{s['tempo']} | 能量:{s['energy']:.2f}" for i, s in enumerate(songs[:6])])
        return self._call("你是专业音乐推荐师。用实用亲切的中文回答。",
                         f'用户正在"{scene}"场景。\n可用歌曲：\n{info}\n\n请生成场景适配分析和歌曲点评。')

    def generate_playlist_insight(self, songs: List[Dict]) -> LLMResponse:
        info = "\n".join([f"{i+1}. 《{s['title']}》- {s['artist']} | 情绪:{','.join(s['mood'])} | BPM:{s['tempo']} | 能量:{s['energy']:.2f}" for i, s in enumerate(songs)])
        return self._call("你是音乐评论家。用富有文学性的中文回答。", f'请为以下播放列表生成洞察：\n\n{info}\n\n生成诗意描述、数据洞察和聆听建议。', False)

    def answer_knowledge_question(self, question: str, knowledge: Optional[Dict] = None) -> LLMResponse:
        ctx = f"\n相关知识：{knowledge['answer']}\n分类：{knowledge['category']}" if knowledge else ""
        return self._call("你是资深音乐学者。用通俗易懂但专业准确的中文回答。",
                         f'用户问题：{question}{ctx}\n\n请深入浅出地回答，举例说明。')


class MockLLMEngine(BaseLLMEngine):
    _mood_tpl = {
        "欢快": ["基于您对{mood}音乐的需求，精选了节奏明快、旋律上扬的歌曲。", "为您推荐{mood}风格：这类音乐往往具有跳跃的节奏型。"],
        "悲伤": ["理解您需要{mood}的音乐陪伴。筛选了采用小调式、缓慢节奏的作品。", "为您准备的{mood}音乐：运用钢琴、大提琴等哀婉音色。"],
        "激昂": ["为您挑选{mood}音乐：具有强烈的节奏驱动。", "推荐{mood}风格：通过强烈的鼓点、电吉他失真音色。"],
        "平静": ["为您精选{mood}音乐：采用氛围音乐和极简主义手法。", "推荐{mood}风格：60 BPM左右的节奏接近人体静息心率。"],
        "愉悦": ["为您推荐{mood}音乐：融合放克、迪斯科元素的流行乐。", "挑选{mood}风格：采用 call and response 结构。"],
    }
    _scene_tpl = {
        "跑步": ["针对{scene}场景，推荐节奏120-160 BPM的音乐。", "{scene}音乐推荐：选择能量值>0.7的电子乐或摇滚。"],
        "睡眠": ["为{scene}场景精选：50-60 BPM的氛围音乐。", "{scene}助眠音乐：通过白噪音、自然音效。"],
        "放松": ["{scene}疗愈音乐：融合新世纪音乐和民族乐器。", "推荐{scene}风格：慢板古典乐和氛围电子的融合。"],
    }

    def recommend_by_mood(self, mood: str, songs: List[Dict]) -> LLMResponse:
        tpl = random.choice(self._mood_tpl.get(mood, self._mood_tpl["欢快"]))
        cmt = [f"{i+1}. 《{s['title']}》- {s['artist']}：{s['description'][:40]}..." for i, s in enumerate(songs[:5])]
        content = f"{tpl.format(mood=mood)}\n\n" + "\n".join(cmt) + f"\n\n总时长约{sum(s['duration'] for s in songs[:5])//60}分钟。"
        return LLMResponse(content, "Mock模拟", 0.8)

    def recommend_by_scene(self, scene: str, songs: List[Dict]) -> LLMResponse:
        tpl = random.choice(self._scene_tpl.get(scene, self._scene_tpl["放松"]))
        cmt = [f"{i+1}. 《{s['title']}》- {s['artist']} ({s['duration_str']})" for i, s in enumerate(songs[:5])]
        return LLMResponse(f"{tpl.format(scene=scene)}\n\n" + "\n".join(cmt), "Mock模拟", 0.8)

    def generate_playlist_insight(self, songs: List[Dict]) -> LLMResponse:
        moods = set().union(*[set(s.get('mood',[])) for s in songs])
        return LLMResponse(f"这个播放列表展现了{random.choice(list(moods)) if moods else '多元'}的情绪主线。\n\n包含{len(songs)}首歌曲，跨越{len(set(s['genre'][0] for s in songs))}种流派。", "Mock模拟", 0.75)

    def answer_knowledge_question(self, question: str, knowledge: Optional[Dict] = None) -> LLMResponse:
        if knowledge:
            ext = {"乐理": "音乐理论是理解音乐语言的钥匙。", "历史": "了解音乐的历史背景，能理解不同时代人们的情感表达方式。", "流派": "音乐流派的演变反映了社会文化的变迁。", "技巧": "演奏技巧的提升需要长期练习。", "乐器": "不同乐器有独特的音色DNA。"}.get(knowledge['category'], "音乐的世界无穷无尽。")
            return LLMResponse(f"{knowledge['answer']}\n\n延伸思考：{ext}", "基于知识库", 0.9)
        return LLMResponse(f"关于「{question}」，建议从基础乐理开始探索。", "Mock通用回答", 0.6)


class LLMEngineFactory:
    @staticmethod
    def create() -> BaseLLMEngine:
        engine = os.environ.get("LLM_ENGINE", "mock").lower().strip()
        if engine == "deepseek":
            key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
            if not key or key == "sk-your-key-here":
                print("⚠️ DEEPSEEK_API_KEY 未设置，回退到 Mock"); return MockLLMEngine()
            try:
                print(f"✅ DeepSeek 引擎启动 | 模型: {os.environ.get('DEEPSEEK_MODEL', 'deepseek-v4-pro')}")
                return DeepSeekEngine(key, os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-pro"))
            except Exception as e:
                print(f"⚠️ DeepSeek 失败: {e}，回退到 Mock"); return MockLLMEngine()
        print("ℹ️ 使用 Mock 引擎"); return MockLLMEngine()