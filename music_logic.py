"""
music_logic.py - 音乐业务逻辑层
职责：推荐算法 + 知识检索，不碰配置读取
"""
from typing import List, Dict, Optional
from music_data import MusicLibrary, KnowledgeBase, Song
from llm_engine import LLMEngineFactory, BaseLLMEngine


class MusicRecommender:
    """音乐推荐服务"""

    def __init__(self, llm: BaseLLMEngine = None):
        self.library = MusicLibrary()
        # 外部传入引擎，或工厂创建（确保全局唯一实例）
        self.llm = llm or LLMEngineFactory.create()

    def get_mood_recommendations(self, mood: str) -> Dict:
        """获取基于情绪的推荐（含LLM智能解读）"""
        songs = self.library.get_by_mood(mood)
        if not songs:
            songs = self.library.get_random(5)

        songs.sort(key=lambda s: s.energy, reverse=True)
        songs_dict = [self._song_to_dict(s) for s in songs[:6]]
        llm_response = self.llm.recommend_by_mood(mood, songs_dict)

        return {
            "mood": mood,
            "songs": songs_dict,
            "llm_analysis": llm_response,
            "total_found": len(songs)
        }

    def get_scene_recommendations(self, scene: str) -> Dict:
        """获取基于场景的推荐（含LLM智能解读）"""
        songs = self.library.get_by_scene(scene)
        if not songs:
            songs = self.library.get_random(5)

        if scene == "跑步":
            songs.sort(key=lambda s: s.tempo, reverse=True)
        else:
            songs.sort(key=lambda s: s.energy)

        songs_dict = [self._song_to_dict(s) for s in songs[:6]]
        llm_response = self.llm.recommend_by_scene(scene, songs_dict)

        return {
            "scene": scene,
            "songs": songs_dict,
            "llm_analysis": llm_response,
            "total_found": len(songs)
        }

    def get_daily_recommendations(self, count: int = 8) -> Dict:
        """获取每日推荐（混合多种情绪）"""
        all_songs = self.library.get_all()

        selected = []
        moods_covered = set()

        for song in all_songs:
            if len(selected) >= count:
                break
            song_moods = set(song.mood)
            if not song_moods.issubset(moods_covered):
                selected.append(song)
                moods_covered.update(song_moods)

        while len(selected) < count and len(selected) < len(all_songs):
            candidate = self.library.get_random(1)[0]
            if candidate not in selected:
                selected.append(candidate)

        import random
        random.shuffle(selected)
        songs_dict = [self._song_to_dict(s) for s in selected]

        llm_response = self.llm.generate_playlist_insight(songs_dict)

        return {
            "songs": songs_dict,
            "llm_insight": llm_response,
            "mood_coverage": list(moods_covered)
        }

    def search_songs(self, query: str) -> List[Dict]:
        """搜索歌曲"""
        songs = self.library.search(query)
        return [self._song_to_dict(s) for s in songs]

    def get_song_by_id(self, song_id: str) -> Optional[Dict]:
        """获取单首歌曲详情"""
        song = self.library.get_by_id(song_id)
        return self._song_to_dict(song) if song else None

    def _song_to_dict(self, song: Song) -> Dict:
        """歌曲对象转字典"""
        return {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "album": song.album,
            "duration": song.duration,
            "duration_str": song.duration_str,
            "genre": song.genre,
            "mood": song.mood,
            "scene": song.scene,
            "tempo": song.tempo,
            "energy": song.energy,
            "description": song.description,
            "year": song.year,
            "cover": song.cover_url
        }


class MusicKnowledgeService:
    """音乐知识服务"""

    def __init__(self, llm: BaseLLMEngine = None):
        self.kb = KnowledgeBase()
        # 外部传入引擎，或工厂创建（确保全局唯一实例）
        self.llm = llm or LLMEngineFactory.create()

    def ask(self, question: str) -> Dict:
        """处理音乐知识问答"""
        knowledge_items = self.kb.search(question)

        if knowledge_items:
            best_match = knowledge_items[0]
            knowledge_dict = {
                "question": best_match.question,
                "answer": best_match.answer,
                "category": best_match.category,
                "difficulty": best_match.difficulty,
                "related_songs": best_match.related_songs
            }
            llm_response = self.llm.answer_knowledge_question(question, knowledge_dict)
            source = "knowledge_base"
        else:
            llm_response = self.llm.answer_knowledge_question(question, None)
            source = "llm_general"
            knowledge_dict = None

        return {
            "question": question,
            "answer": llm_response,
            "matched_knowledge": knowledge_dict,
            "source": source,
            "related_questions": self._get_related_questions(question)
        }

    def get_categories(self) -> List[str]:
        """获取知识分类"""
        return list(set(k.category for k in self.kb.get_all()))

    def get_knowledge_by_category(self, category: str) -> List[Dict]:
        """按分类获取知识"""
        items = self.kb.get_by_category(category)
        return [{
            "question": k.question,
            "category": k.category,
            "difficulty": k.difficulty
        } for k in items]

    def _get_related_questions(self, question: str) -> List[str]:
        """获取相关问题"""
        all_questions = [k.question for k in self.kb.get_all()]
        import random
        return random.sample(all_questions, min(3, len(all_questions)))
