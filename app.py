import time
from uuid import uuid4

import streamlit as st
from agent.react_agent import ReactAgent

st.set_page_config(
    page_title="萌爪管家",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- 样式注入 ----------
THEME_CSS = """
<style>
:root {
    --primary: #FF6B35;
    --primary-soft: #FFB199;
    --bg-soft: #FFF8F2;
    --card-bg: #FFFFFF;
    --card-border: #FFD7BA;
    --user-bubble: linear-gradient(135deg, #FF8A65 0%, #FF6B35 100%);
    --bot-bubble: #FFFFFF;
    --text-main: #1F1A17;
    --text-soft: #4A4039;
    --shadow: 0 4px 16px rgba(255, 107, 53, 0.12);
}

html, body, .stApp, [data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"], [data-testid="stMain"] {
    background: #FFF8F2 !important;
    color: var(--text-main) !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { background: transparent !important; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

section[data-testid="stSidebar"] > div {
    background: #FFFFFF !important;
    border-right: 1px solid var(--card-border);
}

section[data-testid="stSidebar"] * {
    color: var(--text-main) !important;
}
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
section[data-testid="stSidebar"] small,
section[data-testid="stSidebar"] .stMarkdown p {
    color: var(--text-soft) !important;
    font-weight: 500;
}
section[data-testid="stSidebar"] details summary,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] ul {
    color: var(--text-main) !important;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: var(--text-main) !important;
}

.hero {
    text-align: center;
    padding: 1.5rem 1rem 0.5rem;
}
.hero h1 {
    font-size: 2.4rem;
    color: var(--primary) !important;
    margin-bottom: 0.3rem;
}
.hero p {
    color: var(--text-soft) !important;
    font-size: 1rem;
    font-weight: 500;
}

[data-testid="stChatMessage"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 18px !important;
    padding: 1rem 1.2rem !important;
    box-shadow: var(--shadow) !important;
    color: var(--text-main) !important;
    margin-bottom: 0.6rem !important;
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span {
    color: var(--text-main) !important;
}

[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4,
[data-testid="stMain"] h5,
[data-testid="stMain"] h6,
[data-testid="stMain"] [data-testid="stHeadingWithActionElements"] h1,
[data-testid="stMain"] [data-testid="stHeadingWithActionElements"] h2,
[data-testid="stMain"] [data-testid="stHeadingWithActionElements"] h3,
[data-testid="stMain"] [data-testid="stHeadingWithActionElements"] h4,
[data-testid="stMain"] [data-testid="stHeadingWithActionElements"] h5,
[data-testid="stMain"] [data-testid="stHeadingWithActionElements"] h6,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h3,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h4 {
    color: #1F1A17 !important;
    -webkit-text-fill-color: #1F1A17 !important;
    background: none !important;
    background-image: none !important;
    -webkit-background-clip: initial !important;
    background-clip: initial !important;
    font-weight: 700 !important;
}
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h1 { font-size: 1.8rem !important; margin-top: 0.5rem !important; }
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h2 { font-size: 1.4rem !important; }
[data-testid="stMain"] [data-testid="stMarkdownContainer"] h3 { font-size: 1.15rem !important; }

[data-testid="stMain"] p,
[data-testid="stMain"] li,
[data-testid="stMain"] span,
[data-testid="stMain"] strong,
[data-testid="stMain"] em,
[data-testid="stMain"] code,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] p,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] li,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] strong {
    color: var(--text-main) !important;
}
[data-testid="stMain"] [data-testid="stMarkdownContainer"] a {
    color: var(--primary) !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #1F1A17 !important;
    -webkit-text-fill-color: #1F1A17 !important;
    background: none !important;
    background-image: none !important;
    -webkit-background-clip: initial !important;
    background-clip: initial !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: var(--user-bubble) !important;
    border: none !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) p,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) li {
    color: #FFFFFF !important;
}

.suggestion-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    justify-content: center;
    margin: 1.2rem auto 0.5rem;
    max-width: 720px;
}

.stButton > button {
    background: #FFFFFF !important;
    color: var(--text-main) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 999px !important;
    padding: 0.5rem 1rem !important;
    font-weight: 500 !important;
    box-shadow: var(--shadow) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: var(--primary) !important;
    color: #FFFFFF !important;
    border-color: var(--primary) !important;
    transform: translateY(-1px) !important;
}
.stButton > button p,
.stButton > button span {
    color: inherit !important;
}

[data-testid="stChatInput"] textarea {
    border-radius: 18px !important;
    border: 1px solid var(--card-border) !important;
    background: #FFFFFF !important;
    color: var(--text-main) !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #B8A99A !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] [data-baseweb="textarea"],
[data-testid="stChatInput"] [data-baseweb="base-input"],
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"],
[data-testid="stBottom"] > div {
    background: #FFF8F2 !important;
    background-color: #FFF8F2 !important;
}
[data-testid="stChatInput"] * {
    background-color: transparent !important;
}
[data-testid="stChatInput"] [data-baseweb="textarea"] {
    background: #FFFFFF !important;
}

section[data-testid="stSidebar"] details,
section[data-testid="stSidebar"] details > summary,
section[data-testid="stSidebar"] details > div,
section[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 12px !important;
}
section[data-testid="stSidebar"] details > summary {
    color: var(--text-main) !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] details > summary:hover {
    background: #FFF8F2 !important;
}
section[data-testid="stSidebar"] details * {
    color: var(--text-main) !important;
}

.sidebar-stat {
    background: #FFF8F2;
    border: 1px solid var(--card-border);
    border-radius: 14px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
}
.sidebar-stat .label { color: var(--text-soft) !important; font-size: 0.85rem; font-weight: 500; }
.sidebar-stat .value { color: var(--text-main) !important; font-size: 1.3rem; font-weight: 700; }

section[data-testid="stSidebar"] [data-testid="stDivider"] {
    border-color: var(--card-border) !important;
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div,
section[data-testid="stSidebar"] [data-baseweb="input"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    color: var(--text-main) !important;
    border-color: var(--card-border) !important;
}

section[data-testid="stSidebar"] [data-baseweb="popover"] > div,
section[data-testid="stSidebar"] [data-baseweb="popover"] > div > div,
section[data-testid="stSidebar"] [data-baseweb="popover"] [role="dialog"],
section[data-testid="stSidebar"] [data-baseweb="popover"] [data-testid="stModal"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    color: var(--text-main) !important;
}

[data-baseweb="menu"] [role="option"],
[data-baseweb="menu"] [role="listbox"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    color: var(--text-main) !important;
}
[data-baseweb="menu"] [role="option"]:hover,
[data-baseweb="menu"] [role="option"][aria-selected="true"] {
    background: #FFF8F2 !important;
    color: var(--primary) !important;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] strong,
section[data-testid="stSidebar"] b,
section[data-testid="stSidebar"] div {
    color: var(--text-main) !important;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p strong,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong {
    color: var(--text-main) !important;
}

[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
[data-testid="stSidebar"] [data-testid="stSelectbox"] *,
[data-testid="stSidebar"] [data-testid="stSelectbox"],
[data-testid="stSidebar"] div[class*="react-aria-ComboBox"],
[data-testid="stSidebar"] div[class*="react-aria-ComboBox"] * {
    background-color: #FFFFFF !important;
    color: var(--text-main) !important;
}

[data-testid="stSidebar"] [data-testid="stSelectbox"] input,
[data-testid="stSidebar"] div[class*="react-aria-ComboBox"] input,
[data-testid="stSidebar"] div[class*="react-aria-ComboBox"] button {
    background-color: #FFFFFF !important;
    color: var(--text-main) !important;
    caret-color: var(--text-main) !important;
}

[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"],
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] > div,
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] > div > div,
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] span,
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] p,
[data-testid="stSidebar"] [data-testid="stPopoverButton"],
[data-testid="stSidebar"] [data-testid="stPopoverButton"] > div,
[data-testid="stSidebar"] [data-testid="stPopoverButton"] > div > div,
[data-testid="stSidebar"] [data-testid="stPopoverButton"] span,
[data-testid="stSidebar"] [data-testid="stPopoverButton"] p,
[data-testid="stSidebar"] [data-testid="stPopoverButton"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stPopoverButton"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stPopoverButton"] [data-testid="stIconMaterial"],
[data-testid="stSidebar"] button[data-testid],
[data-testid="stSidebar"] button[data-testid] > div,
[data-testid="stSidebar"] button[data-testid] span,
[data-testid="stSidebar"] button[data-testid] p {
    background-color: #FFFFFF !important;
    color: var(--text-main) !important;
    border-color: var(--card-border) !important;
}

[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover,
[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover *,
[data-testid="stSidebar"] [data-testid="stPopoverButton"]:hover,
[data-testid="stSidebar"] [data-testid="stPopoverButton"]:hover *,
[data-testid="stSidebar"] [data-testid="stPopoverButton"]:hover [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stPopoverButton"]:hover [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stPopoverButton"]:hover [data-testid="stIconMaterial"] {
    background-color: var(--primary) !important;
    color: #FFFFFF !important;
}

[role="listbox"], [role="listbox"] *,
[role="option"], [role="option"] * {
    background-color: #FFFFFF !important;
    color: var(--text-main) !important;
}
[role="option"][aria-selected="true"],
[role="option"][aria-selected="true"] *,
[role="option"]:hover,
[role="option"]:hover * {
    background-color: #FFF8F2 !important;
    color: var(--primary) !important;
}

[data-testid="stSidebar"] [data-testid="stPopoverContent"],
[data-testid="stSidebar"] [data-testid="stPopoverContent"] * {
    background-color: #FFFFFF !important;
    color: var(--text-main) !important;
}

[data-testid="stSidebar"] input[type="text"],
[data-testid="stSidebar"] input[type="text"]::placeholder {
    background-color: #FFFFFF !important;
    color: var(--text-main) !important;
}
</style>
"""

st.markdown(THEME_CSS, unsafe_allow_html=True)


# ---------- 会话状态 ----------
if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "conversations" not in st.session_state:
    first_id = uuid4().hex
    st.session_state["conversations"] = {
        first_id: {"title": "新对话", "messages": []},
    }
    st.session_state["current_conv_id"] = first_id

if "pending_prompt" not in st.session_state:
    st.session_state["pending_prompt"] = None

if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = {
        "name": "萌宠家长",
        "city": "深圳",
    }


def _current_conv():
    return st.session_state["conversations"][st.session_state["current_conv_id"]]


def _auto_title(text: str) -> str:
    text = text.strip().replace("\n", " ")
    return (text[:12] + "…") if len(text) > 12 else text


# ---------- 侧边栏 ----------
with st.sidebar:
    st.markdown("### 🐾 萌爪管家")
    st.caption("您的专属宠物健康顾问")

    st.markdown('<div class="sidebar-stat"><div class="label">用户</div>'
                f'<div class="value">{st.session_state["user_profile"]["name"]}</div></div>',
                unsafe_allow_html=True)

    user_count = sum(1 for m in _current_conv()["messages"] if m["role"] == "user")
    st.markdown('<div class="sidebar-stat"><div class="label">本轮对话</div>'
                f'<div class="value">{user_count} 次提问</div></div>',
                unsafe_allow_html=True)

    st.divider()
    st.markdown("**💬 会话**")

    conv_items = list(st.session_state["conversations"].items())
    conv_options = [f"{title}  ·  {cid[:4]}" for cid, _conv in conv_items for title in [_conv["title"]]]
    current_idx = next(
        (i for i, (cid, _) in enumerate(conv_items) if cid == st.session_state["current_conv_id"]),
        0,
    )

    col_sel, col_new = st.columns([5, 1])
    with col_sel:
        selected_label = st.selectbox(
            "切换会话",
            options=conv_options,
            index=current_idx,
            label_visibility="collapsed",
            key="conv_select",
        )
    with col_new:
        if st.button("➕", help="新建对话", use_container_width=True):
            new_id = uuid4().hex
            st.session_state["conversations"][new_id] = {"title": "新对话", "messages": []}
            st.session_state["current_conv_id"] = new_id
            st.session_state["pending_prompt"] = None
            st.rerun()

    if selected_label:
        chosen_idx = conv_options.index(selected_label)
        chosen_id = conv_items[chosen_idx][0]
        if chosen_id != st.session_state["current_conv_id"]:
            st.session_state["current_conv_id"] = chosen_id
            st.session_state["pending_prompt"] = None
            st.rerun()

    col_rename, col_delete = st.columns(2)
    with col_rename:
        if st.button("✏️ 重命名", use_container_width=True):
            st.session_state["show_rename"] = True
    with col_delete:
        if st.button("🗑️ 删除", use_container_width=True):
            st.session_state["show_delete_confirm"] = True

    if st.session_state.get("show_rename"):
        with st.popover("重命名当前会话", use_container_width=True):
            new_title = st.text_input(
                "新标题",
                value=_current_conv()["title"],
                label_visibility="collapsed",
                key="rename_input",
            )
            col_ok, col_cancel = st.columns(2)
            with col_ok:
                if st.button("保存", use_container_width=True, key="rename_ok"):
                    if new_title.strip():
                        _current_conv()["title"] = new_title.strip()
                    st.session_state["show_rename"] = False
                    st.rerun()
            with col_cancel:
                if st.button("取消", use_container_width=True, key="rename_cancel"):
                    st.session_state["show_rename"] = False
                    st.rerun()

    if st.session_state.get("show_delete_confirm"):
        st.warning(f"确认删除「{_current_conv()['title']}」？此操作不可恢复。")
        col_y, col_n = st.columns(2)
        with col_y:
            if st.button("确认删除", use_container_width=True, key="del_yes"):
                del st.session_state["conversations"][st.session_state["current_conv_id"]]
                if not st.session_state["conversations"]:
                    new_id = uuid4().hex
                    st.session_state["conversations"][new_id] = {"title": "新对话", "messages": []}
                st.session_state["current_conv_id"] = next(iter(st.session_state["conversations"]))
                st.session_state["show_delete_confirm"] = False
                st.session_state["pending_prompt"] = None
                st.rerun()
        with col_n:
            if st.button("取消", use_container_width=True, key="del_no"):
                st.session_state["show_delete_confirm"] = False
                st.rerun()

    st.divider()
    with st.expander("💡 我可以帮你", expanded=False):
        st.markdown("""
        - 日常饲养咨询(猫狗/其他家养宠物)
        - 常见疾病判断与处理
        - 健康护理与饮食建议
        - 行为解读与训练建议
        - 用品选购与清洁美容
        - 本月宠物使用情况报告
        """)


# ---------- 主体 ----------
st.markdown(
    '<div class="hero"><h1>🐾 萌爪管家</h1>'
    '<p>专注猫狗与家养宠物的健康、饲养与护理咨询</p></div>',
    unsafe_allow_html=True,
)

SUGGESTIONS = [
    "幼犬多久打一次疫苗？",
    "猫咪挑食不吃猫粮怎么办？",
    "狗狗拉稀怎么处理？",
    "新手养猫需要准备什么？",
    "兔子能洗澡吗？",
    "仓鼠一直咬笼子是为什么？",
]

for message in _current_conv()["messages"]:
    st.chat_message(message["role"]).write(message["content"])

if not _current_conv()["messages"]:
    st.markdown('<div class="suggestion-wrap">', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, q in enumerate(SUGGESTIONS):
        with cols[i % 3]:
            if st.button(q, key=f"sug_{i}", use_container_width=True):
                st.session_state["pending_prompt"] = q
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

prompt = st.session_state.get("pending_prompt") or st.chat_input("向萌爪管家提问…")

if prompt:
    st.session_state["pending_prompt"] = None
    st.chat_message("user").write(prompt)
    _current_conv()["messages"].append({"role": "user", "content": prompt})
    if _current_conv()["title"] == "新对话":
        _current_conv()["title"] = _auto_title(prompt)

    response_messages = []
    with st.spinner("🐾 智能客服思考中…"):
        res_stream = st.session_state["agent"].execute_stream(prompt)

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                for char in chunk:
                    time.sleep(0.01)
                    yield char

        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        _current_conv()["messages"].append({"role": "assistant", "content": response_messages[-1]})
        st.rerun()