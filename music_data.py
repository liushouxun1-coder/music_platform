"""
音乐数据层：定义音乐模型、模拟曲库、用户会话数据
与前端和LLM完全解耦
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
import random
import uuid

@dataclass
class Song:
    """歌曲数据模型"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    artist: str = ""
    album: str = ""
    duration: int = 180  # 秒
    genre: List[str] = field(default_factory=list)
    mood: List[str] = field(default_factory=list)  # 欢快、悲伤、激昂、平静等
    scene: List[str] = field(default_factory=list)  # 跑步、睡眠、工作、派对等
    tempo: int = 120  # BPM
    energy: float = 0.5  # 0-1
    description: str = ""
    lyrics_theme: str = ""  # 歌词主题
    year: int = 2020
    cover_url: str = "🎵"
    
    @property
    def duration_str(self) -> str:
        """格式化时长"""
        return f"{self.duration // 60}:{self.duration % 60:02d}"


class MusicLibrary:
    """音乐曲库：模拟大型音乐数据库"""
    
    def __init__(self):
        self._songs: Dict[str, Song] = {}
        self._init_library()
    
    def _init_library(self):
        """初始化丰富的模拟曲库"""
        songs_data = [
            # 欢快情绪
            {"title": "阳光宅男", "artist": "周杰伦", "mood": ["欢快", "愉悦"], "scene": ["派对", "驾车"],
             "genre": ["流行", "摇滚"], "tempo": 140, "energy": 0.9, "year": 2007,
             "description": "轻快的节奏，充满夏日活力的经典流行摇滚"},
            {"title": "Happy", "artist": "Pharrell Williams", "mood": ["欢快", "愉悦"], "scene": ["派对", "工作"],
             "genre": ["流行", "放克"], "tempo": 160, "energy": 0.95, "year": 2013,
             "description": "极具感染力的快乐旋律，Grammy获奖作品"},
            {"title": "小幸运", "artist": "田馥甄", "mood": ["欢快", "温暖"], "scene": ["散步", "下午茶"],
             "genre": ["流行"], "tempo": 120, "energy": 0.6, "year": 2015,
             "description": "清新温暖的青春回忆，轻快的民谣流行"},
            
            # 悲伤情绪
            {"title": "后来", "artist": "刘若英", "mood": ["悲伤", "怀旧"], "scene": ["独处", "雨天"],
             "genre": ["流行", "抒情"], "tempo": 72, "energy": 0.2, "year": 2000,
             "description": "深情的钢琴伴奏，讲述错过与遗憾的经典情歌"},
            {"title": "Someone Like You", "artist": "Adele", "mood": ["悲伤", "孤独"], "scene": ["独处", "深夜"],
             "genre": ["流行", "灵魂乐"], "tempo": 67, "energy": 0.15, "year": 2011,
             "description": "钢琴驱动的心碎挽歌，Adele的成名之作"},
            {"title": "消愁", "artist": "毛不易", "mood": ["悲伤", "迷茫"], "scene": ["深夜", "独处"],
             "genre": ["民谣"], "tempo": 85, "energy": 0.25, "year": 2017,
             "description": "八杯酒道尽人生百态，低沉嗓音的深夜独白"},
            
            # 激昂情绪
            {"title": "孤勇者", "artist": "陈奕迅", "mood": ["激昂", "励志"], "scene": ["运动", "工作"],
             "genre": ["流行", "摇滚"], "tempo": 130, "energy": 0.85, "year": 2021,
             "description": "热血沸腾的英雄赞歌，充满力量感的史诗流行"},
            {"title": "We Will Rock You", "artist": "Queen", "mood": ["激昂", "振奋"], "scene": ["运动", "派对"],
             "genre": ["摇滚"], "tempo": 164, "energy": 0.95, "year": 1977,
             "description": "标志性的跺脚节拍，体育场摇滚的不朽经典"},
            
            # 平静情绪
            {"title": "天空之城", "artist": "久石让", "mood": ["平静", "治愈"], "scene": ["睡眠", "阅读"],
             "genre": ["古典", "轻音乐"], "tempo": 60, "energy": 0.1, "year": 1986,
             "description": "宫崎骏动画配乐，钢琴与弦乐的梦幻交织"},
            {"title": "River Flows in You", "artist": "Yiruma", "mood": ["平静", "浪漫"], "scene": ["睡眠", "学习"],
             "genre": ["古典", "轻音乐"], "tempo": 72, "energy": 0.15, "year": 2001,
             "description": "如流水般清澈的钢琴曲，治愈系经典"},
            
            # 跑步场景
            {"title": "Eye of the Tiger", "artist": "Survivor", "mood": ["激昂"], "scene": ["跑步", "健身"],
             "genre": ["摇滚"], "tempo": 109, "energy": 0.9, "year": 1982,
             "description": "拳击电影《洛奇》主题曲，极具动感的训练伴侣"},
            {"title": "Titanium", "artist": "David Guetta ft. Sia", "mood": ["激昂", "坚定"], "scene": ["跑步", "健身"],
             "genre": ["电子", "舞曲"], "tempo": 128, "energy": 0.88, "year": 2011,
             "description": "电子舞曲与力量人声的结合，跑步节奏神器"},
            {"title": "奔跑", "artist": "羽泉", "mood": ["激昂", "励志"], "scene": ["跑步", "运动"],
             "genre": ["流行", "摇滚"], "tempo": 135, "energy": 0.8, "year": 2003,
             "description": "中文励志跑步神曲，节奏感强烈的流行摇滚"},
            
            # 睡眠场景
            {"title": "Weightless", "artist": "Marconi Union", "mood": ["平静", "放松"], "scene": ["睡眠", "冥想"],
             "genre": ["氛围音乐", "电子"], "tempo": 50, "energy": 0.05, "year": 2011,
             "description": "科学认证的最放松音乐，降低焦虑的声波设计"},
            {"title": "月光奏鸣曲", "artist": "贝多芬", "mood": ["平静", "深沉"], "scene": ["睡眠", "阅读"],
             "genre": ["古典"], "tempo": 55, "energy": 0.08, "year": 1801,
             "description": "贝多芬最著名的钢琴奏鸣曲，宁静而深邃的夜晚之声"},
            {"title": "夜曲", "artist": "肖邦", "mood": ["平静", "浪漫"], "scene": ["睡眠", "深夜"],
             "genre": ["古典"], "tempo": 60, "energy": 0.1, "year": 1830,
             "description": "钢琴诗人的夜色独白，如梦似幻的旋律"},
            
            # 放松疗愈
            {"title": "Canon in D", "artist": "Pachelbel", "mood": ["平静", "治愈"], "scene": ["放松", "下午茶"],
             "genre": ["古典"], "tempo": 70, "energy": 0.2, "year": 1680,
             "description": "巴洛克时期最优美的卡农，层层递进的和谐之美"},
            {"title": "故乡的原风景", "artist": "宗次郎", "mood": ["治愈", "怀旧"], "scene": ["放松", "冥想"],
             "genre": ["新世纪", "轻音乐"], "tempo": 65, "energy": 0.15, "year": 1991,
             "description": "陶笛演奏的东方意境，仿佛置身山野间的自然疗愈"},
            {"title": "A Thousand Years", "artist": "Christina Perri", "mood": ["浪漫", "治愈"], "scene": ["放松", "约会"],
             "genre": ["流行", "抒情"], "tempo": 69, "energy": 0.3, "year": 2011,
             "description": "电影《暮光之城》插曲，温柔而坚定的爱情誓言"},
        ]
        
        for data in songs_data:
            song = Song(**data)
            self._songs[song.id] = song
    
    def get_all(self) -> List[Song]:
        return list(self._songs.values())
    
    def get_by_mood(self, mood: str) -> List[Song]:
        """根据情绪筛选"""
        return [s for s in self._songs.values() if mood in s.mood]
    
    def get_by_scene(self, scene: str) -> List[Song]:
        """根据场景筛选"""
        return [s for s in self._songs.values() if scene in s.scene]
    
    def get_by_id(self, song_id: str) -> Optional[Song]:
        return self._songs.get(song_id)
    
    def search(self, query: str) -> List[Song]:
        """模糊搜索"""
        query = query.lower()
        results = []
        for song in self._songs.values():
            if (query in song.title.lower() or 
                query in song.artist.lower() or 
                query in song.description.lower() or
                any(query in m.lower() for m in song.mood) or
                any(query in s.lower() for s in song.scene)):
                results.append(song)
        return results
    
    def get_random(self, count: int = 5) -> List[Song]:
        """随机推荐"""
        return random.sample(list(self._songs.values()), min(count, len(self._songs)))


@dataclass
class MusicKnowledge:
    """音乐知识条目"""
    question: str
    answer: str
    category: str  # 乐理、历史、乐器、流派、技巧
    related_songs: List[str] = field(default_factory=list)
    difficulty: str = "中级"  # 初级、中级、高级


class KnowledgeBase:
    """音乐知识库"""
    
    def __init__(self):
        self._knowledge: List[MusicKnowledge] = []
        self._init_knowledge()
    
    def _init_knowledge(self):
        knowledge_data = [
            {
                "question": "什么是五声音阶？为什么中国音乐听起来很\"中国\"？",
                "answer": "五声音阶（Pentatonic Scale）由宫、商、角、徵、羽五个音组成，对应现代音乐的Do、Re、Mi、Sol、La。它省略了半音（Fa和Si），因此听起来和谐稳定，没有尖锐的不协和感。中国传统音乐、民谣甚至许多流行歌曲（如《茉莉花》《沧海一声笑》）都基于五声音阶，这种音阶结构赋予了中国音乐独特的东方韵味——既古朴典雅又空灵悠远。",
                "category": "乐理",
                "difficulty": "初级",
                "related_songs": ["茉莉花", "沧海一声笑"]
            },
            {
                "question": "为什么古典音乐有助于提高专注力？",
                "answer": "这被称为'莫扎特效应'。研究表明，古典音乐（特别是巴洛克时期如巴赫、维瓦尔第的作品）的节奏约为60-70 BPM，接近人体静息心率，能诱导大脑产生α波，使人进入放松而专注的状态。此外，古典音乐没有歌词，不会占用大脑的语言处理区域，因此适合作为工作、学习时的背景音乐。",
                "category": "乐理",
                "difficulty": "中级",
                "related_songs": ["G弦上的咏叹调", "四季"]
            },
            {
                "question": "电子音乐中的'Drop'是什么意思？",
                "answer": "Drop是电子舞曲（EDM）中最核心的高潮段落，通常出现在Build-up（情绪积累段）之后。在Drop处，所有乐器同时爆发，节奏、低音和旋律达到顶峰，是整首歌曲最具冲击力的部分。DJ在演出时往往会通过混音技巧强化Drop的效果，让舞池达到最高潮。经典例子包括Martin Garrix的《Animals》和Skrillex的《Bangarang》。",
                "category": "流派",
                "difficulty": "中级",
                "related_songs": ["Animals", "Bangarang"]
            },
            {
                "question": "爵士乐中的'即兴演奏'是如何进行的？",
                "answer": "爵士即兴不是随意乱弹，而是建立在严格的和声进行（Chord Progression）基础上的创造性表达。乐手需要：1）熟记歌曲的和弦进行（如II-V-I）；2）掌握对应音阶（如多利亚调式、混合利底亚调式）；3）运用乐句库（Licks）进行变奏；4）与其他乐手实时互动（Call and Response）。伟大的爵士即兴是理性与感性的完美结合。",
                "category": "技巧",
                "difficulty": "高级",
                "related_songs": ["Take Five", "So What"]
            },
            {
                "question": "为什么有些歌一听就让人感到悲伤？",
                "answer": "音乐引发悲伤感主要通过几个机制：1）小调（Minor Key）本身带有忧郁色彩；2）下行音阶模拟叹息和哭泣；3）缓慢的节奏（60-80 BPM）匹配悲伤时的心率；4）音色选择（如大提琴、钢琴）本身具有哀婉特质；5）不协和音程（如小二度、三全音）制造紧张感。阿黛尔的《Someone Like You》就是综合运用这些元素的典范。",
                "category": "乐理",
                "difficulty": "中级",
                "related_songs": ["Someone Like You", "后来"]
            },
            {
                "question": "什么是'概念专辑'（Concept Album）？",
                "answer": "概念专辑是指整张专辑围绕一个统一的主题、故事或概念展开的专辑形式，而非单曲的简单集合。它要求歌曲之间有叙事连贯性或主题关联性。经典例子包括：Pink Floyd的《The Dark Side of the Moon》（探讨人性与疯狂）、周杰伦的《范特西》（以幻想为主题）。概念专辑代表了音乐人最高的艺术追求。",
                "category": "历史",
                "difficulty": "中级",
                "related_songs": ["The Dark Side of the Moon", "范特西"]
            }
        ]
        
        for data in knowledge_data:
            self._knowledge.append(MusicKnowledge(**data))
    
    def get_all(self) -> List[MusicKnowledge]:
        return self._knowledge
    
    def search(self, query: str) -> List[MusicKnowledge]:
        """搜索知识"""
        query = query.lower()
        return [k for k in self._knowledge if 
                query in k.question.lower() or query in k.answer.lower() or
                query in k.category.lower()]
    
    def get_by_category(self, category: str) -> List[MusicKnowledge]:
        return [k for k in self._knowledge if k.category == category]