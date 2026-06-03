"""
AI 智能音乐平台 - Spotify 嵌入版
修复：使用 on_click + kwargs 实现可靠的按钮回调
"""
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from components import *
from llm_engine import LLMEngineFactory
from music_logic import MusicRecommender, MusicKnowledgeService
from spotify_service import SpotifyService

# 本地定义 _gradient_text（避免导入问题）
def _gradient_text(text: str, size: str = "1rem", bold: bool = True) -> str:
    b = "bold" if bold else "normal"
    return '<span style="font-size:' + size + ';font-weight:' + b + ';background:linear-gradient(90deg,#00f2fe,#ff00ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent">' + text + '</span>'

st.set_page_config(page_title="🎵 AI 智能音乐平台", page_icon="🎵", layout="wide", initial_sidebar_state="collapsed")

# 全局 CSS
st.markdown("""
<style>
    .stApp{background:linear-gradient(135deg,#0a0a0a 0%,#1a0a2e 50%,#0a0a0a 100%)!important}
    h1,h2,h3,h4,h5,h6{background:linear-gradient(90deg,#00f2fe,#ff00ff)!important;-webkit-background-clip:text!important;-webkit-text-fill-color:transparent!important}
</style>
""", unsafe_allow_html=True)


# ========== Session State 初始化 ==========
def init_session():
    defaults = {
        "recommender": None,
        "knowledge_service": None,
        "spotify": None,
        "current_song": None,
        "is_playing": False,
        "play_history": [],
        "chat_history": [],
        "playlist_queue": [],
        "notification": None,
        "daily_recommendations": [],
        "selected_mood": None,
        "selected_scene": None,
        "mood_songs": [],
        "scene_songs": [],
        "mood_analysis": None,
        "scene_analysis": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

# 延迟初始化服务
if st.session_state.recommender is None:
    llm = LLMEngineFactory.create()
    st.session_state.recommender = MusicRecommender(llm)
    st.session_state.knowledge_service = MusicKnowledgeService(llm)
    st.session_state.spotify = SpotifyService()

rec = st.session_state.recommender
ks = st.session_state.knowledge_service
spotify = st.session_state.spotify


# ========== 回调函数（在页面顶部定义，使用 kwargs 接收参数）==========
def on_add_to_queue(song_id, song_title, song_artist, song_data):
    """添加到播放列表的回调"""
    queue = st.session_state.playlist_queue
    exists = any(q["id"] == song_id for q in queue)

    if not exists:
        queue.append(song_data)
        st.session_state.playlist_queue = queue
        st.session_state.notification = "✅ 已添加 《" + song_title + "》 到播放列表"
    else:
        st.session_state.notification = "⚠️ 《" + song_title + "》 已在列表中"


def on_play_song(song_data):
    """播放歌曲的回调"""
    st.session_state.current_song = song_data
    st.session_state.is_playing = True
    st.session_state.play_history.append(song_data)


def on_remove_from_queue(index):
    """从播放列表移除的回调"""
    queue = st.session_state.playlist_queue
    if 0 <= index < len(queue):
        removed = queue.pop(index)
        st.session_state.playlist_queue = queue
        st.session_state.notification = "🗑️ 已移除 《" + removed["title"] + "》"


def on_toggle_play():
    st.session_state.is_playing = not st.session_state.is_playing


def on_play_next():
    queue = st.session_state.playlist_queue
    current = st.session_state.current_song
    if queue and current:
        for i, q in enumerate(queue):
            if q["id"] == current["id"] and i + 1 < len(queue):
                st.session_state.current_song = queue[i + 1]
                st.session_state.is_playing = True
                st.session_state.play_history.append(queue[i + 1])
                return
    next_song = rec.library.get_random(1)[0].to_dict()
    next_song["spotify_id"] = spotify.search_track(next_song["title"], next_song["artist"])
    st.session_state.current_song = next_song
    st.session_state.is_playing = True
    st.session_state.play_history.append(next_song)


def on_play_prev():
    history = st.session_state.play_history
    if len(history) > 1:
        current_id = st.session_state.current_song["id"] if st.session_state.current_song else None
        for prev in reversed(history[:-1]):
            if prev["id"] != current_id:
                st.session_state.current_song = prev
                st.session_state.is_playing = True
                return


def on_play_random():
    s = rec.library.get_random(1)[0].to_dict()
    s["spotify_id"] = spotify.search_track(s["title"], s["artist"])
    st.session_state.current_song = s
    st.session_state.is_playing = True
    st.session_state.play_history.append(s)


def on_clear_queue():
    st.session_state.playlist_queue = []
    st.session_state.current_song = None
    st.session_state.is_playing = False
    st.session_state.notification = "🗑️ 播放列表已清空"


def on_select_mood(mood):
    """选择情绪的回调"""
    st.session_state.selected_mood = mood
    st.session_state.selected_scene = None  # 清除场景选择
    # 获取推荐
    result = rec.get_mood_recommendations(mood)
    for s in result["songs"]:
        s["spotify_id"] = spotify.search_track(s["title"], s["artist"])
    st.session_state.mood_songs = result["songs"]
    st.session_state.mood_analysis = result["llm_analysis"]
    st.session_state.scene_songs = []
    st.session_state.scene_analysis = None


def on_select_scene(scene):
    """选择场景的回调"""
    st.session_state.selected_scene = scene
    st.session_state.selected_mood = None  # 清除情绪选择
    result = rec.get_scene_recommendations(scene)
    for s in result["songs"]:
        s["spotify_id"] = spotify.search_track(s["title"], s["artist"])
    st.session_state.scene_songs = result["songs"]
    st.session_state.scene_analysis = result["llm_analysis"]
    st.session_state.mood_songs = []
    st.session_state.mood_analysis = None


def on_generate_daily():
    """生成每日推荐的回调"""
    daily = rec.get_daily_recommendations(6)
    for s in daily["songs"]:
        s["spotify_id"] = spotify.search_track(s["title"], s["artist"])
    st.session_state.daily_recommendations = daily["songs"]
    st.session_state.daily_insight = daily["llm_insight"]


def on_clear_chat():
    st.session_state.chat_history = []


# ========== 显示通知 ==========
if st.session_state.notification:
    notif_type = "success" if "✅" in st.session_state.notification else "info"
    render_notification(st.session_state.notification, notif_type)
    st.session_state.notification = None


# ========== 页面头部 ==========
render_header("🎵 AI 智能音乐平台", "基于大语言模型的个性化音乐推荐与 Spotify 在线播放")

# 调试面板
with st.sidebar:
    st.markdown("### 🔧 调试面板")
    st.write("**selected_mood:** " + str(st.session_state.selected_mood))
    st.write("**selected_scene:** " + str(st.session_state.selected_scene))
    queue = st.session_state.playlist_queue
    st.write("**播放列表:** " + str(len(queue)) + " 首")
    for i, q in enumerate(queue):
        st.write(str(i+1) + ". " + q["title"])
    st.divider()
    current = st.session_state.current_song
    st.write("**当前播放:** " + (current["title"] if current else "无"))


tabs = st.tabs(["🎭 应景音乐", "▶️ 在线播放 (Spotify)", "💡 音乐知识问答"])

# ========== 板块一：应景音乐 ==========
with tabs[0]:
    render_section_title("🎭", "应景音乐推荐")
    sub_tabs = st.tabs(["🎨 按情绪推荐", "🏃 按场景推荐"])

    # ===== 情绪推荐 =====
    with sub_tabs[0]:
        st.markdown(_gradient_text("选择您当前的情绪状态", "1.2rem"), unsafe_allow_html=True)

        # 情绪选择按钮 - 使用 on_click
        mood_cols = st.columns(5)
        moods = [
            ("欢快", "mood-happy", "😊"),
            ("悲伤", "mood-sad", "😢"),
            ("愉悦", "mood-joy", "😄"),
            ("激昂", "mood-excited", "🔥"),
            ("平静", "mood-calm", "🌊")
        ]
        gradients = {
            "mood-happy": "linear-gradient(135deg,#ff00ff,#f5576c)",
            "mood-sad": "linear-gradient(135deg,#00f2fe,#4facfe)",
            "mood-joy": "linear-gradient(135deg,#fee140,#fa709a)",
            "mood-excited": "linear-gradient(135deg,#ff6b6b,#fee140)",
            "mood-calm": "linear-gradient(135deg,#00f2fe,#4facfe)"
        }

        for col, (mood, cls, emoji) in zip(mood_cols, moods):
            with col:
                bg = gradients.get(cls, Theme.GRADIENT)
                tc = "#000" if cls == "mood-joy" else "#fff"
                st.markdown("""
                <div style="background:""" + bg + """;border-radius:16px;padding:1.2rem;text-align:center;margin:0.3rem 0;box-shadow:0 8px 32px rgba(0,0,0,0.3)">
                    <div style="font-size:2.5rem;text-shadow:0 0 20px rgba(255,255,255,0.5)">""" + emoji + """</div>
                    <div style="font-weight:bold;color:""" + tc + """;margin-top:0.5rem;font-size:1.1rem;text-shadow:0 2px 10px rgba(0,0,0,0.3)">""" + mood + """</div>
                </div>
                """, unsafe_allow_html=True)
                # 关键修复：使用 on_click + kwargs
                st.button("选择", key="ms_" + mood, use_container_width=True, 
                         on_click=on_select_mood, kwargs={"mood": mood})

        # 显示推荐结果
        if st.session_state.selected_mood and st.session_state.mood_songs:
            mood = st.session_state.selected_mood
            songs = st.session_state.mood_songs
            analysis = st.session_state.mood_analysis

            st.markdown("#### 🎵 「" + mood + "」推荐歌单")

            # 显示 LLM 分析
            if analysis:
                with st.expander("🔍 AI 推理过程"):
                    st.markdown("**置信度:** " + str(int(analysis.confidence * 100)) + "%")
                    st.markdown(analysis.reasoning)
                st.markdown("#### 📝 AI 推荐语")
                st.markdown(analysis.content)

            # 显示歌曲列表 - 关键修复：每首歌独立创建按钮，使用 on_click
            for idx, s in enumerate(songs):
                with st.container():
                    render_song_card_spotify(s, key_prefix="mood_" + mood + "_" + str(idx))

                    # 独立创建按钮 - 使用 on_click + kwargs
                    btn_cols = st.columns([1, 1])
                    has_spotify = s.get("spotify_id") is not None

                    # 播放按钮
                    if has_spotify:
                        btn_cols[0].button("▶️ 播放", key="mood_play_" + mood + "_" + str(idx) + "_" + s["id"],
                                          use_container_width=True,
                                          on_click=on_play_song, kwargs={"song_data": s})
                    else:
                        btn_cols[0].button("▶️ 暂无音源", key="mood_noplay_" + mood + "_" + str(idx),
                                          use_container_width=True, disabled=True)

                    # 关键修复：添加按钮 - 使用 on_click + kwargs 传递完整歌曲数据
                    btn_cols[1].button("➕ 加入列表", key="mood_add_" + mood + "_" + str(idx) + "_" + s["id"],
                                      use_container_width=True,
                                      on_click=on_add_to_queue, 
                                      kwargs={
                                          "song_id": s["id"],
                                          "song_title": s["title"],
                                          "song_artist": s["artist"],
                                          "song_data": s
                                      })

                    st.markdown("<hr style='border:none;height:1px;background:rgba(0,242,254,0.1);margin:0.5rem 0'>", unsafe_allow_html=True)

    # ===== 场景推荐 =====
    with sub_tabs[1]:
        st.markdown(_gradient_text("选择您当前的场景", "1.2rem"), unsafe_allow_html=True)

        scene_cols = st.columns(3)
        scenes = [
            ("跑步", "🏃", "动感节奏"),
            ("睡眠", "🌙", "助眠音乐"),
            ("放松", "🧘", "疗愈轻音乐")
        ]

        for col, (scene, emoji, desc) in zip(scene_cols, scenes):
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
                st.button("进入场景", key="ss_" + scene, use_container_width=True,
                         on_click=on_select_scene, kwargs={"scene": scene})

        # 显示场景推荐结果
        if st.session_state.selected_scene and st.session_state.scene_songs:
            scene = st.session_state.selected_scene
            songs = st.session_state.scene_songs
            analysis = st.session_state.scene_analysis

            st.markdown("#### 🎵 「" + scene + "」场景歌单")

            if analysis:
                with st.expander("🔍 AI 推理过程"):
                    st.markdown("**置信度:** " + str(int(analysis.confidence * 100)) + "%")
                    st.markdown(analysis.reasoning)
                st.markdown("#### 📝 AI 场景推荐")
                st.markdown(analysis.content)

            for i, s in enumerate(songs, 1):
                with st.container():
                    c = st.columns([0.5, 3, 1.5, 1])
                    c[0].markdown("<div style='text-align:center'>#" + str(i) + "</div>", unsafe_allow_html=True)
                    c[1].markdown("**" + s["title"] + "** - " + s["artist"])
                    c[1].caption(s["description"][:50] + "...")
                    c[2].markdown(("🏃 配速：" if scene == "跑步" else "🌙 指数：" if scene == "睡眠" else "🧘 指数：") + str(s["tempo"]//2 if scene == "跑步" else 100-int(s["energy"]*100)) + ("步/分" if scene == "跑步" else "%"))

                    # 场景添加按钮 - 使用 on_click
                    c[3].button("➕", key="scene_add_" + scene + "_" + str(i) + "_" + s["id"],
                               on_click=on_add_to_queue,
                               kwargs={
                                   "song_id": s["id"],
                                   "song_title": s["title"],
                                   "song_artist": s["artist"],
                                   "song_data": s
                               })

# ========== 板块二：在线播放 (Spotify) ==========
with tabs[1]:
    render_section_title("▶️", "在线音乐播放")

    cs = st.session_state.current_song
    queue = st.session_state.playlist_queue

    # ===== 播放器区域 =====
    if cs and cs.get("spotify_id"):
        render_spotify_player(cs["spotify_id"], cs.get("title", "未知歌曲"))

        ctrl = st.columns([1,1,1,1,1,2])
        ctrl[0].button("⏮️", key="pp", on_click=on_play_prev)
        ctrl[2].button("⏸️" if st.session_state.is_playing else "▶️", key="pt", on_click=on_toggle_play)
        ctrl[4].button("⏭️", key="pn", on_click=on_play_next)
        ctrl[5].button("🔀 随机播放", key="pr", on_click=on_play_random)

        st.markdown("""
        <div style="text-align:center;margin:1rem 0">
            <div style="font-size:1.2rem;font-weight:bold;color:#fff">""" + cs["title"] + """</div>
            <div style="color:#888">""" + cs["artist"] + " · " + cs.get("album", "") + " · " + str(cs.get("year", "")) + """</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        render_empty_state("🎵", "暂无播放中的歌曲", "请从「应景音乐」添加歌曲到播放列表后点击播放")

    render_divider()

    # ===== 播放列表区域 =====
    st.markdown("#### 📋 播放列表")

    if queue:
        st.success("当前列表共 " + str(len(queue)) + " 首歌曲")

        for i, s in enumerate(queue):
            cols = st.columns([0.5, 3, 1.5, 1, 1])

            cols[0].markdown("**" + str(i+1) + ".**")

            has_spotify = s.get("spotify_id") is not None
            badge = "🎵" if has_spotify else "❌"
            cols[1].markdown(badge + " **" + s["title"] + "** - " + s["artist"])
            cols[1].caption(s.get("duration_str", "3:00") + " · " + str(s.get("tempo", 120)) + " BPM")

            if has_spotify:
                cols[2].button("▶️ 播放", key="queue_play_" + s["id"] + "_" + str(i),
                              on_click=on_play_song, kwargs={"song_data": s})
            else:
                cols[2].caption("暂无音源")

            cols[4].button("❌", key="queue_remove_" + s["id"] + "_" + str(i),
                          on_click=on_remove_from_queue, kwargs={"index": i})

        st.button("🗑️ 清空播放列表", use_container_width=True, on_click=on_clear_queue)
    else:
        st.info("📭 播放列表为空，请从「应景音乐」板块添加歌曲")

    render_divider()

    # ===== 每日推荐 =====
    st.markdown("#### ✨ 每日智能推荐")
    st.button("🔄 生成今日推荐", use_container_width=True, on_click=on_generate_daily)

    if st.session_state.daily_recommendations:
        daily_songs = st.session_state.daily_recommendations
        if "daily_insight" in st.session_state and st.session_state.daily_insight:
            render_llm_response(st.session_state.daily_insight.content, "🤖 AI 洞察")

        for idx, s in enumerate(daily_songs):
            with st.container():
                render_compact_card_spotify(s, key_prefix="daily_" + str(idx))
                btn_cols = st.columns([1, 1])
                if s.get("spotify_id"):
                    btn_cols[0].button("▶️ 播放", key="daily_play_" + str(idx) + "_" + s["id"],
                                      use_container_width=True,
                                      on_click=on_play_song, kwargs={"song_data": s})
                btn_cols[1].button("➕ 加入列表", key="daily_add_" + str(idx) + "_" + s["id"],
                                  use_container_width=True,
                                  on_click=on_add_to_queue,
                                  kwargs={
                                      "song_id": s["id"],
                                      "song_title": s["title"],
                                      "song_artist": s["artist"],
                                      "song_data": s
                                  })

    # ===== 播放历史 =====
    history = st.session_state.play_history
    if history:
        with st.expander("📜 播放历史 (" + str(len(history)) + "首)"):
            for s in history[-10:]:
                st.markdown(s.get("cover", "🎵") + " **" + s["title"] + "** - " + s["artist"])

# ========== 板块三：音乐知识问答 ==========
with tabs[2]:
    render_section_title("💡", "音乐知识你问我答")
    render_notification("🤖 AI 音乐导师已就位！可询问乐理、历史、乐器、流派、演奏技巧等问题。", "info")

    st.markdown("#### 💬 对话记录")
    render_chat_history(st.session_state.chat_history)

    render_divider()
    q = st.text_input("输入您的问题...", placeholder="例如：为什么小调听起来比较悲伤？", key="q_input")

    # 提问按钮
    if st.button("🚀 提问", use_container_width=True) and q:
        with render_loading_spinner("AI 思考中..."):
            st.session_state.chat_history.append({"role": "user", "content": q})
            r = ks.ask(q)
            st.session_state.chat_history.append({
                "role": "assistant", "content": r["answer"].content,
                "reasoning": r["answer"].reasoning, "confidence": r["answer"].confidence,
                "source": r["source"]
            })
            if r["matched_knowledge"]:
                render_notification("📚 来源：" + r["matched_knowledge"]["category"] + " | 难度：" + r["matched_knowledge"]["difficulty"], "info")
            if r["related_questions"]:
                with st.expander("📎 相关问题"):
                    for x in r["related_questions"]: st.markdown("- " + x)
            st.rerun()

    if st.session_state.chat_history and st.button("🗑️ 清空对话", use_container_width=True, on_click=on_clear_chat):
        pass

render_divider()
st.markdown('<div style="text-align:center;color:#666;padding:1rem"><small>🎵 AI 智能音乐平台 | Powered by Streamlit + Spotify</small></div>', unsafe_allow_html=True)