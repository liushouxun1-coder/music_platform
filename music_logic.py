"""精简版音乐业务逻辑"""
from typing import List, Dict, Optional
from music_data import MusicLibrary, KnowledgeBase
from llm_engine import LLMEngineFactory, BaseLLMEngine
import random


class MusicRecommender:
    def __init__(self, llm: BaseLLMEngine = None):
        self.library = MusicLibrary()
        self.llm = llm or LLMEngineFactory.create()

    def get_mood_recommendations(self, mood: str) -> Dict:
        songs = self.library.get_by_mood(mood) or self.library.get_random(5)
        songs.sort(key=lambda s: s.energy, reverse=True)
        sd = [s.to_dict() for s in songs[:6]]
        return {"mood": mood, "songs": sd, "llm_analysis": self.llm.recommend_by_mood(mood, sd), "total_found": len(songs)}

    def get_scene_recommendations(self, scene: str) -> Dict:
        songs = self.library.get_by_scene(scene) or self.library.get_random(5)
        songs.sort(key=lambda s: s.tempo if scene == "跑步" else s.energy, reverse=(scene == "跑步"))
        sd = [s.to_dict() for s in songs[:6]]
        return {"scene": scene, "songs": sd, "llm_analysis": self.llm.recommend_by_scene(scene, sd), "total_found": len(songs)}

    def get_daily_recommendations(self, count: int = 8) -> Dict:
        all_songs = self.library.get_all()
        selected, moods = [], set()
        for s in all_songs:
            if len(selected) >= count: break
            if not set(s.mood).issubset(moods):
                selected.append(s); moods.update(s.mood)
        while len(selected) < count:
            c = self.library.get_random(1)[0]
            if c not in selected: selected.append(c)
        random.shuffle(selected)
        sd = [s.to_dict() for s in selected]
        return {"songs": sd, "llm_insight": self.llm.generate_playlist_insight(sd), "mood_coverage": list(moods)}

    def search_songs(self, q: str) -> List[Dict]: return [s.to_dict() for s in self.library.search(q)]
    def get_song_by_id(self, sid: str) -> Optional[Dict]: return (s := self.library.get_by_id(sid)) and s.to_dict()


class MusicKnowledgeService:
    def __init__(self, llm: BaseLLMEngine = None):
        self.kb = KnowledgeBase()
        self.llm = llm or LLMEngineFactory.create()

    def ask(self, question: str) -> Dict:
        items = self.kb.search(question)
        if items:
            k = items[0]
            kd = {"question": k.question, "answer": k.answer, "category": k.category, "difficulty": k.difficulty, "related_songs": k.related_songs}
            return {"question": question, "answer": self.llm.answer_knowledge_question(question, kd), "matched_knowledge": kd, "source": "knowledge_base", "related_questions": self._related(question)}
        return {"question": question, "answer": self.llm.answer_knowledge_question(question), "matched_knowledge": None, "source": "llm_general", "related_questions": self._related(question)}

    def get_categories(self) -> List[str]: return list(set(k.category for k in self.kb.get_all()))
    def get_knowledge_by_category(self, cat: str) -> List[Dict]: return [{"question": k.question, "category": k.category, "difficulty": k.difficulty} for k in self.kb.get_by_category(cat)]
    def _related(self, q: str) -> List[str]: return random.sample([k.question for k in self.kb.get_all()], min(3, len(self.kb.get_all())))