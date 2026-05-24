"""精简版霓虹赛博朋克组件库"""
import streamlit as st
from typing import List, Dict, Optional, Callable


class Theme:
    BG_CARD = "rgba(0,242,254,0.06)"
    TEXT_PRIMARY = "#e0e0e0"
    TEXT_SECONDARY = "#888"
    TEXT_ACCENT = "#00f2fe"
    TEXT_ACCENT2 = "#ff00ff"
    BORDER = "rgba(0,242,254,0.2)"
    GRADIENT = "linear-gradient(90deg,#00f2fe,#ff00ff)"


def _gradient_text(text: str, size: str = "1rem", bold: bool = True) -> str:
    b = "bold" if bold else "normal"
    return f'<span style="font-size:{size};font-weight:{b};background:{Theme.GRADIENT};-webkit-background-clip:text;-webkit-text-fill-color:transparent">{text}</span>'


def _neon_box(content: str, border_color: str = Theme.TEXT_ACCENT, bg_alpha: str = "04") -> str:
    return f'<div style="background:rgba(0,242,254,0.{bg_alpha});border:1px solid {border_color}44;border-radius:12px;padding:1rem;margin:0.5rem 0;box-shadow:0 0 15px {border_color}22">{content}</div>'


# ========== 基础组件 ==========
def render_header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div style="text-align:center;margin-bottom:2rem">
        <div style="font-size:3rem;font-weight:bold;background:linear-gradient(90deg,#00f2fe,#4facfe,#ff00ff,#fee140);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-shadow:0 0 40px rgba(0,242,254,0.5)">{title}</div>
        {f'<div style="background:{Theme.GRADIENT};-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-top:0.5rem">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def render_section_title(icon: str, title: str):
    st.markdown(f'<div style="font-size:1.8rem;font-weight:bold;background:{Theme.GRADIENT};-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:1.5rem 0 1rem;padding-left:1rem;border-left:4px solid #00f2fe">{icon} {title}</div>', unsafe_allow_html=True)


def render_divider():
    st.markdown(f'<hr style="border:none;height:1px;background:linear-gradient(90deg,transparent,#00f2fe88,#ff00ff88,transparent);margin:2rem 0">', unsafe_allow_html=True)


# ========== 音乐卡片 ==========
def render_song_card_add(song: Dict, on_add: Optional[Callable] = None):
    mood_colors = {"欢快": "#ff00ff", "悲伤": "#00f2fe", "愉悦": "#fee140", "激昂": "#ff6b6b", "平静": "#00f2fe", "温暖": "#ff00ff"}
    mood = song.get("mood", ["流行"])[0]
    bc = mood_colors.get(mood, "#00f2fe")
    tags = " ".join([f'<span style="background:{bc}33;color:{bc};padding:0.15rem 0.5rem;border-radius:10px;font-size:0.75rem;margin-right:0.3rem">#{m}</span>' for m in song.get("mood", [])])
    e = song.get("energy", 0.5)
    ec = "#ff00ff" if e > 0.7 else "#fee140" if e > 0.4 else "#00f2fe"

    st.markdown(f"""
    <div style="background:rgba(0,242,254,0.03);border:1px solid {bc}44;border-left:4px solid {bc};border-radius:12px;padding:1rem;margin:0.5rem 0">
        <div style="display:flex;align-items:center;gap:1rem">
            <div style="font-size:2.5rem;min-width:3rem;text-align:center">{song.get("cover", "🎵")}</div>
            <div style="flex:1">
                <div style="font-size:1.1rem;font-weight:bold;color:#fff">{song["title"]}</div>
                <div style="color:{Theme.TEXT_SECONDARY};font-size:0.9rem">{song["artist"]} · {song.get("album","")} · {song.get("year","")}</div>
                <div style="margin:0.4rem 0">{tags}</div>
                <div style="display:flex;align-items:center;gap:0.5rem;margin-top:0.5rem">
                    <span style="color:{Theme.TEXT_SECONDARY};font-size:0.8rem">⚡</span>
                    <div style="flex:1;background:rgba(255,255,255,0.05);height:4px;border-radius:2px">
                        <div style="background:linear-gradient(90deg,#00f2fe,#ff00ff);width:{e*100}%;height:100%;border-radius:2px"></div>
                    </div>
                    <span style="color:{Theme.TEXT_SECONDARY};font-size:0.75rem">{song.get("tempo",120)} BPM · {song.get("duration_str","3:00")}</span>
                </div>
                <div style="color:{Theme.TEXT_SECONDARY};font-size:0.8rem;margin-top:0.3rem">{song.get("description","")}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if on_add and st.button("➕ 加入播放列表", key=f"sa_{song['id']}", use_container_width=True):
        on_add(song)


def render_compact_card_add(song: Dict, on_add: Optional[Callable] = None):
    st.markdown(f"""
    <div style="background:rgba(0,242,254,0.03);border:1px solid rgba(0,242,254,0.15);border-radius:12px;padding:1rem;text-align:center;margin:0.3rem 0">
        <div style="font-size:2.5rem;margin-bottom:0.5rem">{song.get("cover","🎵")}</div>
        <div style="font-weight:bold;color:#fff;font-size:0.95rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{song["title"]}</div>
        <div style="color:{Theme.TEXT_SECONDARY};font-size:0.8rem;margin:0.3rem 0">{song["artist"]}</div>
        <span style="background:rgba(0,242,254,0.2);padding:0.2rem 0.5rem;border-radius:8px;font-size:0.7rem;color:#00f2fe">{song.get("mood",["流行"])[0]}</span>
        <div style="color:{Theme.TEXT_SECONDARY};font-size:0.75rem;margin-top:0.3rem">{song.get("duration_str","3:00")}</div>
    </div>
    """, unsafe_allow_html=True)
    if on_add and st.button("➕", key=f"ca_{song['id']}", use_container_width=True):
        on_add(song)


def render_song_grid_add(songs: List[Dict], cols: int = 3, on_add: Optional[Callable] = None):
    for i in range(0, len(songs), cols):
        for col, s in zip(st.columns(cols), songs[i:i+cols]):
            with col: render_compact_card_add(s, on_add=on_add)


# ========== 播放器 ==========
def render_player(song: Dict, is_playing: bool, on_play_pause=None, on_next=None, on_prev=None, on_random=None, progress: float = 0.35):
    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.4);border:1px solid rgba(0,242,254,0.3);border-radius:16px;padding:1.5rem;margin:1rem 0;box-shadow:0 0 30px rgba(0,242,254,0.15)">
        <div style="display:flex;align-items:center;gap:1.5rem">
            <div style="font-size:3.5rem;min-width:4rem;text-align:center">{song.get("cover","🎵")}</div>
            <div style="flex:1">
                <div style="font-size:1.4rem;font-weight:bold;color:#fff">{song["title"]}</div>
                <div style="color:{Theme.TEXT_SECONDARY};margin:0.3rem 0">{song["artist"]} · {song.get("album","")} · {song.get("year","")}</div>
                <div style="display:flex;gap:0.5rem;margin:0.5rem 0">{" ".join([f'<span style="background:rgba(0,242,254,0.2);padding:0.2rem 0.6rem;border-radius:10px;font-size:0.8rem;color:#00f2fe">{m}</span>' for m in song.get("mood",[])])}</div>
            </div>
            <div style="text-align:right">
                <div style="font-size:2rem;color:#00f2fe">{"⏸️" if is_playing else "▶️"}</div>
                <div style="color:{Theme.TEXT_SECONDARY};font-size:0.85rem">{song.get("duration_str","3:00")}</div>
            </div>
        </div>
        <div style="margin-top:1.2rem">
            <div style="background:rgba(255,255,255,0.05);height:5px;border-radius:3px;overflow:hidden">
                <div style="background:linear-gradient(90deg,#00f2fe,#ff00ff);width:{progress*100}%;height:100%;border-radius:3px"></div>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:0.4rem;font-size:0.75rem;color:{Theme.TEXT_SECONDARY}">
                <span>{int(progress*180//60)}:{int(progress*180%60):02d}</span>
                <span>{song.get("duration_str","3:00")}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c = st.columns([1,1,1,1,1,2])
    if c[0].button("⏮️", key="pp") and on_prev: on_prev()
    if c[2].button("⏸️" if is_playing else "▶️", key="pt") and on_play_pause: on_play_pause()
    if c[4].button("⏭️", key="pn") and on_next: on_next()
    if c[5].button("🔀 随机", key="pr") and on_random: on_random()


# ========== LLM 组件 ==========
def render_llm_thinking(content: str, confidence: float = 0.9, expanded: bool = True):
    with st.expander("🔍 AI 推理过程", expanded=expanded):
        st.markdown(_neon_box(f"""
            <div style="font-weight:bold;margin-bottom:0.5rem;background:{Theme.GRADIENT};-webkit-background-clip:text;-webkit-text-fill-color:transparent">🤖 AI 思考中...</div>
            <div style="line-height:1.6">{content.replace(chr(10), "<br>")}</div>
            <div style="margin-top:0.8rem;padding-top:0.5rem;border-top:1px solid rgba(0,242,254,0.2)">
                <span style="font-size:0.8rem;color:{Theme.TEXT_SECONDARY}">置信度：{confidence*100:.0f}%</span>
            </div>
        """, Theme.TEXT_ACCENT, "04"), unsafe_allow_html=True)


def render_llm_response(content: str, title: str = "🤖 AI 回复"):
    st.markdown(_neon_box(f"""
        <div style="font-weight:bold;background:{Theme.GRADIENT};-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:0.8rem;font-size:1.1rem">{title}</div>
        <div style="line-height:1.7;font-size:0.95rem">{content.replace(chr(10), "<br>")}</div>
    """, Theme.TEXT_ACCENT, "05"), unsafe_allow_html=True)


# ========== 选择器 ==========
def render_mood_selector(moods: List[tuple]) -> Optional[str]:
    st.markdown(_gradient_text("选择您当前的情绪状态", "1.2rem"), unsafe_allow_html=True)
    selected = None
    gradients = {"mood-happy": "linear-gradient(135deg,#ff00ff,#f5576c)", "mood-sad": "linear-gradient(135deg,#00f2fe,#4facfe)",
                 "mood-joy": "linear-gradient(135deg,#fee140,#fa709a)", "mood-excited": "linear-gradient(135deg,#ff6b6b,#fee140)",
                 "mood-calm": "linear-gradient(135deg,#00f2fe,#4facfe)"}
    for col, (mood, cls, emoji) in zip(st.columns(len(moods)), moods):
        with col:
            bg = gradients.get(cls, Theme.GRADIENT)
            tc = "#000" if cls == "mood-joy" else "#fff"
            st.markdown(f'<div style="background:{bg};border-radius:16px;padding:1.2rem;text-align:center;margin:0.3rem 0"><div style="font-size:2.5rem">{emoji}</div><div style="font-weight:bold;color:{tc};margin-top:0.5rem;font-size:1.1rem">{mood}</div></div>', unsafe_allow_html=True)
            if st.button("选择", key=f"ms_{mood}", use_container_width=True): selected = mood
    return selected


def render_scene_selector(scenes: List[tuple]) -> Optional[str]:
    st.markdown(_gradient_text("选择您当前的场景", "1.2rem"), unsafe_allow_html=True)
    selected = None
    for col, (scene, emoji, desc) in zip(st.columns(len(scenes)), scenes):
        with col:
            st.markdown(f"""
            <div style="background:rgba(0,242,254,0.05);border:1px solid rgba(0,242,254,0.2);border-radius:16px;padding:1.5rem 1rem;text-align:center;margin:0.3rem 0">
                <div style="font-size:2.5rem;margin-bottom:0.5rem">{emoji}</div>
                <div style="font-weight:bold;color:#fff;font-size:1.2rem;margin:0.5rem 0">{scene}</div>
                <div style="color:{Theme.TEXT_SECONDARY};font-size:0.85rem">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("进入场景", key=f"ss_{scene}", use_container_width=True): selected = scene
    return selected


# ========== 聊天组件 ==========
def render_chat_message(role: str, content: str, reasoning: str = "", confidence: float = 0.9):
    if role == "user":
        st.markdown(f"""
        <div style="background:rgba(0,242,254,0.08);border:1px solid rgba(0,242,254,0.2);border-radius:12px 12px 0 12px;padding:1rem;margin:0.5rem 0 0.5rem 15%;color:{Theme.TEXT_PRIMARY}">
            <div style="font-weight:bold;margin-bottom:0.3rem;background:linear-gradient(90deg,#00f2fe,#4facfe);-webkit-background-clip:text;-webkit-text-fill-color:transparent">👤 您</div>
            <div style="line-height:1.5">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        r = f'<div style="margin-top:0.8rem;padding-top:0.5rem;border-top:1px solid rgba(255,0,255,0.2)"><small style="color:{Theme.TEXT_SECONDARY}">💭 {reasoning[:80]}{"..." if len(reasoning)>80 else ""} | 置信度：{confidence*100:.0f}%</small></div>' if reasoning else ""
        st.markdown(f"""
        <div style="background:rgba(255,0,255,0.06);border:1px solid rgba(255,0,255,0.2);border-radius:12px 12px 12px 0;padding:1rem;margin:0.5rem 15% 0.5rem 0;color:{Theme.TEXT_PRIMARY}">
            <div style="font-weight:bold;margin-bottom:0.3rem;background:linear-gradient(90deg,#ff00ff,#fee140);-webkit-background-clip:text;-webkit-text-fill-color:transparent">🤖 AI 音乐导师</div>
            <div style="line-height:1.6">{content.replace(chr(10), "<br>")}</div>{r}
        </div>
        """, unsafe_allow_html=True)


def render_chat_history(history: List[Dict]):
    for m in history: render_chat_message(m.get("role","user"), m.get("content",""), m.get("reasoning",""), m.get("confidence",0.9))


# ========== 状态组件 ==========
def render_loading_spinner(text: str = "AI 思考中..."):
    return st.spinner(f"🧠 {text}")


def render_empty_state(icon: str, title: str, description: str):
    st.markdown(f"""
    <div style="text-align:center;padding:3rem 1rem;color:{Theme.TEXT_SECONDARY}">
        <div style="font-size:3rem;margin-bottom:1rem">{icon}</div>
        <div style="font-size:1.2rem;font-weight:bold;color:#fff;margin-bottom:0.5rem">{title}</div>
        <div style="font-size:0.9rem">{description}</div>
    </div>
    """, unsafe_allow_html=True)


def render_notification(message: str, type_: str = "info"):
    colors = {"info": "#00f2fe", "success": "#2ecc71", "warning": "#fee140", "error": "#ff00ff"}
    c, icon = colors.get(type_, "#00f2fe"), {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}.get(type_, "ℹ️")
    st.markdown(f'<div style="background:{c}15;border-left:3px solid {c};padding:0.8rem 1rem;border-radius:0 8px 8px 0;margin:0.5rem 0"><span style="color:{c};font-weight:bold">{icon}</span> {message}</div>', unsafe_allow_html=True)

# ========== Spotify 组件 ==========

def render_spotify_player(track_id: str, title: str = ""):
    """渲染 Spotify 嵌入播放器"""
    if not track_id:
        render_empty_state("🎵", "暂无 Spotify 音源", "该歌曲暂未收录到 Spotify")
        return
    
    embed_url = f"https://open.spotify.com/embed/track/{track_id}?utm_source=generator&theme=0"
    
    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.4);border:1px solid rgba(0,242,254,0.3);border-radius:16px;padding:1rem;margin:1rem 0;box-shadow:0 0 30px rgba(0,242,254,0.15)">
        <iframe style="border-radius:12px" 
                src="{embed_url}" 
                width="100%" 
                height="352" 
                frameBorder="0" 
                allowfullscreen="" 
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                loading="lazy">
        </iframe>
    </div>
    """, unsafe_allow_html=True)


def render_song_card_spotify(song: Dict, on_add: Optional[Callable] = None, on_play: Optional[Callable] = None):
    """渲染带 Spotify 状态的歌曲卡片"""
    has_spotify = song.get("spotify_id") is not None
    spotify_badge = f'<span style="background:#1DB95433;color:#1DB954;padding:0.15rem 0.5rem;border-radius:10px;font-size:0.75rem;margin-left:0.5rem">🎵 Spotify</span>' if has_spotify else f'<span style="background:#666633;color:#999;padding:0.15rem 0.5rem;border-radius:10px;font-size:0.75rem;margin-left:0.5rem">❌ 暂无音源</span>'
    
    mood_colors = {"欢快": "#ff00ff", "悲伤": "#00f2fe", "愉悦": "#fee140", "激昂": "#ff6b6b", "平静": "#00f2fe", "温暖": "#ff00ff"}
    mood = song.get("mood", ["流行"])[0]
    bc = mood_colors.get(mood, "#00f2fe")
    tags = " ".join([f'<span style="background:{bc}33;color:{bc};padding:0.15rem 0.5rem;border-radius:10px;font-size:0.75rem;margin-right:0.3rem">#{m}</span>' for m in song.get("mood", [])])
    e = song.get("energy", 0.5)

    st.markdown(f"""
    <div style="background:rgba(0,242,254,0.03);border:1px solid {bc}44;border-left:4px solid {bc};border-radius:12px;padding:1rem;margin:0.5rem 0">
        <div style="display:flex;align-items:center;gap:1rem">
            <div style="font-size:2.5rem;min-width:3rem;text-align:center">{song.get("cover", "🎵")}</div>
            <div style="flex:1">
                <div style="font-size:1.1rem;font-weight:bold;color:#fff">{song["title"]}{spotify_badge}</div>
                <div style="color:{Theme.TEXT_SECONDARY};font-size:0.9rem">{song["artist"]} · {song.get("album","")} · {song.get("year","")}</div>
                <div style="margin:0.4rem 0">{tags}</div>
                <div style="display:flex;align-items:center;gap:0.5rem;margin-top:0.5rem">
                    <span style="color:{Theme.TEXT_SECONDARY};font-size:0.8rem">⚡</span>
                    <div style="flex:1;background:rgba(255,255,255,0.05);height:4px;border-radius:2px">
                        <div style="background:linear-gradient(90deg,#00f2fe,#ff00ff);width:{e*100}%;height:100%;border-radius:2px"></div>
                    </div>
                    <span style="color:{Theme.TEXT_SECONDARY};font-size:0.75rem">{song.get("tempo",120)} BPM · {song.get("duration_str","3:00")}</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns([1, 1])
    if has_spotify and on_play and cols[0].button("▶️ Spotify 播放", key=f"sp_{song['id']}", use_container_width=True):
        on_play(song)
    if on_add and cols[1].button("➕ 加入列表", key=f"sa_{song['id']}", use_container_width=True):
        on_add(song)


def render_compact_card_spotify(song: Dict, on_add: Optional[Callable] = None, on_play: Optional[Callable] = None):
    """紧凑型 Spotify 卡片"""
    has_spotify = song.get("spotify_id") is not None
    badge = "🎵" if has_spotify else "❌"
    
    st.markdown(f"""
    <div style="background:rgba(0,242,254,0.03);border:1px solid rgba(0,242,254,0.15);border-radius:12px;padding:1rem;text-align:center;margin:0.3rem 0">
        <div style="font-size:2.5rem;margin-bottom:0.5rem">{song.get("cover","🎵")}</div>
        <div style="font-weight:bold;color:#fff;font-size:0.95rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{song["title"]}</div>
        <div style="color:{Theme.TEXT_SECONDARY};font-size:0.8rem;margin:0.3rem 0">{song["artist"]}</div>
        <span style="background:rgba(0,242,254,0.2);padding:0.2rem 0.5rem;border-radius:8px;font-size:0.7rem;color:#00f2fe">{badge} {song.get("mood",["流行"])[0]}</span>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns([1, 1])
    if has_spotify and on_play and cols[0].button("▶️", key=f"cp_{song['id']}", use_container_width=True):
        on_play(song)
    if on_add and cols[1].button("➕", key=f"ca_{song['id']}", use_container_width=True):
        on_add(song)


def render_song_grid_spotify(songs: List[Dict], cols: int = 3, on_add: Optional[Callable] = None, on_play: Optional[Callable] = None):
    """Spotify 歌曲网格"""
    for i in range(0, len(songs), cols):
        for col, s in zip(st.columns(cols), songs[i:i+cols]):
            with col: render_compact_card_spotify(s, on_add=on_add, on_play=on_play)

# ========== 导出别名（兼容旧导入） ==========
render_song_card = render_song_card_add
render_compact_card = render_compact_card_add
render_song_grid = render_song_grid_add
render_mini_player = render_player