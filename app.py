"""
AI 智能音乐平台 - Spotify 嵌入版
"""
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from components import *
from llm_engine import LLMEngineFactory
from music_logic import MusicRecommender, MusicKnowledgeService
from spotify_service import SpotifyService

st.set_page_config(page_title="🎵 AI 智能音乐平台", page_icon="🎵", layout="wide", initial_sidebar_state="collapsed")

# 全局 CSS
st.markdown("""
<style>
    .stApp{background:linear-gradient(135deg,#0a0a0a 0%,#1a0a2e 50%,#0a0a0a 100%)!important}
    h1,h2,h3,h4,h5,h6{background:linear-gradient(90deg,#00f2fe,#ff00ff)!important;-webkit-background-clip:text!important;-webkit-text-fill-color:transparent!important}
    .stButton>button{background:linear-gradient(135deg,#00f2fe,#ff00ff)!important;color:#000!important}
    ::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#00f2fe,#ff00ff)}
</style>
""", unsafe_allow_html=True)

# ========== 辅助函数 ==========
def _ensure_queue():
    """确保播放列表存在"""
    if "playlist_queue" not in st.session_state:
        st.session_state.playlist_queue = []
    return st.session_state.playlist_queue

def _add_to_queue(s):
    """添加歌曲到播放列表"""
    queue = _ensure_queue()
    # 检查是否已存在
    if not any(q["id"] == s["id"] for q in queue):
        queue.append(s)
        st.session_state.playlist_queue = queue  # 显式赋值确保持久化
        render_notification(f"✅ 已添加 《{s['title']}》 到播放列表", "success")
    else:
        render_notification(f"⚠️ 《{s['title']}》 已在列表中", "warning")
    st.rerun()

def _remove_from_queue(index):
    """从播放列表移除"""
    queue = _ensure_queue()
    if 0 <= index < len(queue):
        queue.pop(index)
        st.session_state.playlist_queue = queue
        st.rerun()

def _play_spotify(song):
    """播放 Spotify 歌曲"""
    st.session_state.current_song = song
    st.session_state.is_playing = True
    # 添加到历史
    if "play_history" not in st.session_state:
        st.session_state.play_history = []
    st.session_state.play_history.append(song)
    st.rerun()

def _toggle_play():
    st.session_state.is_playing = not st.session_state.is_playing
    st.rerun()

def _play_next(rec, spotify):
    queue = _ensure_queue()
    current = st.session_state.current_song
    if queue and current:
        # 找到当前歌曲在队列中的位置，播放下一首
        for i, q in enumerate(queue):
            if q["id"] == current["id"] and i + 1 < len(queue):
                _play_spotify(queue[i + 1])
                return
    # 队列没有下一首，随机播放
    next_song = rec.library.get_random(1)[0].to_dict()
    next_song["spotify_id"] = spotify.search_track(next_song["title"], next_song["artist"])
    _play_spotify(next_song)

def _play_prev():
    h = st.session_state.get("play_history", [])
    if len(h) > 1:
        # 找到上一首不同的歌曲
        current_id = st.session_state.current_song["id"] if st.session_state.current_song else None
        for prev in reversed(h[:-1]):
            if prev["id"] != current_id:
                st.session_state.current_song = prev
                st.session_state.is_playing = True
                st.rerun()
                return

def _play_random(rec, spotify):
    s = rec.library.get_random(1)[0].to_dict()
    s["spotify_id"] = spotify.search_track(s["title"], s["artist"])
    _play_spotify(s)


# ========== Session State 初始化 ==========
if "recommender" not in st.session_state:
    llm = LLMEngineFactory.create()
    st.session_state.update({
        "recommender": MusicRecommender(llm),
        "knowledge_service": MusicKnowledgeService(llm),
        "spotify": SpotifyService(),
        "current_song": None,
        "is_playing": False,
        "play_history": [],
        "chat_history": [],
        "playlist_queue": []  # 显式初始化
    })

rec = st.session_state.recommender
ks = st.session_state.knowledge_service
spotify = st.session_state.spotify

render_header("🎵 AI 智能音乐平台", "基于大语言模型的个性化音乐推荐与 Spotify 在线播放")

# 在 render_header 之后添加
with st.sidebar:
    st.markdown("### 🔧 调试信息")
    queue = st.session_state.get("playlist_queue", [])
    st.write(f"播放列表: {len(queue)} 首")
    for i, q in enumerate(queue):
        st.write(f"{i+1}. {q['title']}")
tabs = st.tabs(["🎭 应景音乐", "▶️ 在线播放 (Spotify)", "💡 音乐知识问答"])

# ========== 板块一：应景音乐 ==========
with tabs[0]:
    render_section_title("🎭", "应景音乐推荐")
    sub_tabs = st.tabs(["🎨 按情绪推荐", "🏃 按场景推荐"])

    with sub_tabs[0]:
        mood = render_mood_selector([
            ("欢快", "mood-happy", "😊"), ("悲伤", "mood-sad", "😢"),
            ("愉悦", "mood-joy", "😄"), ("激昂", "mood-excited", "🔥"),
            ("平静", "mood-calm", "🌊")
        ])
        if mood:
            with render_loading_spinner(f"AI 分析「{mood}」..."):
                result = rec.get_mood_recommendations(mood)
                render_llm_thinking(result["llm_analysis"].reasoning, result["llm_analysis"].confidence)
                render_llm_response(result["llm_analysis"].content, "📝 AI 推荐语")
                st.markdown("#### 🎵 推荐歌单")
                for s in result["songs"]:
                    s["spotify_id"] = spotify.search_track(s["title"], s["artist"])
                    render_song_card_spotify(s, 
                        on_add=lambda x=s: _add_to_queue(x),
                        on_play=lambda x=s: _play_spotify(x)
                    )

    with sub_tabs[1]:
        scene = render_scene_selector([
            ("跑步", "🏃", "动感节奏"), ("睡眠", "🌙", "助眠音乐"),
            ("放松", "🧘", "疗愈轻音乐")
        ])
        if scene:
            with render_loading_spinner(f"AI 匹配「{scene}」..."):
                result = rec.get_scene_recommendations(scene)
                render_llm_thinking(result["llm_analysis"].reasoning, result["llm_analysis"].confidence)
                render_llm_response(result["llm_analysis"].content, "📝 AI 场景推荐")
                st.markdown("#### 🎵 场景歌单")
                for i, s in enumerate(result["songs"], 1):
                    s["spotify_id"] = spotify.search_track(s["title"], s["artist"])
                    c = st.columns([0.5, 3, 1.5, 1])
                    c[0].markdown(f"<div style='text-align:center'>#{i}</div>", unsafe_allow_html=True)
                    c[1].markdown(f"**{s['title']}** - {s['artist']}")
                    c[1].caption(s['description'][:50] + "...")
                    c[2].markdown(f"{'🏃' if scene=='跑步' else '🌙' if scene=='睡眠' else '🧘'} {'配速' if scene=='跑步' else '指数'}：{s['tempo']//2 if scene=='跑步' else 100-int(s['energy']*100)}{'步/分' if scene=='跑步' else '%'}")
                    if c[3].button("➕", key=f"sc_{s['id']}"):
                        _add_to_queue(s)

# ========== 板块二：在线播放 (Spotify) ==========
with tabs[1]:
    render_section_title("▶️", "在线音乐播放")
    
    cs = st.session_state.get("current_song")
    queue = _ensure_queue()  # 确保获取最新队列

    # ===== 播放器区域 =====
    if cs and cs.get("spotify_id"):
        render_spotify_player(cs["spotify_id"], cs.get("title", "未知歌曲"))
        
        ctrl = st.columns([1,1,1,1,1,2])
        if ctrl[0].button("⏮️", key="pp"): _play_prev()
        if ctrl[2].button("⏸️" if st.session_state.get("is_playing", False) else "▶️", key="pt"): _toggle_play()
        if ctrl[4].button("⏭️", key="pn"): _play_next(rec, spotify)
        if ctrl[5].button("🔀 随机播放", key="pr"): _play_random(rec, spotify)
        
        st.markdown(f"""
        <div style="text-align:center;margin:1rem 0">
            <div style="font-size:1.2rem;font-weight:bold;color:#fff">{cs['title']}</div>
            <div style="color:#888">{cs['artist']} · {cs.get('album','')} · {cs.get('year','')}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        render_empty_state("🎵", "暂无播放中的歌曲", "请从「应景音乐」添加歌曲到播放列表后点击播放")

    render_divider()

    # ===== 播放列表区域（关键修复）=====
    st.markdown("#### 📋 播放列表")
    
    if queue:
        st.success(f"当前列表共 {len(queue)} 首歌曲")
        
        for i, s in enumerate(queue):
            cols = st.columns([0.5, 3, 1.5, 1, 1])
            
            # 序号
            cols[0].markdown(f"**{i+1}.**")
            
            # 歌曲信息
            has_spotify = s.get("spotify_id") is not None
            badge = "🎵" if has_spotify else "❌"
            cols[1].markdown(f"{badge} **{s['title']}** - {s['artist']}")
            cols[1].caption(f"{s.get('duration_str','3:00')} · {s.get('tempo',120)} BPM")
            
            # 播放按钮
            if has_spotify:
                if cols[2].button("▶️ 播放", key=f"queue_play_{s['id']}_{i}"):
                    _play_spotify(s)
            else:
                cols[2].caption("暂无音源")
            
            # 上移/下移
            if i > 0 and cols[3].button("⬆️", key=f"qu_{i}"):
                queue[i], queue[i-1] = queue[i-1], queue[i]
                st.session_state.playlist_queue = queue
                st.rerun()
            if i < len(queue) - 1 and cols[3].button("⬇️", key=f"qd_{i}"):
                queue[i], queue[i+1] = queue[i+1], queue[i]
                st.session_state.playlist_queue = queue
                st.rerun()
            
            # 删除
            if cols[4].button("❌", key=f"qr_{s['id']}_{i}"):
                _remove_from_queue(i)
        
        # 清空按钮
        if st.button("🗑️ 清空播放列表", use_container_width=True):
            st.session_state.playlist_queue = []
            st.session_state.current_song = None
            st.session_state.is_playing = False
            st.rerun()
    else:
        st.info("📭 播放列表为空，请从「应景音乐」板块添加歌曲")

    render_divider()

    # ===== 每日推荐 =====
    st.markdown("#### ✨ 每日智能推荐")
    if st.button("🔄 生成今日推荐", use_container_width=True):
        with render_loading_spinner("AI 分析口味..."):
            daily = rec.get_daily_recommendations(6)
            render_llm_response(daily["llm_insight"].content, "🤖 AI 洞察")
            for s in daily["songs"]:
                s["spotify_id"] = spotify.search_track(s["title"], s["artist"])
            render_song_grid_spotify(daily["songs"], cols=3, 
                on_add=lambda s: _add_to_queue(s),
                on_play=lambda s: _play_spotify(s))

    # ===== 播放历史 =====
    history = st.session_state.get("play_history", [])
    if history:
        with st.expander(f"📜 播放历史 ({len(history)}首)"):
            for s in history[-10:]:
                st.markdown(f"{s.get('cover','🎵')} **{s['title']}** - {s['artist']}")

# ========== 板块三：音乐知识问答 ==========
with tabs[2]:
    render_section_title("💡", "音乐知识你问我答")
    render_notification("🤖 AI 音乐导师已就位！可询问乐理、历史、乐器、流派、演奏技巧等问题。", "info")

    st.markdown("#### 💬 对话记录")
    render_chat_history(st.session_state.get("chat_history", []))

    render_divider()
    q = st.text_input("输入您的问题...", placeholder="例如：为什么小调听起来比较悲伤？", key="q_input")
    if st.button("🚀 提问", use_container_width=True) and q:
        with render_loading_spinner("AI 思考中..."):
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            st.session_state.chat_history.append({"role": "user", "content": q})
            r = ks.ask(q)
            st.session_state.chat_history.append({
                "role": "assistant", "content": r["answer"].content,
                "reasoning": r["answer"].reasoning, "confidence": r["answer"].confidence,
                "source": r["source"]
            })
            if r["matched_knowledge"]:
                render_notification(f"📚 来源：{r['matched_knowledge']['category']} | 难度：{r['matched_knowledge']['difficulty']}", "info")
            if r["related_questions"]:
                with st.expander("📎 相关问题"):
                    for x in r["related_questions"]: st.markdown(f"- {x}")
            st.rerun()

    if st.session_state.get("chat_history") and st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

render_divider()
st.markdown('<div style="text-align:center;color:#666;padding:1rem"><small>🎵 AI 智能音乐平台 | Powered by Streamlit + Spotify</small></div>', unsafe_allow_html=True)