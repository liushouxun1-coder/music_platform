"""
components.py - 霓虹赛博朋克主题组件库
所有颜色通过 CSS 变量或参数传入，避免与 app.py 冲突
"""
import streamlit as st
from typing import List, Dict, Optional, Callable
import time


# ========== 主题配置（霓虹赛博朋克）==========
class Theme:
    """赛博朋克霓虹主题配置"""
    # 背景色 - 深黑底
    BG_PRIMARY = "#0a0a0a"           # 页面底层
    BG_SECONDARY = "#141414"         # 次层
    BG_CARD = "rgba(0,242,254,0.06)"  # 科技青微透卡片背景
    BG_PLAYER = "rgba(0,0,0,0.3)"     # 播放器背景
    BG_CHAT_USER = "rgba(0,242,254,0.08)"   # 用户消息 - 科技青
    BG_CHAT_ASSISTANT = "rgba(255,0,255,0.06)"  # AI消息 - 霓虹粉
    BG_LLM = "rgba(0,242,254,0.04)"  # LLM框

    # 文字色
    TEXT_PRIMARY = "#e0e0e0"         # 主文字
    TEXT_SECONDARY = "#888888"      # 次要文字
    TEXT_TITLE = "#ffffff"          # 标题纯白（会被渐变覆盖）
    TEXT_ACCENT = "#00f2fe"         # 科技青
    TEXT_ACCENT2 = "#ff00ff"        # 霓虹粉

    # 边框与装饰 - 霓虹光晕
    BORDER = "rgba(0,242,254,0.2)"
    BORDER_ACCENT = "#00f2fe"
    SHADOW = "rgba(0,242,254,0.3)"

    # 渐变 - 霓虹色系
    GRADIENT_PRIMARY = "linear-gradient(135deg, #00f2fe 0%, #ff00ff 100%)"
    GRADIENT_TITLE = "linear-gradient(90deg, #00f2fe 0%, #4facfe 30%, #ff00ff 70%, #fee140 100%)"
    GRADIENT_NEON = "linear-gradient(90deg, #00f2fe, #4facfe, #ff00ff, #fee140)"


# ========== 基础组件 ==========

def render_header(title: str, subtitle: str = ""):
    """渲染霓虹科技风页面头部"""
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:2rem; position:relative; z-index:1;">
        <div style="font-size:3rem; font-weight:bold;
                    background:linear-gradient(90deg, #00f2fe 0%, #4facfe 30%, #ff00ff 60%, #fee140 100%);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    text-shadow: 0 0 40px rgba(0,242,254,0.5), 0 0 80px rgba(255,0,255,0.3);">
            {title}
        </div>
        {f'<div style="background:linear-gradient(90deg, #00f2fe, #ff00ff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-top:0.5rem; font-size:1.1rem; text-shadow: 0 0 20px rgba(0,242,254,0.3);">{subtitle}</div>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def render_section_title(icon: str, title: str):
    """渲染霓虹板块标题"""
    st.markdown(f"""
    <div style="font-size:1.8rem; font-weight:bold; 
                background:linear-gradient(90deg, #00f2fe 0%, #ff00ff 100%);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                margin:1.5rem 0 1rem 0; padding-left:1rem;
                border-left:4px solid #00f2fe;
                text-shadow: 0 0 20px rgba(0,242,254,0.4), 0 0 40px rgba(255,0,255,0.2);">
        {icon} {title}
    </div>
    """, unsafe_allow_html=True)


def render_divider():
    """渲染霓虹分隔线"""
    st.markdown(f"""
    <hr style="border:none; height:1px; 
               background:linear-gradient(90deg, transparent, #00f2fe88, #ff00ff88, transparent); 
               margin:2rem 0;
               box-shadow: 0 0 10px rgba(0,242,254,0.3);">
    """, unsafe_allow_html=True)


# ========== 音乐卡片组件 ==========

def render_song_card(song: Dict, show_play: bool = True,
                     on_play: Optional[Callable] = None,
                     key_prefix: str = "song"):
    """渲染霓虹歌曲卡片"""
    mood_colors = {
        "欢快": "#ff00ff", "悲伤": "#00f2fe", "愉悦": "#fee140",
        "激昂": "#ff6b6b", "平静": "#00f2fe", "温暖": "#ff00ff",
        "孤独": "#4facfe", "迷茫": "#ff00ff", "浪漫": "#ff00ff",
        "治愈": "#2ecc71", "坚定": "#00f2fe", "放松": "#4facfe"
    }

    primary_mood = song.get("mood", ["流行"])[0] if song.get("mood") else "流行"
    border_color = mood_colors.get(primary_mood, "#00f2fe")

    mood_tags = " ".join([
        f'<span style="background:{border_color}33; color:{border_color}; padding:0.15rem 0.5rem; border-radius:10px; font-size:0.75rem; margin-right:0.3rem; text-shadow: 0 0 5px {border_color}66;">#{m}</span>'
        for m in song.get("mood", [])
    ])

    scene_tags = " ".join([
        f'<span style="background:rgba(0,242,254,0.1); color:{Theme.TEXT_SECONDARY}; padding:0.15rem 0.5rem; border-radius:10px; font-size:0.75rem; margin-right:0.3rem;">🏷️ {s}</span>'
        for s in song.get("scene", [])
    ])

    energy = song.get("energy", 0.5)
    energy_color = "#ff00ff" if energy > 0.7 else "#fee140" if energy > 0.4 else "#00f2fe"

    st.markdown(f"""
    <div style="background:rgba(0,242,254,0.03); border:1px solid {border_color}44;
                border-left:4px solid {border_color}; border-radius:12px;
                padding:1rem; margin:0.5rem 0; 
                box-shadow: 0 0 15px {border_color}22, inset 0 0 20px rgba(0,0,0,0.2);
                transition:all 0.3s;">
        <div style="display:flex; align-items:center; gap:1rem;">
            <div style="font-size:2.5rem; min-width:3rem; text-align:center; text-shadow: 0 0 20px {border_color}66;">{song.get("cover", "🎵")}</div>
            <div style="flex:1;">
                <div style="font-size:1.1rem; font-weight:bold; background:linear-gradient(90deg, #e0e0e0, #fff); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">{song["title"]}</div>
                <div style="color:{Theme.TEXT_SECONDARY}; font-size:0.9rem;">{song["artist"]} · {song.get("album", "")} · {song.get("year", "")}</div>
                <div style="margin:0.4rem 0;">{mood_tags}</div>
                <div style="margin:0.3rem 0;">{scene_tags}</div>
                <div style="display:flex; align-items:center; gap:0.5rem; margin-top:0.5rem;">
                    <span style="color:{Theme.TEXT_SECONDARY}; font-size:0.8rem;">⚡ 能量</span>
                    <div style="flex:1; background:rgba(255,255,255,0.05); height:4px; border-radius:2px;">
                        <div style="background:linear-gradient(90deg, #00f2fe, #ff00ff); width:{energy*100}%; height:100%; border-radius:2px; box-shadow: 0 0 8px {energy_color}88;"></div>
                    </div>
                    <span style="color:{Theme.TEXT_SECONDARY}; font-size:0.75rem;">{song.get("tempo", 120)} BPM</span>
                    <span style="color:{Theme.TEXT_SECONDARY}; font-size:0.75rem;">⏱️ {song.get("duration_str", "3:00")}</span>
                </div>
                <div style="color:{Theme.TEXT_SECONDARY}; font-size:0.8rem; margin-top:0.3rem; line-height:1.4;">
                    {song.get("description", "")}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if show_play and on_play:
        if st.button("▶️ 立即播放", key=f"{key_prefix}_{song['id']}", use_container_width=True):
            on_play(song)


def render_compact_card(song: Dict, on_play: Optional[Callable] = None, key_prefix: str = "compact"):
    """渲染紧凑型霓虹歌曲卡片（用于网格）"""
    mood_color = "#00f2fe"

    st.markdown(f"""
    <div style="background:rgba(0,242,254,0.03); border:1px solid rgba(0,242,254,0.15);
                border-radius:12px; padding:1rem; text-align:center; margin:0.3rem 0;
                box-shadow: 0 0 15px rgba(0,242,254,0.1);">
        <div style="font-size:2.5rem; margin-bottom:0.5rem; text-shadow: 0 0 15px rgba(0,242,254,0.4);">{song.get("cover", "🎵")}</div>
        <div style="font-weight:bold; font-size:0.95rem; background:linear-gradient(90deg, #e0e0e0, #fff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
            {song["title"]}
        </div>
        <div style="color:{Theme.TEXT_SECONDARY}; font-size:0.8rem; margin:0.3rem 0;">
            {song["artist"]}
        </div>
        <div style="margin:0.3rem 0;">
            <span style="background:rgba(0,242,254,0.2); padding:0.2rem 0.5rem; border-radius:8px; font-size:0.7rem; color:#00f2fe; text-shadow: 0 0 5px rgba(0,242,254,0.5);">
                {song.get("mood", ["流行"])[0] if song.get("mood") else "流行"}
            </span>
        </div>
        <div style="color:{Theme.TEXT_SECONDARY}; font-size:0.75rem;">{song.get("duration_str", "3:00")}</div>
    </div>
    """, unsafe_allow_html=True)

    if on_play:
        if st.button("▶️", key=f"{key_prefix}_{song['id']}", use_container_width=True):
            on_play(song)


def render_song_grid(songs: List[Dict], cols: int = 3,
                     on_play: Optional[Callable] = None):
    """渲染歌曲网格布局"""
    for i in range(0, len(songs), cols):
        row_songs = songs[i:i+cols]
        columns = st.columns(cols)

        for idx, (col, song) in enumerate(zip(columns, row_songs)):
            with col:
                render_compact_card(song, on_play=on_play, key_prefix=f"grid_{i}_{idx}")


# ========== 播放器组件 ==========

def render_player(song: Dict, is_playing: bool = False,
                  on_play_pause: Optional[Callable] = None,
                  on_next: Optional[Callable] = None,
                  on_prev: Optional[Callable] = None,
                  on_random: Optional[Callable] = None,
                  progress: float = 0.35):
    """渲染霓虹播放器控制栏"""
    if not song:
        st.info("🎵 暂无播放中的歌曲")
        return

    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.4); border:1px solid rgba(0,242,254,0.3);
                border-radius:16px; padding:1.5rem; margin:1rem 0;
                box-shadow: 0 0 30px rgba(0,242,254,0.15), inset 0 0 30px rgba(0,0,0,0.3);">
        <div style="display:flex; align-items:center; gap:1.5rem;">
            <div style="font-size:3.5rem; min-width:4rem; text-align:center; text-shadow: 0 0 25px rgba(0,242,254,0.5);">
                {song.get("cover", "🎵")}
            </div>
            <div style="flex:1;">
                <div style="font-size:1.4rem; font-weight:bold; background:linear-gradient(90deg, #e0e0e0, #fff); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">{song["title"]}</div>
                <div style="color:{Theme.TEXT_SECONDARY}; margin:0.3rem 0;">{song["artist"]} · {song.get("album", "")} · {song.get("year", "")}</div>
                <div style="display:flex; gap:0.5rem; margin:0.5rem 0;">
                    {''.join([f'<span style="background:rgba(0,242,254,0.2); padding:0.2rem 0.6rem; border-radius:10px; font-size:0.8rem; color:#00f2fe; text-shadow: 0 0 5px rgba(0,242,254,0.5);">{m}</span>' for m in song.get("mood", [])])}
                    {''.join([f'<span style="background:rgba(255,255,255,0.05); padding:0.2rem 0.6rem; border-radius:10px; font-size:0.8rem; color:{Theme.TEXT_SECONDARY};">{g}</span>' for g in song.get("genre", [])])}
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:2rem; color:#00f2fe; text-shadow: 0 0 15px rgba(0,242,254,0.6);">{"⏸️" if is_playing else "▶️"}</div>
                <div style="color:{Theme.TEXT_SECONDARY}; font-size:0.85rem; margin-top:0.3rem;">{song.get("duration_str", "3:00")}</div>
            </div>
        </div>
        <div style="margin-top:1.2rem;">
            <div style="background:rgba(255,255,255,0.05); height:5px; border-radius:3px; overflow:hidden;">
                <div style="background:linear-gradient(90deg, #00f2fe, #ff00ff); width:{progress*100}%; height:100%; border-radius:3px; box-shadow: 0 0 10px rgba(0,242,254,0.5);"></div>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:0.4rem; font-size:0.75rem; color:{Theme.TEXT_SECONDARY};">
                <span>{int(progress * 180 // 60)}:{int(progress * 180 % 60):02d}</span>
                <span>{song.get("duration_str", "3:00")}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    ctrl_cols = st.columns([1, 1, 1, 1, 1, 2])
    with ctrl_cols[0]:
        if st.button("⏮️", key="player_prev") and on_prev:
            on_prev()
    with ctrl_cols[1]:
        if st.button("⏪", key="player_rewind"):
            pass
    with ctrl_cols[2]:
        btn_text = "⏸️" if is_playing else "▶️"
        if st.button(btn_text, key="player_toggle") and on_play_pause:
            on_play_pause()
    with ctrl_cols[3]:
        if st.button("⏩", key="player_forward"):
            pass
    with ctrl_cols[4]:
        if st.button("⏭️", key="player_next") and on_next:
            on_next()
    with ctrl_cols[5]:
        if st.button("🔀 随机播放", key="player_random") and on_random:
            on_random()


def render_mini_player(song: Dict, is_playing: bool = False):
    """渲染霓虹迷你播放器（用于页面底部固定栏）"""
    st.markdown(f"""
    <div style="position:fixed; bottom:0; left:0; right:0; background:rgba(10,10,10,0.95);
                border-top:1px solid rgba(0,242,254,0.3); padding:0.8rem 2rem;
                display:flex; align-items:center; gap:1rem; z-index:1000;
                box-shadow: 0 -5px 30px rgba(0,242,254,0.2);">
        <div style="font-size:1.5rem; text-shadow: 0 0 10px rgba(0,242,254,0.5);">{song.get("cover", "🎵") if song else "🎵"}</div>
        <div style="flex:1;">
            <div style="font-weight:bold; background:linear-gradient(90deg, #e0e0e0, #fff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:0.9rem;">{song["title"] if song else "未播放"}</div>
            <div style="color:{Theme.TEXT_SECONDARY}; font-size:0.75rem;">{song["artist"] if song else "-"}</div>
        </div>
        <div style="font-size:1.2rem; color:#00f2fe; text-shadow: 0 0 10px rgba(0,242,254,0.6);">{"⏸️" if is_playing else "▶️"}</div>
    </div>
    <div style="height:60px;"></div>
    """, unsafe_allow_html=True)


# ========== LLM 交互组件 ==========

def render_llm_thinking(content: str, confidence: float = 0.9, expanded: bool = True):
    """渲染霓虹 LLM 思考过程展示框"""
    with st.expander("🔍 查看 AI 推理过程", expanded=expanded):
        st.markdown(f"""
        <div style="background:rgba(0,242,254,0.04); border-left:3px solid #00f2fe;
                    padding:1rem; border-radius:0 8px 8px 0; font-size:0.9rem; color:{Theme.TEXT_PRIMARY};
                    box-shadow: 0 0 15px rgba(0,242,254,0.1), inset 0 0 20px rgba(0,0,0,0.2);">
            <div style="font-weight:bold; margin-bottom:0.5rem; background:linear-gradient(90deg, #00f2fe, #ff00ff); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">🤖 AI 思考中...</div>
            <div style="line-height:1.6;">{content.replace(chr(10), "<br>")}</div>
            <div style="margin-top:0.8rem; padding-top:0.5rem; border-top:1px solid rgba(0,242,254,0.2);">
                <span style="font-size:0.8rem; color:{Theme.TEXT_SECONDARY};">置信度：{confidence*100:.0f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_llm_response(content: str, title: str = "🤖 AI 回复"):
    """渲染霓虹 LLM 生成的内容"""
    st.markdown(f"""
    <div style="background:rgba(0,242,254,0.05); border:1px solid rgba(0,242,254,0.2);
                border-radius:12px; padding:1.2rem; margin:1rem 0;
                box-shadow: 0 0 20px rgba(0,242,254,0.1), inset 0 0 20px rgba(0,0,0,0.2);">
        <div style="font-weight:bold; background:linear-gradient(90deg, #00f2fe, #ff00ff);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    margin-bottom:0.8rem; font-size:1.1rem;">
            {title}
        </div>
        <div style="color:{Theme.TEXT_PRIMARY}; line-height:1.7; font-size:0.95rem;">
            {content.replace(chr(10), "<br>")}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_streaming_text(text: str, container, speed: float = 0.02):
    """模拟流式输出效果（打字机效果）"""
    displayed = ""
    for char in text:
        displayed += char
        container.markdown(f"""
        <div style="background:rgba(0,242,254,0.04); border-radius:8px; padding:1rem; color:{Theme.TEXT_PRIMARY}; border:1px solid rgba(0,242,254,0.2); box-shadow: 0 0 10px rgba(0,242,254,0.1);">
            {displayed}▌
        </div>
        """, unsafe_allow_html=True)
        time.sleep(speed)


# ========== 情绪/场景选择组件 ==========

def render_mood_selector(moods: List[tuple], on_select: Optional[Callable] = None) -> Optional[str]:
    """渲染霓虹情绪选择器"""
    st.markdown("<div style='font-size:1.2rem; font-weight:bold; background:linear-gradient(90deg, #00f2fe, #ff00ff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:1rem;'>选择您当前的情绪状态</div>", unsafe_allow_html=True)

    mood_cols = st.columns(len(moods))
    selected = None

    for col, (mood, css_class, emoji) in zip(mood_cols, moods):
        with col:
            gradient_map = {
                "mood-happy": "linear-gradient(135deg, #ff00ff 0%, #f5576c 100%)",
                "mood-sad": "linear-gradient(135deg, #00f2fe 0%, #4facfe 100%)",
                "mood-joy": "linear-gradient(135deg, #fee140 0%, #fa709a 100%)",
                "mood-excited": "linear-gradient(135deg, #ff6b6b 0%, #fee140 100%)",
                "mood-calm": "linear-gradient(135deg, #00f2fe 0%, #4facfe 100%)"
            }
            bg = gradient_map.get(css_class, Theme.GRADIENT_PRIMARY)
            text_color = "#000" if css_class == "mood-joy" else "#fff"

            st.markdown(f"""
            <div style="background:{bg}; border-radius:16px; padding:1.2rem; text-align:center; margin:0.3rem 0; box-shadow: 0 0 20px rgba(0,242,254,0.2);">
                <div style="font-size:2.5rem; text-shadow: 0 0 15px rgba(255,255,255,0.5);">{emoji}</div>
                <div style="font-weight:bold; color:{text_color}; margin-top:0.5rem; font-size:1.1rem; text-shadow: 0 0 10px rgba(0,0,0,0.3);">{mood}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("选择", key=f"mood_select_{mood}", use_container_width=True):
                selected = mood
                if on_select:
                    on_select(mood)

    return selected


def render_scene_selector(scenes: List[tuple], on_select: Optional[Callable] = None) -> Optional[str]:
    """渲染霓虹场景选择器"""
    st.markdown("<div style='font-size:1.2rem; font-weight:bold; background:linear-gradient(90deg, #00f2fe, #ff00ff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:1rem;'>选择您当前的场景</div>", unsafe_allow_html=True)

    scene_cols = st.columns(len(scenes))
    selected = None

    for col, (scene, emoji, desc) in zip(scene_cols, scenes):
        with col:
            st.markdown(f"""
            <div style="background:rgba(0,242,254,0.05); border:1px solid rgba(0,242,254,0.2);
                        border-radius:16px; padding:1.5rem 1rem; text-align:center; margin:0.3rem 0;
                        box-shadow: 0 0 20px rgba(0,242,254,0.1);">
                <div style="font-size:2.5rem; margin-bottom:0.5rem; text-shadow: 0 0 15px rgba(0,242,254,0.4);">{emoji}</div>
                <div style="font-weight:bold; background:linear-gradient(90deg, #e0e0e0, #fff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:1.2rem; margin:0.5rem 0;">{scene}</div>
                <div style="color:{Theme.TEXT_SECONDARY}; font-size:0.85rem; line-height:1.4;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("进入场景", key=f"scene_select_{scene}", use_container_width=True):
                selected = scene
                if on_select:
                    on_select(scene)

    return selected


# ========== 聊天/问答组件 ==========

def render_chat_message(role: str, content: str, reasoning: str = "", confidence: float = 0.9):
    """渲染霓虹聊天消息"""
    if role == "user":
        st.markdown(f"""
        <div style="background:rgba(0,242,254,0.08); border:1px solid rgba(0,242,254,0.2); border-radius:12px 12px 0 12px;
                    padding:1rem; margin:0.5rem 0 0.5rem 15%; color:{Theme.TEXT_PRIMARY};
                    box-shadow: 0 0 15px rgba(0,242,254,0.1);">
            <div style="font-weight:bold; margin-bottom:0.3rem; background:linear-gradient(90deg, #00f2fe, #4facfe); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">👤 您</div>
            <div style="line-height:1.5;">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        reasoning_html = f"""
        <div style="margin-top:0.8rem; padding-top:0.5rem; border-top:1px solid rgba(255,0,255,0.2);">
            <small style="color:{Theme.TEXT_SECONDARY};">
                💭 推理：{reasoning[:80]}{"..." if len(reasoning) > 80 else ""} | 
                置信度：{confidence*100:.0f}%
            </small>
        </div>
        """ if reasoning else ""

        st.markdown(f"""
        <div style="background:rgba(255,0,255,0.06); border:1px solid rgba(255,0,255,0.2);
                    border-radius:12px 12px 12px 0; padding:1rem; 
                    margin:0.5rem 15% 0.5rem 0; color:{Theme.TEXT_PRIMARY};
                    box-shadow: 0 0 15px rgba(255,0,255,0.1);">
            <div style="font-weight:bold; margin-bottom:0.3rem; background:linear-gradient(90deg, #ff00ff, #fee140); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">🤖 AI 音乐导师</div>
            <div style="line-height:1.6;">{content.replace(chr(10), "<br>")}</div>
            {reasoning_html}
        </div>
        """, unsafe_allow_html=True)


def render_chat_history(history: List[Dict]):
    """渲染完整聊天历史"""
    for msg in history:
        render_chat_message(
            role=msg.get("role", "user"),
            content=msg.get("content", ""),
            reasoning=msg.get("reasoning", ""),
            confidence=msg.get("confidence", 0.9)
        )


def render_quick_questions(questions: List[str], on_select: Optional[Callable] = None):
    """渲染霓虹快捷问题按钮"""
    st.markdown("<div style='font-size:1.2rem; font-weight:bold; background:linear-gradient(90deg, #00f2fe, #ff00ff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:1rem;'>🔥 热门问题</div>", unsafe_allow_html=True)
    cols = st.columns(3)

    for i, (col, q) in enumerate(zip(cols * ((len(questions) + 2) // 3), questions)):
        with col:
            if st.button(f"💬 {q}", key=f"quick_q_{i}", use_container_width=True):
                if on_select:
                    on_select(q)


# ========== 统计/数据展示组件 ==========

def render_stat_card(label: str, value: str, icon: str = "📊", color: str = None):
    """渲染霓虹统计卡片"""
    color = color or Theme.TEXT_ACCENT
    st.markdown(f"""
    <div style="background:rgba(0,242,254,0.05); 
                border:1px solid {color}44; border-radius:12px;
                padding:1.2rem; text-align:center;
                box-shadow: 0 0 20px {color}22;">
        <div style="font-size:1.5rem; margin-bottom:0.3rem; text-shadow: 0 0 10px {color}66;">{icon}</div>
        <div style="font-size:1.8rem; font-weight:bold; background:linear-gradient(90deg, #e0e0e0, #fff); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">{value}</div>
        <div style="color:{Theme.TEXT_SECONDARY}; font-size:0.85rem; margin-top:0.3rem;">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_song_list_table(songs: List[Dict], show_actions: bool = True):
    """渲染歌曲列表表格"""
    df_data = []
    for s in songs:
        df_data.append({
            "歌曲": f"{s.get('cover', '🎵')} {s['title']}",
            "艺人": s["artist"],
            "情绪": ", ".join(s.get("mood", [])),
            "场景": ", ".join(s.get("scene", [])),
            "时长": s.get("duration_str", "3:00"),
            "BPM": s.get("tempo", 120),
            "能量": f"{s.get('energy', 0.5):.0%}"
        })

    st.dataframe(
        df_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "歌曲": st.column_config.TextColumn("歌曲", width="large"),
            "能量": st.column_config.ProgressColumn("能量", min_value=0, max_value=1, format="%.0f%%")
        }
    )


# ========== 加载/状态组件 ==========

def render_loading_spinner(text: str = "AI 思考中..."):
    """渲染霓虹加载动画"""
    return st.spinner(f"🧠 {text}")


def render_empty_state(icon: str, title: str, description: str):
    """渲染霓虹空状态提示"""
    st.markdown(f"""
    <div style="text-align:center; padding:3rem 1rem; color:{Theme.TEXT_SECONDARY};">
        <div style="font-size:3rem; margin-bottom:1rem; text-shadow: 0 0 20px rgba(0,242,254,0.4);">{icon}</div>
        <div style="font-size:1.2rem; font-weight:bold; background:linear-gradient(90deg, #e0e0e0, #fff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:0.5rem;">{title}</div>
        <div style="font-size:0.9rem;">{description}</div>
    </div>
    """, unsafe_allow_html=True)


def render_notification(message: str, type_: str = "info"):
    """渲染霓虹通知消息"""
    colors = {
        "info": ("#00f2fe", "ℹ️"),
        "success": ("#2ecc71", "✅"),
        "warning": ("#fee140", "⚠️"),
        "error": ("#ff00ff", "❌")
    }
    color, icon = colors.get(type_, colors["info"])

    st.markdown(f"""
    <div style="background:{color}15; border-left:3px solid {color};
                padding:0.8rem 1rem; border-radius:0 8px 8px 0;
                margin:0.5rem 0; color:{Theme.TEXT_PRIMARY};
                box-shadow: 0 0 15px {color}33;">
        <span style="color:{color}; font-weight:bold; text-shadow: 0 0 5px {color}66;">{icon}</span> {message}
    </div>
    """, unsafe_allow_html=True)


# ========== 标签/徽章组件 ==========

def render_tag(text: str, color: str = None, size: str = "normal"):
    """渲染霓虹标签徽章"""
    color = color or Theme.TEXT_ACCENT
    font_size = "0.85rem" if size == "normal" else "0.75rem"
    padding = "0.3rem 0.8rem" if size == "normal" else "0.15rem 0.5rem"

    return f"""
    <span style="background:{color}22; color:{color}; 
                padding:{padding}; border-radius:20px; 
                font-size:{font_size}; margin:0.2rem; display:inline-block;
                text-shadow: 0 0 5px {color}66;
                box-shadow: 0 0 10px {color}22;">
        {text}
    </span>
    """


def render_mood_badge(mood: str) -> str:
    """渲染霓虹情绪徽章"""
    mood_color_map = {
        "欢快": "#ff00ff", "悲伤": "#00f2fe", "愉悦": "#fee140",
        "激昂": "#ff6b6b", "平静": "#00f2fe", "温暖": "#ff00ff",
        "孤独": "#4facfe", "迷茫": "#ff00ff", "浪漫": "#ff00ff",
        "治愈": "#2ecc71", "坚定": "#00f2fe", "放松": "#4facfe"
    }
    color = mood_color_map.get(mood, Theme.TEXT_ACCENT)
    return render_tag(f"#{mood}", color)


def render_scene_badge(scene: str) -> str:
    """渲染霓虹场景徽章"""
    return render_tag(f"🏷️ {scene}", Theme.TEXT_SECONDARY)


# ========== 分页/导航组件 ==========

def render_pagination(current_page: int, total_pages: int, on_change: Optional[Callable] = None):
    """渲染霓虹分页器"""
    cols = st.columns(min(total_pages, 7))
    for i, col in enumerate(cols):
        page_num = i + 1
        if page_num > total_pages:
            break
        with col:
            btn_type = "primary" if page_num == current_page else "secondary"
            if st.button(str(page_num), key=f"page_{page_num}", type=btn_type, use_container_width=True):
                if on_change:
                    on_change(page_num)


def render_tab_nav(tabs: List[str], active_tab: str, on_change: Optional[Callable] = None) -> str:
    """渲染霓虹自定义标签导航"""
    cols = st.columns(len(tabs))
    selected = active_tab

    for col, tab_name in zip(cols, tabs):
        with col:
            is_active = tab_name == active_tab
            bg_color = "rgba(0,242,254,0.2)" if is_active else "rgba(0,242,254,0.05)"
            border_color = "#00f2fe" if is_active else "rgba(0,242,254,0.2)"
            text_color = "#00f2fe" if is_active else Theme.TEXT_SECONDARY

            st.markdown(f"""
            <div style="background:{bg_color}; border:1px solid {border_color};
                        border-radius:8px; padding:0.6rem; text-align:center;
                        box-shadow: 0 0 10px {border_color}33;">
                <span style="color:{text_color}; font-weight:{'bold' if is_active else 'normal'}; text-shadow: 0 0 5px {text_color}66;">{tab_name}</span>
            </div>
            """, unsafe_allow_html=True)

            if st.button("选择", key=f"tab_{tab_name}", label_visibility="collapsed"):
                selected = tab_name
                if on_change:
                    on_change(tab_name)

    return selected


# ========== 特殊效果组件 ==========

def render_equalizer_animation():
    """渲染霓虹音频均衡器动画"""
    st.markdown(f"""
    <div style="display:flex; align-items:flex-end; justify-content:center; gap:3px; height:30px;">
        <div style="width:4px; background:linear-gradient(180deg, #00f2fe, #ff00ff); height:15px; border-radius:2px; animation:eq1 0.5s ease-in-out infinite alternate; box-shadow: 0 0 5px rgba(0,242,254,0.5);"></div>
        <div style="width:4px; background:linear-gradient(180deg, #00f2fe, #ff00ff); height:25px; border-radius:2px; animation:eq2 0.7s ease-in-out infinite alternate; box-shadow: 0 0 5px rgba(0,242,254,0.5);"></div>
        <div style="width:4px; background:linear-gradient(180deg, #00f2fe, #ff00ff); height:20px; border-radius:2px; animation:eq3 0.4s ease-in-out infinite alternate; box-shadow: 0 0 5px rgba(0,242,254,0.5);"></div>
        <div style="width:4px; background:linear-gradient(180deg, #00f2fe, #ff00ff); height:30px; border-radius:2px; animation:eq1 0.6s ease-in-out infinite alternate; box-shadow: 0 0 5px rgba(0,242,254,0.5);"></div>
        <div style="width:4px; background:linear-gradient(180deg, #00f2fe, #ff00ff); height:18px; border-radius:2px; animation:eq2 0.5s ease-in-out infinite alternate; box-shadow: 0 0 5px rgba(0,242,254,0.5);"></div>
    </div>
    <style>
        @keyframes eq1 {{ from {{ height: 10px; }} to {{ height: 30px; }} }}
        @keyframes eq2 {{ from {{ height: 15px; }} to {{ height: 25px; }} }}
        @keyframes eq3 {{ from {{ height: 5px; }} to {{ height: 20px; }} }}
    </style>
    """, unsafe_allow_html=True)


def render_hero_section(title: str, subtitle: str, cta_text: str = "开始探索"):
    """渲染霓虹首页 Hero 区域"""
    st.markdown(f"""
    <div style="text-align:center; padding:3rem 1rem; margin:1rem 0;">
        <div style="font-size:3.5rem; margin-bottom:1rem; text-shadow: 0 0 30px rgba(0,242,254,0.5);">🎵</div>
        <div style="font-size:2.5rem; font-weight:bold;
                    background:linear-gradient(90deg, #00f2fe 0%, #4facfe 30%, #ff00ff 70%, #fee140 100%);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    margin-bottom:1rem;
                    text-shadow: 0 0 40px rgba(0,242,254,0.3);">
            {title}
        </div>
        <div style="color:{Theme.TEXT_SECONDARY}; font-size:1.1rem; max-width:600px; margin:0 auto 2rem auto;">
            {subtitle}
        </div>
        <div style="display:inline-block; background:linear-gradient(135deg, #00f2fe, #ff00ff);
                    padding:0.8rem 2rem; border-radius:30px; color:#000; font-weight:bold;
                    box-shadow: 0 0 30px rgba(0,242,254,0.4), 0 0 60px rgba(255,0,255,0.2);">
            {cta_text} →
        </div>
    </div>
    """, unsafe_allow_html=True)


# ========== 导出说明 ==========
"""
使用方式：
from components import Theme, render_header, render_song_card, render_player

# 如需修改主题，直接改 Theme 类：
Theme.TEXT_ACCENT = "#ff0000"  # 改为红色强调色

# 或创建新主题：
class DarkTheme:
    TEXT_ACCENT = "#64ffda"
    ...
"""
