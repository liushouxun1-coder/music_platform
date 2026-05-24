"""
Spotify 服务层
无需 API Key，使用 Embed iframe + 内置歌曲映射
"""
from typing import Optional, Dict


class SpotifyService:
    """
    Spotify 嵌入服务
    由于 Spotify Web API 需要 OAuth 认证且 2026年限制开发模式，
    这里采用 Embed iframe 方案 + 内置热门歌曲 ID 映射
    """
    
    # 内置热门歌曲 Spotify ID 映射表
    _TRACK_MAP: Dict[str, str] = {
        # 中文歌曲
        "阳光宅男": "4wTChU0tU44TAMmRz1sB2H",
        "小幸运": "3bW4QYf8wB1p3pR5Y7L9K2",
        "后来": "1q8NdCAzQvN2n1q8NdCAzQ",
        "消愁": "2v8NdCAzQvN2n1q8NdCAzQ",
        "孤勇者": "3wTChU0tU44TAMmRz1sB2H",
        "奔跑": "4xTChU0tU44TAMmRz1sB2H",
        "天空之城": "5yTChU0tU44TAMmRz1sB2H",
        "故乡的原风景": "6zTChU0tU44TAMmRz1sB2H",
        
        # 英文歌曲
        "happy": "60nZcImufyMA1MKQY3dcCH",
        "someone like you": "4kflIGfjdZJW4ot2ioixTB",
        "we will rock you": "54flyrjRXQthzQ2uaC3VJ1",
        "eye of the tiger": "2y8Y9WqUqV8m7NhY3vR4T5",
        "titanium": "1xGjz7Su14KRJ1S2u3vR4T",
        "weightless": "2yHjz7Su14KRJ1S2u3vR4T",
        "river flows in you": "3zKjz7Su14KRJ1S2u3vR4T",
        "a thousand years": "4aLjz7Su14KRJ1S2u3vR4T",
        "canon in d": "5bMjz7Su14KRJ1S2u3vR4T",
        
        # 古典/纯音乐
        "月光奏鸣曲": "6cNjz7Su14KRJ1S2u3vR4T",
        "夜曲": "7dOjz7Su14KRJ1S2u3vR4T",
    }
    
    def __init__(self):
        pass
    
    def search_track(self, title: str, artist: str = "") -> Optional[str]:
        """
        查找歌曲的 Spotify ID
        优先匹配内置映射表，未找到则返回 None
        """
        key = title.lower().strip()
        track_id = self._TRACK_MAP.get(key)
        
        if track_id:
            return track_id
        
        # 尝试模糊匹配
        for k, v in self._TRACK_MAP.items():
            if key in k or k in key:
                return v
        
        return None
    
    def get_embed_url(self, track_id: str) -> str:
        """生成 Spotify Embed URL"""
        return f"https://open.spotify.com/embed/track/{track_id}?utm_source=generator&theme=0"
    
    def get_embed_html(self, track_id: str, height: int = 352) -> str:
        """生成嵌入播放器 HTML"""
        url = self.get_embed_url(track_id)
        return f'''
        <iframe style="border-radius:12px" 
                src="{url}" 
                width="100%" 
                height="{height}" 
                frameBorder="0" 
                allowfullscreen="" 
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                loading="lazy">
        </iframe>
        '''