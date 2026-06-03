"""精简版音乐数据层"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict
import random, uuid


@dataclass
class Song:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""; artist: str = ""; album: str = ""
    duration: int = 180
    genre: List[str] = field(default_factory=list)
    mood: List[str] = field(default_factory=list)
    scene: List[str] = field(default_factory=list)
    tempo: int = 120
    energy: float = 0.5
    description: str = ""
    year: int = 2020
    cover_url: str = "🎵"

    @property
    def duration_str(self) -> str:
        return f"{self.duration//60}:{self.duration%60:02d}"

    def to_dict(self) -> Dict:
        return {
            "id": self.id, "title": self.title, "artist": self.artist, "album": self.album,
            "duration": self.duration, "duration_str": self.duration_str,
            "genre": self.genre, "mood": self.mood, "scene": self.scene,
            "tempo": self.tempo, "energy": self.energy,
            "description": self.description, "year": self.year, "cover": self.cover_url
        }


class MusicLibrary:
    _DATA = [
        {"title": "稻香", "artist": "周杰伦", "mood": ["治愈", "温暖"], "scene": ["散步", "放松"], "genre": ["流行", "民谣"], "tempo": 90, "energy": 0.7, "year": 2008, "description": "乡村风格的励志歌曲，唤起童年记忆与家的温暖"},
        {"title": "逆光", "artist": "孙燕姿", "mood": ["坚定", "励志"], "scene": ["运动", "驾车"], "genre": ["流行"], "tempo": 128, "energy": 0.75, "year": 2007, "description": "充满力量与希望的旋律，鼓励迎难而上"},
        {"title": "Shake It Off", "artist": "Taylor Swift", "mood": ["欢快", "愉悦"], "scene": ["派对", "运动"], "genre": ["流行", "舞曲"], "tempo": 160, "energy": 0.92, "year": 2014, "description": "无视流言蜚语的快乐舞曲，轻快铜管与俏皮歌词"},
        {"title": "Blinding Lights", "artist": "The Weeknd", "mood": ["激昂", "欢快"], "scene": ["驾车", "派对"], "genre": ["电子", "流行"], "tempo": 171, "energy": 0.85, "year": 2019, "description": "复古合成器浪潮，极具速度感的都市夜行曲"},
        {"title": "Lose Yourself", "artist": "Eminem", "mood": ["激昂", "专注"], "scene": ["运动", "工作"], "genre": ["嘻哈"], "tempo": 171, "energy": 0.9, "year": 2002, "description": "奥斯卡最佳原创歌曲，充满紧迫感的励志说唱"},
        {"title": "平凡之路", "artist": "朴树", "mood": ["平静", "治愈"], "scene": ["驾车", "独处"], "genre": ["民谣", "摇滚"], "tempo": 78, "energy": 0.4, "year": 2014, "description": "电影《后会无期》主题曲，关于流浪与成长的哲思"},
        {"title": "Imagine", "artist": "John Lennon", "mood": ["平静", "希望"], "scene": ["冥想", "放松"], "genre": ["流行", "古典"], "tempo": 76, "energy": 0.2, "year": 1971, "description": "和平颂歌，钢琴驱动的乌托邦愿景"},
        {"title": "Bohemian Rhapsody", "artist": "Queen", "mood": ["激昂", "深沉"], "scene": ["派对", "独处"], "genre": ["摇滚"], "tempo": 72, "energy": 0.8, "year": 1975, "description": "结构复杂的前卫摇滚史诗，融合歌剧、硬摇滚与民谣"},
        {"title": "Shape of You", "artist": "Ed Sheeran", "mood": ["欢快", "浪漫"], "scene": ["派对", "运动"], "genre": ["流行", "舞曲"], "tempo": 96, "energy": 0.85, "year": 2017, "description": "热带浩室节奏下的爱情赞歌，流媒体时代神曲"},
        {"title": "Viva La Vida", "artist": "Coldplay", "mood": ["激昂", "历史"], "scene": ["工作", "驾车"], "genre": ["摇滚", "古典"], "tempo": 138, "energy": 0.7, "year": 2008, "description": "弦乐铺陈的帝王挽歌，关于权力与失落的寓言"},
        {"title": "夜的第七章", "artist": "周杰伦", "mood": ["深沉", "悬疑"], "scene": ["深夜", "独处"], "genre": ["流行", "古典"], "tempo": 85, "energy": 0.6, "year": 2006, "description": "侦探主题的暗黑叙事，编曲充满古典弦乐与神秘感"},
        {"title": "Bad Guy", "artist": "Billie Eilish", "mood": ["欢快", "挑衅"], "scene": ["派对", "运动"], "genre": ["电子", "流行"], "tempo": 135, "energy": 0.6, "year": 2019, "description": "极简低音与俏皮人声，反传统的另类流行"},
        {"title": "Rolling in the Deep", "artist": "Adele", "mood": ["激昂", "愤怒"], "scene": ["运动", "独处"], "genre": ["流行", "灵魂乐"], "tempo": 105, "energy": 0.85, "year": 2010, "description": "复仇主题的灵魂流行，爆炸性副歌与蓝调吉他"},
        {"title": "Clocks", "artist": "Coldplay", "mood": ["激昂", "专注"], "scene": ["工作", "学习"], "genre": ["摇滚"], "tempo": 130, "energy": 0.65, "year": 2002, "description": "标志性的钢琴riff，时间流逝感的渐进摇滚"},
        {"title": "Hallelujah", "artist": "Leonard Cohen", "mood": ["悲伤", "神圣"], "scene": ["深夜", "独处"], "genre": ["民谣", "古典"], "tempo": 62, "energy": 0.2, "year": 1984, "description": "充满宗教意象的民谣，无数翻唱的经典"},
        {"title": "Thinking Out Loud", "artist": "Ed Sheeran", "mood": ["浪漫", "温暖"], "scene": ["约会", "放松"], "genre": ["流行", "民谣"], "tempo": 79, "energy": 0.4, "year": 2014, "description": "婚礼必备情歌，灵魂乐风格的吉他弹唱"},
        {"title": "Dance Monkey", "artist": "Tones and I", "mood": ["欢快", "活力"], "scene": ["派对", "运动"], "genre": ["流行", "电子"], "tempo": 98, "energy": 0.75, "year": 2019, "description": "俏皮沙哑人声+复古合成器，街头艺人逆袭神曲"},
        {"title": "Hotel California", "artist": "Eagles", "mood": ["深沉", "悬疑"], "scene": ["驾车", "深夜"], "genre": ["摇滚"], "tempo": 75, "energy": 0.5, "year": 1977, "description": "双吉他solo传世经典，讲述囚笼般的奢华酒店"},
        {"title": "Something Just Like This", "artist": "The Chainsmokers & Coldplay", "mood": ["浪漫", "治愈"], "scene": ["派对", "运动"], "genre": ["电子", "流行"], "tempo": 103, "energy": 0.7, "year": 2017, "description": "关于平凡爱情的电子流行，温暖而谦逊"},
        {"title": "凉凉", "artist": "张碧晨 & 杨宗纬", "mood": ["悲伤", "浪漫"], "scene": ["独处", "深夜"], "genre": ["流行", "古风"], "tempo": 78, "energy": 0.35, "year": 2017, "description": "电视剧《三生三世十里桃花》片尾曲，凄美对唱"},
        {"title": "City of Stars", "artist": "Ryan Gosling & Emma Stone", "mood": ["浪漫", "怀旧"], "scene": ["深夜", "独处"], "genre": ["爵士", "流行"], "tempo": 85, "energy": 0.25, "year": 2016, "description": "电影《爱乐之城》主题曲，追梦人的温柔独白"},
        {"title": "Believer", "artist": "Imagine Dragons", "mood": ["激昂", "坚定"], "scene": ["运动", "工作"], "genre": ["摇滚", "流行"], "tempo": 125, "energy": 0.95, "year": 2017, "description": "打击乐强烈的自我激励曲，疼痛转化为力量"},
        {"title": "Demons", "artist": "Imagine Dragons", "mood": ["悲伤", "治愈"], "scene": ["独处", "深夜"], "genre": ["摇滚"], "tempo": 90, "energy": 0.5, "year": 2012, "description": "直面内心恶魔，主唱脆弱人声与爆发合唱"},
        {"title": "Counting Stars", "artist": "OneRepublic", "mood": ["欢快", "励志"], "scene": ["运动", "驾车"], "genre": ["流行", "摇滚"], "tempo": 122, "energy": 0.8, "year": 2013, "description": "追逐梦想的流行摇滚，木吉他扫弦与福音合唱"},
        {"title": "Radioactive", "artist": "Imagine Dragons", "mood": ["激昂", "黑暗"], "scene": ["运动", "工作"], "genre": ["摇滚", "电子"], "tempo": 136, "energy": 0.85, "year": 2012, "description": "末日风格的电子摇滚，低音重击与爆发副歌"},
        {"title": "Stressed Out", "artist": "Twenty One Pilots", "mood": ["悲伤", "怀旧"], "scene": ["独处", "深夜"], "genre": ["另类", "嘻哈"], "tempo": 85, "energy": 0.5, "year": 2015, "description": "关于成年焦虑与童年怀念，低传真的感性表达"},
        {"title": "Ride", "artist": "Twenty One Pilots", "mood": ["欢快", "迷茫"], "scene": ["驾车", "放松"], "genre": ["另类", "雷鬼"], "tempo": 120, "energy": 0.65, "year": 2015, "description": "雷鬼节奏的存在主义思考，在快乐中感受虚无"},
        {"title": "Heathens", "artist": "Twenty One Pilots", "mood": ["深沉", "悬疑"], "scene": ["深夜", "独处"], "genre": ["另类", "摇滚"], "tempo": 90, "energy": 0.55, "year": 2016, "description": "电影《自杀小队》插曲，黑暗中的边缘人宣言"},
        {"title": "Happier", "artist": "Marshmello & Bastille", "mood": ["悲伤", "电子"], "scene": ["独处", "深夜"], "genre": ["电子", "流行"], "tempo": 100, "energy": 0.6, "year": 2018, "description": "伪装成快乐舞曲的悲伤情歌，放手也是一种爱"},
        {"title": "Silence", "artist": "Marshmello ft. Khalid", "mood": ["治愈", "电子"], "scene": ["放松", "深夜"], "genre": ["电子", "流行"], "tempo": 96, "energy": 0.55, "year": 2017, "description": "关于内心平静的电子流行，空灵人声与渐进drop"},
        {"title": "Faded", "artist": "Alan Walker", "mood": ["悲伤", "电子"], "scene": ["独处", "深夜"], "genre": ["电子", "流行"], "tempo": 90, "energy": 0.5, "year": 2015, "description": "空灵女声+渐进浩室，关于迷失与寻找的电子神曲"},
        {"title": "Alone", "artist": "Alan Walker", "mood": ["悲伤", "电子"], "scene": ["独处", "深夜"], "genre": ["电子"], "tempo": 97, "energy": 0.6, "year": 2016, "description": "尽管孤独但你我同在，电音中的归属感"},
        {"title": "The Spectre", "artist": "Alan Walker", "mood": ["激昂", "电子"], "scene": ["运动", "派对"], "genre": ["电子"], "tempo": 128, "energy": 0.8, "year": 2017, "description": "极具爆发力的渐进浩室，召唤内心的自由灵魂"},
        {"title": "Wake Me Up", "artist": "Avicii", "mood": ["欢快", "励志"], "scene": ["驾车", "运动"], "genre": ["电子", "民谣"], "tempo": 124, "energy": 0.85, "year": 2013, "description": "电音与蓝草民谣的结合，寻找自我的人生旅程"},
        {"title": "Waiting for Love", "artist": "Avicii", "mood": ["浪漫", "励志"], "scene": ["驾车", "派对"], "genre": ["电子"], "tempo": 128, "energy": 0.82, "year": 2015, "description": "充满希望的爱情电子，温暖人声与抓人旋律"},
        {"title": "Hey Jude", "artist": "The Beatles", "mood": ["治愈", "希望"], "scene": ["放松", "聚会"], "genre": ["摇滚"], "tempo": 74, "energy": 0.5, "year": 1968, "description": "传世经典，na na na合唱治愈无数心灵"},
        {"title": "Let It Be", "artist": "The Beatles", "mood": ["平静", "治愈"], "scene": ["冥想", "独处"], "genre": ["摇滚"], "tempo": 70, "energy": 0.3, "year": 1970, "description": "顺其自然的智慧，教堂般的庄严与温柔"},
        {"title": "Yesterday", "artist": "The Beatles", "mood": ["悲伤", "怀旧"], "scene": ["独处", "深夜"], "genre": ["流行"], "tempo": 82, "energy": 0.2, "year": 1965, "description": "史上被翻唱最多的歌曲，弦乐四重奏的忧伤"},
        {"title": "海浪", "artist": "Deca Joins", "mood": ["悲伤", "迷茫"], "scene": ["深夜", "独处"], "genre": ["独立", "摇滚"], "tempo": 105, "energy": 0.4, "year": 2017, "description": "台湾独立乐队代表作，慵懒颓废的都市迷惘"},
        {"title": "山海", "artist": "草东没有派对", "mood": ["愤怒", "悲伤"], "scene": ["独处", "深夜"], "genre": ["独立", "摇滚"], "tempo": 130, "energy": 0.8, "year": 2016, "description": "毁灭性的自我剖析，爆发嘶吼与沉默低语"},
        {"title": "丑", "artist": "草东没有派对", "mood": ["愤怒", "无力"], "scene": ["深夜", "独处"], "genre": ["独立", "摇滚"], "tempo": 136, "energy": 0.85, "year": 2016, "description": "自我厌恶的呐喊，直击灵魂的华语独立摇滚"},
        {"title": "阳光宅男", "artist": "周杰伦", "mood": ["欢快", "愉悦"], "scene": ["派对", "驾车"], "genre": ["流行", "摇滚"], "tempo": 140, "energy": 0.9, "year": 2007, "description": "轻快的节奏，充满夏日活力的经典流行摇滚"},
        {"title": "Happy", "artist": "Pharrell Williams", "mood": ["欢快", "愉悦"], "scene": ["派对", "工作"], "genre": ["流行", "放克"], "tempo": 160, "energy": 0.95, "year": 2013, "description": "极具感染力的快乐旋律，Grammy获奖作品"},
        {"title": "小幸运", "artist": "田馥甄", "mood": ["欢快", "温暖"], "scene": ["散步", "下午茶"], "genre": ["流行"], "tempo": 120, "energy": 0.6, "year": 2015, "description": "清新温暖的青春回忆，轻快的民谣流行"},
        {"title": "后来", "artist": "刘若英", "mood": ["悲伤", "怀旧"], "scene": ["独处", "雨天"], "genre": ["流行", "抒情"], "tempo": 72, "energy": 0.2, "year": 2000, "description": "深情的钢琴伴奏，讲述错过与遗憾的经典情歌"},
        {"title": "Someone Like You", "artist": "Adele", "mood": ["悲伤", "孤独"], "scene": ["独处", "深夜"], "genre": ["流行", "灵魂乐"], "tempo": 67, "energy": 0.15, "year": 2011, "description": "钢琴驱动的心碎挽歌，Adele的成名之作"},
        {"title": "消愁", "artist": "毛不易", "mood": ["悲伤", "迷茫"], "scene": ["深夜", "独处"], "genre": ["民谣"], "tempo": 85, "energy": 0.25, "year": 2017, "description": "八杯酒道尽人生百态，低沉嗓音的深夜独白"},
        {"title": "孤勇者", "artist": "陈奕迅", "mood": ["激昂", "励志"], "scene": ["运动", "工作"], "genre": ["流行", "摇滚"], "tempo": 130, "energy": 0.85, "year": 2021, "description": "热血沸腾的英雄赞歌，充满力量感的史诗流行"},
        {"title": "We Will Rock You", "artist": "Queen", "mood": ["激昂", "振奋"], "scene": ["运动", "派对"], "genre": ["摇滚"], "tempo": 164, "energy": 0.95, "year": 1977, "description": "标志性的跺脚节拍，体育场摇滚的不朽经典"},
        {"title": "天空之城", "artist": "久石让", "mood": ["平静", "治愈"], "scene": ["睡眠", "阅读"], "genre": ["古典", "轻音乐"], "tempo": 60, "energy": 0.1, "year": 1986, "description": "宫崎骏动画配乐，钢琴与弦乐的梦幻交织"},
        {"title": "River Flows in You", "artist": "Yiruma", "mood": ["平静", "浪漫"], "scene": ["睡眠", "学习"], "genre": ["古典", "轻音乐"], "tempo": 72, "energy": 0.15, "year": 2001, "description": "如流水般清澈的钢琴曲，治愈系经典"},
        {"title": "Eye of the Tiger", "artist": "Survivor", "mood": ["激昂"], "scene": ["跑步", "健身"], "genre": ["摇滚"], "tempo": 109, "energy": 0.9, "year": 1982, "description": "拳击电影《洛奇》主题曲，极具动感的训练伴侣"},
        {"title": "Titanium", "artist": "David Guetta ft. Sia", "mood": ["激昂", "坚定"], "scene": ["跑步", "健身"], "genre": ["电子", "舞曲"], "tempo": 128, "energy": 0.88, "year": 2011, "description": "电子舞曲与力量人声的结合，跑步节奏神器"},
        {"title": "奔跑", "artist": "羽泉", "mood": ["激昂", "励志"], "scene": ["跑步", "运动"], "genre": ["流行", "摇滚"], "tempo": 135, "energy": 0.8, "year": 2003, "description": "中文励志跑步神曲，节奏感强烈的流行摇滚"},
        {"title": "Weightless", "artist": "Marconi Union", "mood": ["平静", "放松"], "scene": ["睡眠", "冥想"], "genre": ["氛围音乐", "电子"], "tempo": 50, "energy": 0.05, "year": 2011, "description": "科学认证的最放松音乐，降低焦虑的声波设计"},
        {"title": "月光奏鸣曲", "artist": "贝多芬", "mood": ["平静", "深沉"], "scene": ["睡眠", "阅读"], "genre": ["古典"], "tempo": 55, "energy": 0.08, "year": 1801, "description": "贝多芬最著名的钢琴奏鸣曲，宁静而深邃的夜晚之声"},
        {"title": "夜曲", "artist": "肖邦", "mood": ["平静", "浪漫"], "scene": ["睡眠", "深夜"], "genre": ["古典"], "tempo": 60, "energy": 0.1, "year": 1830, "description": "钢琴诗人的夜色独白，如梦似幻的旋律"},
        {"title": "Canon in D", "artist": "Pachelbel", "mood": ["平静", "治愈"], "scene": ["放松", "下午茶"], "genre": ["古典"], "tempo": 70, "energy": 0.2, "year": 1680, "description": "巴洛克时期最优美的卡农，层层递进的和谐之美"},
        {"title": "故乡的原风景", "artist": "宗次郎", "mood": ["治愈", "怀旧"], "scene": ["放松", "冥想"], "genre": ["新世纪", "轻音乐"], "tempo": 65, "energy": 0.15, "year": 1991, "description": "陶笛演奏的东方意境，仿佛置身山野间的自然疗愈"},
        {"title": "A Thousand Years", "artist": "Christina Perri", "mood": ["浪漫", "治愈"], "scene": ["放松", "约会"], "genre": ["流行", "抒情"], "tempo": 69, "energy": 0.3, "year": 2011, "description": "电影《暮光之城》插曲，温柔而坚定的爱情誓言"},
    ]

    def __init__(self):
        self._songs = {s.id: s for s in [Song(**d) for d in self._DATA]}

    def get_all(self) -> List[Song]: return list(self._songs.values())
    def get_by_mood(self, mood: str) -> List[Song]: return [s for s in self._songs.values() if mood in s.mood]
    def get_by_scene(self, scene: str) -> List[Song]: return [s for s in self._songs.values() if scene in s.scene]
    def get_by_id(self, sid: str) -> Optional[Song]: return self._songs.get(sid)
    def get_random(self, n: int = 5) -> List[Song]: return random.sample(list(self._songs.values()), min(n, len(self._songs)))

    def search(self, q: str) -> List[Song]:
        q = q.lower()
        return [s for s in self._songs.values() if q in s.title.lower() or q in s.artist.lower() or q in s.description.lower()
                or any(q in m.lower() for m in s.mood) or any(q in sc.lower() for sc in s.scene)]


@dataclass
class MusicKnowledge:
    question: str; answer: str; category: str
    related_songs: List[str] = field(default_factory=list)
    difficulty: str = "中级"


class KnowledgeBase:
    _DATA = [
        {"question": "什么是五声音阶？为什么中国音乐听起来很\"中国\"？", "answer": "五声音阶（Pentatonic Scale）由宫、商、角、徵、羽五个音组成，对应Do、Re、Mi、Sol、La。省略了半音（Fa和Si），听起来和谐稳定，没有尖锐的不协和感。中国传统音乐、民谣甚至许多流行歌曲都基于五声音阶，赋予了中国音乐独特的东方韵味。", "category": "乐理", "difficulty": "初级", "related_songs": ["茉莉花", "沧海一声笑"]},
        {"question": "为什么古典音乐有助于提高专注力？", "answer": "这被称为'莫扎特效应'。巴洛克时期作品节奏约60-70 BPM，接近人体静息心率，能诱导大脑产生α波，使人进入放松而专注的状态。此外，古典音乐没有歌词，不会占用大脑的语言处理区域。", "category": "乐理", "difficulty": "中级", "related_songs": ["G弦上的咏叹调", "四季"]},
        {"question": "电子音乐中的'Drop'是什么意思？", "answer": "Drop是电子舞曲（EDM）中最核心的高潮段落，通常出现在Build-up之后。所有乐器同时爆发，节奏、低音和旋律达到顶峰，是整首歌曲最具冲击力的部分。", "category": "流派", "difficulty": "中级", "related_songs": ["Animals", "Bangarang"]},
        {"question": "爵士乐中的'即兴演奏'是如何进行的？", "answer": "爵士即兴建立在严格的和声进行基础上。乐手需要：1）熟记和弦进行（如II-V-I）；2）掌握对应音阶；3）运用乐句库（Licks）进行变奏；4）与其他乐手实时互动。是理性与感性的完美结合。", "category": "技巧", "difficulty": "高级", "related_songs": ["Take Five", "So What"]},
        {"question": "为什么有些歌一听就让人感到悲伤？", "answer": "主要通过：1）小调带有忧郁色彩；2）下行音阶模拟叹息；3）缓慢节奏（60-80 BPM）匹配悲伤时的心率；4）哀婉音色（大提琴、钢琴）；5）不协和音程制造紧张感。", "category": "乐理", "difficulty": "中级", "related_songs": ["Someone Like You", "后来"]},
        {"question": "什么是'概念专辑'（Concept Album）？", "answer": "概念专辑是指整张专辑围绕统一主题、故事或概念展开的专辑形式，而非单曲集合。经典例子包括Pink Floyd的《The Dark Side of the Moon》、周杰伦的《范特西》。", "category": "历史", "difficulty": "中级", "related_songs": ["The Dark Side of the Moon", "范特西"]},
    ]

    def __init__(self):
        self._kb = [MusicKnowledge(**d) for d in self._DATA]

    def get_all(self) -> List[MusicKnowledge]: return self._kb
    def search(self, q: str) -> List[MusicKnowledge]:
        q = q.lower()
        return [k for k in self._kb if q in k.question.lower() or q in k.answer.lower() or q in k.category.lower()]
    def get_by_category(self, cat: str) -> List[MusicKnowledge]: return [k for k in self._kb if k.category == cat]