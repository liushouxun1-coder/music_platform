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
    # 获取方式：在 Spotify 网页版找到歌曲 → 分享 → 复制链接
    # 链接格式：https://open.spotify.com/track/XXXXXXXXXX
    # 提取 XXXXXXXXXX 部分作为 ID
    _TRACK_MAP: Dict[str, str] = {
        # 中文歌曲
        "稻香":"69pyHCoBn4Ki0BzDJ2xPGI",
        "逆光":"4x1hB3Yg01Aq6J6q0deS9M",
        "平凡之路":"3YFGh5Kga1K40yUhuCVffM",
        "夜的第七章":"1IqO5tjlh7uSkstlaFCQke",
        "凉凉":"2OKQ6fSyc88ZcKQMjGIdMj",
        "海浪":"5EpLeWSwqOG0mZW0R4WdKQ",
        "山海":"0VUORVhLmsxKTSwg4P9CrB",
        "丑":"5Kc0fVPgQ808lwikSxCh70",
        "阳光宅男": "5pFCvT5Vq9B8Kx58A8sVI5",
        "小幸运": "2zapgrglLRISEUlspPtdep",
        "后来": "2wzXhxWPX0aODraKNXoJYY",
        "消愁": "7x3WCjRe4YW0z6W1OxOvc1",
        "孤勇者": "6akVETVeqqPVvuBS5e0EB1",
        "奔跑": "5rGcsWV67Z4K8f52vhyW82",
        "天空之城": "4LwucQallV2W12OqJoLMBl",
        "故乡的原风景": "3jyhGjqueIqmJQR62nMFMR",
        # 英文歌曲
        "Shake It Off":"0cqRj7pUJDkTCEsJkx8snD",
        "Blinding Lights":"0VjIjW4GlUZAMYd2vXMi3b",
        "Lose Yourself":"5Z01UMMf7V1o0MzF86s6WJ",
        "Imagine":"7pKfPomDEeI4TPT6EOYjn9",
        "Bohemian Rhapsody":"3z8h0TU7ReDPLIbEnYhWZb",
        "Shape of You":"7qiZfU4dY1lWllzX7mPBI3",
        "Viva La Vida":"1mea3bSkSGXuIRvnydlB5b",
        "Bad Guy":"2Fxmhks0bxGSBdJ92vM42m",
        "Rolling in the Deep":"4OSBTYWVwsQhGLF9NHvIbR",
        "Clocks":"0BCPKOYdS2jbQ8iyB56Zns",
        "Hallelujah":"7yzbimr8WVyAtBX3Eg6UL9",
        "Thinking Out Loud":"34gCuhDGsG4bRPIf9bb02f",
        "Dance Monkey":"2XU0oxnq2qxCpomAAuJY8K",
        "Hotel California":"40riOy7x9W7GXjyGp4pjAv",
        "Something Just Like This":"6RUKPb4LETWmmr3iAEQktW",
        "City of Stars":"6XQHlsNu6so4PdglFkJQRJ",
        "Believer":"0pqnGHJpmpxLKifKRmU6WP",
        "Demons":"5qaEfEh1AtSdrdrByCP7qR",
        "Counting Stars":"2tpWsVSb9UEmDRxAl1zhX1",
        "Radioactive":"62yJjFtgkhUrXktIoSjgP2",
        "Stressed Out":"3CRDbSIZ4r5MsZ0YwxuEkn",
        "Ride":"2Z8WuEywRWYTKe1NybPQEW",
        "Heathens":"6i0V12jOa3mr6uu4WYhUBr",
        "Happier":"7BqHUALzNBTanL6OvsqmC1",
        "Silence":"7vGuf3Y35N4wmASOKLUVVU",
        "Faded":"698ItKASDavgwZ3WjaWjtz",
        "Alone":"3MEYFivt6bilQ9q9mFWZ4g",
        "The Spectre":"2DGa7iaidT5s0qnINlwMjJ",
        "Wake Me Up":"0nrRP2bk19rLc0orkWPQk2",
        "Waiting for Love":"2P4OICZRVAQcYAV2JReRfj",
        "Hey Jude":"1eT2CjXwFXNx6oY5ydvzKU",
        "Let It Be":"7iN1s7xHE4ifF5povM6A48",
        "Yesterday":"3BQHpFgAp4l80e1XslIjNI",
        "happy": "60nZcImufyMA1MKQY3dcCH",
        "someone like you": "4kflIGfjdZJW4ot2ioixTB",
        "we will rock you": "4pbJqGIASGPr0ZpGpnWkDn",
        "eye of the tiger": "2HHtWyy5CgaQbC7XSoOb0e",
        "titanium": "2i1AVZAYLhrQTvzr1hu7Jt",
        "weightless": "6kkwzB6hXLIONkEk9JciA6",
        "river flows in you": "5PjJaAZVDKWZYdMo45wNQY",
        "a thousand years": "6lanRgr6wXibZr8KgzXxBl",
        "canon in d": "1c3GkbZBnyrQ1cm4TGHFrK",

        # 古典/纯音乐
        "月光奏鸣曲": "7gzxvyjcuX5RxX4y2rJoPV",
        "夜曲": "25oQ0Gd3BLH3haQK0dGmuZ",
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