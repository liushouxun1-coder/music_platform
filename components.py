"""精简版霓虹赛博朋克组件库 - 纯展示组件"""
import streamlit as st
from typing import List, Dict


class Theme:
    TEXT_PRIMARY = "#e0e0e0"
    TEXT_SECONDARY = "#888"
    TEXT_ACCENT = "#00f2fe"
    GRADIENT = "linear-gradient(90deg,#00f2fe,#ff00ff)"


# ========== 全局 CSS ==========
st.markdown("""
<style>
    .stButton > button {
        background: linear-gradient(135deg, #00f2fe, #ff00ff) !important;
        color: #000 !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0, 242, 254, 0.5) !important;
        filter: brightness(1.2) !important;
    }
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0a0a0a; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #00f2fe, #ff00ff); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


def _gradient_text(text: str, size: str = "1rem", bold: bool = True) -> str:
    b = "bold" if bold else "normal"
    return '<span style="font-size:' + size + ';font-weight:' + b + ';background:' + Theme.GRADIENT + ';-webkit-background-clip:text;-webkit-text-fill-color:transparent">' + text + '</span>'


# ========== 基础组件 ==========
def render_header(title: str, subtitle: str = ""):
    subtitle_html = '<div style="background:' + Theme.GRADIENT + ';-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-top:0.5rem">' + subtitle + '</div>' if subtitle else ''
    st.markdown("""
    <div style="text-align:center;margin-bottom:2rem">
        <div style="font-size:3rem;font-weight:bold;background:linear-gradient(90deg,#00f2fe,#4facfe,#ff00ff,#fee140);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-shadow:0 0 40px rgba(0,242,254,0.5)">""" + title + """</div>
        """ + subtitle_html + """
    </div>
    """, unsafe_allow_html=True)


def render_section_title(icon: str, title: str):
    st.markdown('<div style="font-size:1.8rem;font-weight:bold;background:' + Theme.GRADIENT + ';-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:1.5rem 0 1rem;padding-left:1rem;border-left:4px solid #00f2fe">' + icon + ' ' + title + '</div>', unsafe_allow_html=True)


def render_divider():
    st.markdown('<hr style="border:none;height:1px;background:linear-gradient(90deg,transparent,#00f2fe88,#ff00ff88,transparent);margin:2rem 0">', unsafe_allow_html=True)


# ========== Spotify 播放器 ==========
def render_spotify_player(track_id: str, title: str = ""):
    if not track_id:
        render_empty_state("🎵", "暂无 Spotify 音源", "该歌曲暂未收录到 Spotify")
        return

    embed_url = "https://open.spotify.com/embed/track/" + track_id + "?utm_source=generator&theme=0"

    st.markdown("""
    <div style="
        background: rgba(0, 242, 254, 0.03);
        backdrop-filter: blur(20px) saturate(200%);
        -webkit-backdrop-filter: blur(20px) saturate(200%);
        border: 1px solid rgba(0, 242, 254, 0.15);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 242, 254, 0.1);
    ">
        <iframe style="border-radius:12px" 
                src=""" + embed_url + """" 
                width="100%" 
                height="352" 
                frameBorder="0" 
                allowfullscreen="" 
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                loading="lazy">
        </iframe>
    </div>
    """, unsafe_allow_html=True)


# ========== 歌曲卡片（纯展示，无按钮）==========
def render_song_card_spotify(song: Dict, key_prefix: str = "song"):
    """纯展示卡片，按钮在 app.py 中独立创建"""

    has_spotify = song.get("spotify_id") is not None
    mood_colors = {"欢快": "#ff00ff", "悲伤": "#00f2fe", "愉悦": "#fee140", "激昂": "#ff6b6b", "平静": "#00f2fe", "温暖": "#ff00ff"}
    mood = song.get("mood", ["流行"])[0]
    bc = mood_colors.get(mood, "#00f2fe")
    e = song.get("energy", 0.5)

    spotify_badge = "🎵 Spotify" if has_spotify else "❌ 暂无音源"
    badge_color = "#1DB954" if has_spotify else "#999"
    tags = " ".join(["#" + m for m in song.get("mood", [])])

    st.markdown("""
    <div style="
        background: rgba(0, 242, 254, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid """ + bc + """44;
        border-left: 4px solid """ + bc + """;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 8px 32px """ + bc + """22;
    ">
        <div style="display:flex;align-items:center;gap:1rem">
            <div style="font-size:2.5rem;min-width:3rem;text-align:center">""" + song.get("cover", "🎵") + """</div>
            <div style="flex:1">
                <div style="font-size:1.1rem;font-weight:bold;color:#fff">""" + song["title"] + """ <span style="color:""" + badge_color + """;font-size:0.75rem">● """ + spotify_badge + """</span></div>
                <div style="color:""" + Theme.TEXT_SECONDARY + """;font-size:0.9rem">""" + song["artist"] + " · " + song.get("album", "") + " · " + str(song.get("year", "")) + """</div>
                <div style="margin:0.4rem 0">""" + tags + """</div>
                <div style="display:flex;align-items:center;gap:0.5rem;margin-top:0.5rem">
                    <span style="color:""" + Theme.TEXT_SECONDARY + """;font-size:0.8rem">⚡</span>
                    <div style="flex:1;background:rgba(255,255,255,0.05);height:4px;border-radius:2px;overflow:hidden">
                        <div style="background:linear-gradient(90deg,#00f2fe,#ff00ff);width:""" + str(e*100) + """%;height:100%;border-radius:2px;box-shadow:0 0 8px rgba(0,242,254,0.5)"></div>
                    </div>
                    <span style="color:""" + Theme.TEXT_SECONDARY + """;font-size:0.75rem">""" + str(song.get("tempo", 120)) + " BPM · " + song.get("duration_str", "3:00") + """</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_compact_card_spotify(song: Dict, key_prefix: str = "compact"):
    """紧凑型纯展示卡片"""
    has_spotify = song.get("spotify_id") is not None
    badge = "🎵" if has_spotify else "❌"

    st.markdown("""
    <div style="
        background: rgba(0, 242, 254, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 242, 254, 0.15);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin: 0.3rem 0;
    ">
        <div style="font-size:2.5rem;margin-bottom:0.5rem">""" + song.get("cover", "🎵") + """</div>
        <div style="font-weight:bold;color:#fff;font-size:0.95rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">""" + song["title"] + """</div>
        <div style="color:""" + Theme.TEXT_SECONDARY + """;font-size:0.8rem;margin:0.3rem 0">""" + song["artist"] + """</div>
        <span style="background:rgba(0,242,254,0.2);padding:0.2rem 0.5rem;border-radius:8px;font-size:0.7rem;color:#00f2fe">""" + badge + " " + song.get("mood", ["流行"])[0] + """</span>
    </div>
    """, unsafe_allow_html=True)


# ========== LLM 组件 ==========
def render_llm_thinking(content: str, confidence: float = 0.9, expanded: bool = True):
    with st.expander("🔍 AI 推理过程", expanded=expanded):
        st.markdown("""
        <div style="
            background: rgba(0, 242, 254, 0.04);
            backdrop-filter: blur(16px);
            border-left: 3px solid #00f2fe;
            border-radius: 0 8px 8px 0;
            padding: 1rem;
            font-size: 0.9rem;
            color: """ + Theme.TEXT_PRIMARY + """;
        ">
            <div style="font-weight:bold;margin-bottom:0.5rem;background:""" + Theme.GRADIENT + """;-webkit-background-clip:text;-webkit-text-fill-color:transparent">🤖 AI 思考中...</div>
            <div style="line-height:1.6">""" + content.replace(chr(10), "<br>") + """</div>
            <div style="margin-top:0.8rem;padding-top:0.5rem;border-top:1px solid rgba(0,242,254,0.2)">
                <span style="font-size:0.8rem;color:""" + Theme.TEXT_SECONDARY + """>置信度：""" + str(int(confidence*100)) + """%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_llm_response(content: str, title: str = "🤖 AI 回复"):
    st.markdown("""
    <div style="
        background: rgba(0, 242, 254, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
    ">
        <div style="font-weight:bold;background:""" + Theme.GRADIENT + """;-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:0.8rem;font-size:1.1rem">""" + title + """</div>
        <div style="line-height:1.7;font-size:0.95rem;color:""" + Theme.TEXT_PRIMARY + """>""" + content.replace(chr(10), "<br>") + """</div>
    </div>
    """, unsafe_allow_html=True)


# ========== 选择器 ==========
def render_mood_selector(moods: List[tuple]):
    st.markdown(_gradient_text("选择您当前的情绪状态", "1.2rem"), unsafe_allow_html=True)
    selected = None
    gradients = {"mood-happy": "linear-gradient(135deg,#ff00ff,#f5576c)", "mood-sad": "linear-gradient(135deg,#00f2fe,#4facfe)",
                 "mood-joy": "linear-gradient(135deg,#fee140,#fa709a)", "mood-excited": "linear-gradient(135deg,#ff6b6b,#fee140)",
                 "mood-calm": "linear-gradient(135deg,#00f2fe,#4facfe)"}
    for col, (mood, cls, emoji) in zip(st.columns(len(moods)), moods):
        with col:
            bg = gradients.get(cls, Theme.GRADIENT)
            tc = "#000" if cls == "mood-joy" else "#fff"
            st.markdown("""
            <div style="background:""" + bg + """;border-radius:16px;padding:1.2rem;text-align:center;margin:0.3rem 0;box-shadow:0 8px 32px rgba(0,0,0,0.3)">
                <div style="font-size:2.5rem;text-shadow:0 0 20px rgba(255,255,255,0.5)">""" + emoji + """</div>
                <div style="font-weight:bold;color:""" + tc + """;margin-top:0.5rem;font-size:1.1rem;text-shadow:0 2px 10px rgba(0,0,0,0.3)">""" + mood + """</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("选择", key="ms_" + mood, use_container_width=True): selected = mood
    return selected


def render_scene_selector(scenes: List[tuple]):
    st.markdown(_gradient_text("选择您当前的场景", "1.2rem"), unsafe_allow_html=True)
    selected = None
    for col, (scene, emoji, desc) in zip(st.columns(len(scenes)), scenes):
        with col:
            st.markdown("""
            <div style="
                background: rgba(0, 242, 254, 0.03);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(0, 242, 254, 0.2);
                border-radius: 16px;
                padding: 1.5rem 1rem;
                text-align: center;
                margin: 0.3rem 0;
            ">
                <div style="font-size:2.5rem;margin-bottom:0.5rem">""" + emoji + """</div>
                <div style="font-weight:bold;color:#fff;font-size:1.2rem;margin:0.5rem 0">""" + scene + """</div>
                <div style="color:""" + Theme.TEXT_SECONDARY + """;font-size:0.85rem">""" + desc + """</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("进入场景", key="ss_" + scene, use_container_width=True): selected = scene
    return selected


# ========== 聊天组件 ==========
def render_chat_message(role: str, content: str, reasoning: str = "", confidence: float = 0.9):
    if role == "user":
        st.markdown("""
        <div style="
            background: rgba(0, 242, 254, 0.06);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(0, 242, 254, 0.2);
            border-radius: 12px 12px 0 12px;
            padding: 1rem;
            margin: 0.5rem 0 0.5rem 15%;
            color: """ + Theme.TEXT_PRIMARY + """;
        ">
            <div style="font-weight:bold;margin-bottom:0.3rem;background:linear-gradient(90deg,#00f2fe,#4facfe);-webkit-background-clip:text;-webkit-text-fill-color:transparent">👤 您</div>
            <div style="line-height:1.5">""" + content + """</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        r = ""
        if reasoning:
            r = '<div style="margin-top:0.8rem;padding-top:0.5rem;border-top:1px solid rgba(255,0,255,0.2)"><small style="color:' + Theme.TEXT_SECONDARY + '">💭 ' + reasoning[:80] + ("..." if len(reasoning) > 80 else "") + " | 置信度：" + str(int(confidence*100)) + "%</small></div>"
        st.markdown("""
        <div style="
            background: rgba(255, 0, 255, 0.05);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 0, 255, 0.2);
            border-radius: 12px 12px 12px 0;
            padding: 1rem;
            margin: 0.5rem 15% 0.5rem 0;
            color: """ + Theme.TEXT_PRIMARY + """;
        ">
            <div style="font-weight:bold;margin-bottom:0.3rem;background:linear-gradient(90deg,#ff00ff,#fee140);-webkit-background-clip:text;-webkit-text-fill-color:transparent">🤖 AI 音乐导师</div>
            <div style="line-height:1.6">""" + content.replace(chr(10), "<br>") + """</div>""" + r + """
        </div>
        """, unsafe_allow_html=True)


def render_chat_history(history: List[Dict]):
    for m in history: render_chat_message(m.get("role", "user"), m.get("content", ""), m.get("reasoning", ""), m.get("confidence", 0.9))


# ========== 状态组件 ==========
def render_loading_spinner(text: str = "AI 思考中..."):
    return st.spinner("🧠 " + text)


def render_empty_state(icon: str, title: str, description: str):
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        text-align: center;
        padding: 3rem 1rem;
        margin: 1rem 0;
    ">
        <div style="font-size:3rem;margin-bottom:1rem">""" + icon + """</div>
        <div style="font-size:1.2rem;font-weight:bold;color:#fff;margin-bottom:0.5rem">""" + title + """</div>
        <div style="font-size:0.9rem;color:""" + Theme.TEXT_SECONDARY + """>""" + description + """</div>
    </div>
    """, unsafe_allow_html=True)


def render_notification(message: str, type_: str = "info"):
    colors = {"info": "#00f2fe", "success": "#2ecc71", "warning": "#fee140", "error": "#ff00ff"}
    c = colors.get(type_, "#00f2fe")
    icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
    icon = icons.get(type_, "ℹ️")
    st.markdown("""
    <div style="
        background: """ + c + """15;
        backdrop-filter: blur(12px);
        border-left: 3px solid """ + c + """;
        padding: 0.8rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        color: """ + Theme.TEXT_PRIMARY + """;
    ">
        <span style="color:""" + c + """;font-weight:bold">""" + icon + """</span> """ + message + """
    </div>
    """, unsafe_allow_html=True)