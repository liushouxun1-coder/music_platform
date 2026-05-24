"""
AI 智能音乐平台 - 霓虹赛博朋克版
职责：全局 CSS + 业务逻辑 + 状态管理
所有 UI 渲染委托给 components.py
"""
import streamlit as st
from typing import Optional

# ========== 1. 加载 .env（必须在任何业务导入之前）==========
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ========== 2. 导入组件库（唯一 UI 渲染入口）==========
from components import (
    render_header, render_section_title, render_divider,
    render_song_card, render_compact_card, render_song_grid,
    render_player, render_mini_player,
    render_llm_thinking, render_llm_response,
    render_mood_selector, render_scene_selector,
    render_chat_message, render_chat_history, render_quick_questions,
    render_stat_card, render_empty_state, render_notification,
    render_loading_spinner, render_equalizer_animation
)

# ========== 3. 导入业务层 ==========
from llm_engine import LLMEngineFactory
from music_logic import MusicRecommender, MusicKnowledgeService

# ========== 4. 页面配置 ==========
st.set_page_config(
    page_title="🎵 AI 智能音乐平台",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== 5. 全局 CSS（霓虹赛博朋克主题）==========
st.markdown("""
<style>
    :root {
        --bg-primary: #0a0a0a;
        --text-primary: #e0e0e0;
        --accent-primary: #00f2fe;
        --accent-secondary: #ff00ff;
    }

    /* 背景 */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0a2e 50%, #0a0a0a 100%) !important;
    }

    /* 只给 h1-h6 加渐变文字 */
    h1, h2, h3, h4, h5, h6 {
        background: linear-gradient(90deg, #00f2fe, #ff00ff) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }

    /* 普通文字保持可见 */
    body, p, span, div, label, li {
        color: #e0e0e0 !important;
    }

    /* 按钮 */
    .stButton>button {
        background: linear-gradient(135deg, #00f2fe, #ff00ff) !important;
        color: #000 !important;
    }

    /* 滚动条 */
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00f2fe, #ff00ff);
    }
</style>
""", unsafe_allow_html=True)

# ========== 6. 初始化 Session State（修复：共享引擎）==========
if "recommender" not in st.session_state:
    # 只创建一次引擎，两个服务共享
    llm_engine = LLMEngineFactory.create()

    st.session_state.recommender = MusicRecommender(llm=llm_engine)
    st.session_state.knowledge_service = MusicKnowledgeService(llm=llm_engine)
    st.session_state.current_song = None
    st.session_state.is_playing = False
    st.session_state.play_history = []
    st.session_state.chat_history = []
    st.session_state.selected_mood = None
    st.session_state.selected_scene = None

# 获取服务实例
recommender = st.session_state.recommender
knowledge_service = st.session_state.knowledge_service

# ========== 7. 页面头部 ==========
render_header("🎵 AI 智能音乐平台", "基于大语言模型的个性化音乐推荐与知识服务")

# ========== 8. 顶部导航 ==========
tabs = st.tabs(["🎭 应景音乐", "▶️ 在线播放", "💡 音乐知识问答"])

# ========== 板块一：应景音乐 ==========
with tabs[0]:
    render_section_title("🎭", "应景音乐推荐")

    sub_tabs = st.tabs(["🎨 按情绪推荐", "🏃 按场景推荐"])

    # --- 情绪推荐 ---
    with sub_tabs[0]:
        selected_mood = render_mood_selector([
            ("欢快", "mood-happy", "😊"),
            ("悲伤", "mood-sad", "😢"),
            ("愉悦", "mood-joy", "😄"),
            ("激昂", "mood-excited", "🔥"),
            ("平静", "mood-calm", "🌊")
        ])

        if selected_mood:
            st.session_state.selected_mood = selected_mood
        elif st.session_state.selected_mood:
            selected_mood = st.session_state.selected_mood

        if selected_mood:
            with render_loading_spinner(f"AI 正在分析「{selected_mood}」音乐特征..."):
                result = recommender.get_mood_recommendations(selected_mood)
                llm_response = result["llm_analysis"]

                # LLM 推理过程
                render_llm_thinking(
                    llm_response.reasoning,
                    llm_response.confidence,
                    expanded=True
                )

                # LLM 推荐文案
                render_llm_response(llm_response.content, "📝 AI 推荐语")

                # 歌曲列表
                st.markdown("#### 🎵 推荐歌单")
                for song in result["songs"]:
                    render_song_card(
                        song,
                        on_play=lambda s: (
                            st.session_state.update({
                                "current_song": s,
                                "is_playing": True
                            }),
                            st.session_state.play_history.append(s),
                            st.rerun()
                        )[-1]
                    )

    # --- 场景推荐 ---
    with sub_tabs[1]:
        selected_scene = render_scene_selector([
            ("跑步", "🏃", "动感节奏，匹配步频"),
            ("睡眠", "🌙", "助眠音乐，432Hz调音"),
            ("放松", "🧘", "疗愈轻音乐，自然音效")
        ])

        if selected_scene:
            st.session_state.selected_scene = selected_scene
        elif st.session_state.selected_scene:
            selected_scene = st.session_state.selected_scene

        if selected_scene:
            with render_loading_spinner(f"AI 正在匹配「{selected_scene}」最佳音乐..."):
                result = recommender.get_scene_recommendations(selected_scene)
                llm_response = result["llm_analysis"]

                render_llm_thinking(llm_response.reasoning, llm_response.confidence)
                render_llm_response(llm_response.content, "📝 AI 场景推荐")

                st.markdown("#### 🎵 场景歌单")
                for i, song in enumerate(result["songs"], 1):
                    cols = st.columns([0.5, 3, 1.5, 1])
                    with cols[0]:
                        st.markdown(f"<div style='text-align:center'>#{i}</div>", unsafe_allow_html=True)
                    with cols[1]:
                        st.markdown(f"**{song['title']}** - {song['artist']}")
                        st.caption(song['description'][:50] + "...")
                    with cols[2]:
                        if selected_scene == "跑步":
                            st.markdown(f"🏃 配速：{song['tempo']//2}步/分")
                        else:
                            st.markdown(f"{'🌙' if selected_scene=='睡眠' else '🧘'} 指数：{100-int(song['energy']*100)}%")
                    with cols[3]:
                        if st.button("▶️", key=f"scene_play_{song['id']}"):
                            st.session_state.current_song = song
                            st.session_state.is_playing = True
                            st.session_state.play_history.append(song)
                            st.rerun()

# ========== 板块二：在线播放 ==========
with tabs[1]:
    render_section_title("▶️", "在线音乐播放")

    current_song = st.session_state.current_song
    is_playing = st.session_state.is_playing

    # 播放器
    if current_song:
        render_player(
            current_song,
            is_playing=is_playing,
            on_play_pause=lambda: (
                st.session_state.update({"is_playing": not is_playing}),
                st.rerun()
            )[-1],
            on_next=lambda: _play_next(recommender),
            on_prev=lambda: _play_prev(),
            on_random=lambda: _play_random(recommender),
            progress=0.35
        )
    else:
        render_empty_state("🎵", "暂无播放中的歌曲", "请从「应景音乐」板块选择歌曲")

    render_divider()

    # 每日推荐
    st.markdown("#### ✨ 每日智能推荐")
    if st.button("🔄 生成今日推荐", use_container_width=True):
        with render_loading_spinner("AI 正在分析您的音乐口味..."):
            daily = recommender.get_daily_recommendations(6)
            llm_insight = daily["llm_insight"]

            render_llm_response(llm_insight.content, "🤖 AI 播放列表洞察")

            # 歌曲网格
            render_song_grid(
                daily["songs"],
                cols=3,
                on_play=lambda s: (
                    st.session_state.update({"current_song": s, "is_playing": True}),
                    st.session_state.play_history.append(s),
                    st.rerun()
                )[-1]
            )

    # 播放历史
    if st.session_state.play_history:
        with st.expander("📜 播放历史"):
            for song in st.session_state.play_history[-10:]:
                st.markdown(f"{song['cover']} **{song['title']}** - {song['artist']}")

# ========== 板块三：音乐知识问答 ==========
with tabs[2]:
    render_section_title("💡", "音乐知识你问我答")

    # 介绍
    render_notification(
        "🤖 AI 音乐导师已就位！您可以询问乐理知识、音乐历史、乐器知识、流派辨析、演奏技巧等任何问题。",
        "info"
    )

    # 快捷问题
    render_quick_questions([
        "什么是五声音阶？",
        "为什么古典音乐有助于提高专注力？",
        "电子音乐中的'Drop'是什么意思？",
        "爵士乐中的'即兴演奏'是如何进行的？",
        "为什么有些歌一听就让人感到悲伤？",
        "什么是'概念专辑'？"
    ], on_select=lambda q: st.session_state.update({"pending_question": q}))

    render_divider()

    # 聊天历史
    st.markdown("#### 💬 对话记录")
    render_chat_history(st.session_state.chat_history)

    render_divider()

    # 输入框
    default_value = st.session_state.pop("pending_question", "")
    user_question = st.text_input(
        "输入您的问题...",
        value=default_value,
        placeholder="例如：为什么小调听起来比较悲伤？",
        key="question_input"
    )

    if st.button("🚀 提问", use_container_width=True) and user_question:
        with render_loading_spinner("AI 音乐导师思考中..."):
            # 添加用户消息
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })

            # 调用知识服务
            result = knowledge_service.ask(user_question)
            answer = result["answer"]

            # 添加助手消息
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": answer.content,
                "reasoning": answer.reasoning,
                "confidence": answer.confidence,
                "source": result["source"]
            })

            # 来源信息
            if result["matched_knowledge"]:
                render_notification(
                    f"📚 知识来源：{result['matched_knowledge']['category']} | 难度：{result['matched_knowledge']['difficulty']}",
                    "info"
                )

            # 相关问题
            if result["related_questions"]:
                with st.expander("📎 相关问题推荐"):
                    for q in result["related_questions"]:
                        st.markdown(f"- {q}")

            st.rerun()

    # 清空对话
    if st.session_state.chat_history and st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ========== 页脚 ==========
render_divider()
st.markdown("""
<div style="text-align:center; color:#666; padding:1rem;">
    <small>🎵 AI 智能音乐平台 | Powered by Streamlit + Python LLM Engine</small>
</div>
""", unsafe_allow_html=True)


# ========== 辅助函数 ==========
def _play_next(recommender):
    """播放下一首"""
    next_song = recommender.library.get_random(1)[0]
    song_dict = recommender._song_to_dict(next_song)
    st.session_state.current_song = song_dict
    st.session_state.play_history.append(song_dict)
    st.rerun()

def _play_prev():
    """播放上一首"""
    history = st.session_state.play_history
    if len(history) > 1:
        st.session_state.current_song = history[-2]
    st.rerun()

def _play_random(recommender):
    """随机播放"""
    random_song = recommender.library.get_random(1)[0]
    song_dict = recommender._song_to_dict(random_song)
    st.session_state.current_song = song_dict
    st.session_state.play_history.append(song_dict)
    st.rerun()
