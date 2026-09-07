import os
import json
import datetime
from pathlib import Path

import streamlit as st

# ============================================================
# JHOSAI REX MODEL — CLEAN APP DASHBOARD
# ============================================================

st.set_page_config(
    page_title="JHOSAI REX Model",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_DIR = Path(__file__).resolve().parent
LOGO_CANDIDATES = [
    APP_DIR / "jhosai_rex_logo.png",
    APP_DIR / "jhosai_rex_logo.png(1).png",
    APP_DIR / "jhosai_rex_logo_original.png",
]
LOGO_PATH = next(
    (p for p in LOGO_CANDIDATES if p.exists()),
    next(iter(APP_DIR.glob("jhosai_rex_logo*.png")), APP_DIR / "jhosai_rex_logo.png"),
)
SESSIONS_DIR = APP_DIR / "saved_sessions"
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

AUTOMATIC_MODEL = "Automatic — Free fallback"

KNOWN_FREE_MODELS = [
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "nvidia/nemotron-3.5-lightning:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
]

FREE_MODEL_CACHE_SECONDS = 300


# ----------------------------
# Session state
# ----------------------------
for key, default in {
    "messages": [],
    "conversations": [],
    "uploaded_files": [],
    "model": AUTOMATIC_MODEL,
    "show_upload": False,
    "last_model_used": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ----------------------------
# Safe, non-HTML UI styling
# ----------------------------
st.markdown(
    """
    <style>
    .stApp { background: #080A0D; color: #F5F7FA; }
    [data-testid="stHeader"] { background: #080A0D; }
    .block-container { max-width: 1180px; padding-top: 1.5rem; padding-bottom: 7rem; }

    section[data-testid="stSidebar"] {
        background: #0B0D10;
        border-right: 1px solid #1B2026;
    }
    section[data-testid="stSidebar"] * { color: #F5F7FA; }

    h1, h2, h3, h4, p, span, label { color: #F5F7FA; }
    .stCaption, [data-testid="stCaptionContainer"] { color: #9BA3AD !important; }

    div[data-testid="stChatMessage"] {
        background: #101419;
        border: 1px solid #20272E;
        border-radius: 14px;
        margin-bottom: 12px;
        padding: 0.35rem 0.8rem;
    }

    [data-testid="stChatInput"] {
        background: #151A1F;
        border: 1px solid #2B333A;
        border-radius: 14px;
    }
    [data-testid="stChatInput"] textarea {
        color: #F5F7FA !important;
        caret-color: #00F5FF;
    }
    [data-testid="stChatInput"] textarea::placeholder { color: #7F8994 !important; }

    .stButton > button {
        border-radius: 10px;
        border: 1px solid #293139;
        background: #11161A;
        color: #F5F7FA;
    }
    .stButton > button:hover {
        border-color: #00EAF2;
        color: #00EAF2;
    }

    [data-baseweb="select"] > div {
        background: #151A1F;
        border-color: #303940;
        color: #F5F7FA;
    }
    [data-baseweb="select"] * { color: #F5F7FA !important; }

    [data-testid="stFileUploader"] {
        background: #101419;
        border: 1px solid #252D34;
        border-radius: 12px;
    }

    hr { border-color: #20262C; }
    .rex-status {
        color: #00F5FF !important;
        font-weight: 700;
        letter-spacing: 0.08em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# OpenRouter backend
# ============================================================

def _is_free_model(model: dict) -> bool:
    pricing = model.get("pricing") or {}
    try:
        prompt_price = float(pricing.get("prompt", 1))
        completion_price = float(pricing.get("completion", 1))
    except (TypeError, ValueError):
        return False

    if prompt_price != 0 or completion_price != 0:
        return False

    model_id = str(model.get("id", "")).lower()
    blocked = (
        "embed", "rerank", "moderation", "content-safety",
        "whisper", "asr", "transcription", "tts", "audio", "speech",
    )
    return bool(model_id) and not any(word in model_id for word in blocked)


@st.cache_data(ttl=FREE_MODEL_CACHE_SECONDS, show_spinner=False)
def discover_free_models():
    """Fetch currently listed free chat-capable models from OpenRouter."""
    import urllib.request

    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/models",
        headers={
            "Accept": "application/json",
            "User-Agent": "JHOSAI-REX-Model/1.0",
        },
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        payload = json.loads(response.read().decode("utf-8"))

    discovered = [
        str(item["id"])
        for item in payload.get("data", [])
        if _is_free_model(item)
    ]

    ordered = []
    for model_id in KNOWN_FREE_MODELS:
        if model_id in discovered:
            ordered.append(model_id)
    for model_id in discovered:
        if model_id not in ordered:
            ordered.append(model_id)

    return ordered[:40]


def get_free_models():
    try:
        models = discover_free_models()
        return models or KNOWN_FREE_MODELS.copy()
    except Exception:
        return KNOWN_FREE_MODELS.copy()


def generate_response(prompt: str, history=None, files=None, model=None) -> str:
    """Send the conversation to OpenRouter using the existing setup."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return (
            "OpenRouter is not configured yet. Set the environment variable "
            "OPENROUTER_API_KEY in PowerShell, then restart Streamlit."
        )

    try:
        from openai import OpenAI
    except ImportError:
        return "The Python package 'openai' is missing. Run: pip install openai"

    model = model or st.session_state.model
    history = history or []

    free_models = get_free_models()
    if model == AUTOMATIC_MODEL:
        model = free_models[0] if free_models else KNOWN_FREE_MODELS[0]
    files = files or []

    messages = []
    for item in history:
        role = item.get("role")
        content = item.get("content", "")
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})

    file_names = [getattr(f, "name", "file") for f in files]
    if file_names:
        prompt = prompt + "\n\nAttached files: " + ", ".join(file_names)

    messages.append({"role": "user", "content": prompt})

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": "JHOSAI REX Model",
            },
        )

        # OpenRouter accepts at most 3 models in the fallback array.
        # Keep the primary model plus two alternatives.
        fallback_models = [
            model,
            *[m for m in free_models if m != model][:2],
        ]

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1500,
            extra_body={"models": fallback_models},
        )

        st.session_state.last_model_used = getattr(response, "model", None) or model

        return response.choices[0].message.content or "REX did not return a response."

    except Exception as exc:
        return f"REX Model error: {exc}"

# ============================================================
# Session helpers
# ============================================================

def save_current_session():
    if not st.session_state.messages:
        return

    title = st.session_state.messages[0].get("content", "Conversation").strip()
    title = title[:40] + ("..." if len(title) > 40 else "")
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    data = {
        "title": title,
        "messages": st.session_state.messages,
        "updated": datetime.datetime.now().isoformat(),
    }
    (SESSIONS_DIR / f"session_{stamp}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=210)
    else:
        st.title("JHOSAI REX")
        st.caption("MODEL BOT")
        st.caption("Logo file not found in project folder.")

    st.divider()

    if st.button("＋  New chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.uploaded_files = []
        st.session_state.show_upload = False
        st.rerun()

    st.caption("MODEL")
    free_models = get_free_models()
    model_options = [AUTOMATIC_MODEL] + free_models
    current_model = (
        st.session_state.model
        if st.session_state.model in model_options
        else AUTOMATIC_MODEL
    )

    st.session_state.model = st.selectbox(
        "Model",
        model_options,
        index=model_options.index(current_model),
        label_visibility="collapsed",
    )
    st.caption(f"{len(free_models)} free models available")

    st.divider()
    st.caption("TODAY")
    if st.session_state.messages:
        title = st.session_state.messages[0].get("content", "Conversation")
        st.button(title[:32], disabled=True, use_container_width=True)
    else:
        st.caption("No conversations yet.")

    st.divider()
    st.caption("WORKSPACE")
    if st.button("⌕  Search conversations", use_container_width=True):
        st.info("Conversation search will be available here.")
    if st.button("⚙  Settings", use_container_width=True):
        st.info("Settings")

    st.divider()
    st.caption("JHOSAI REX MODEL")

# ============================================================
# TOP BAR
# ============================================================
top_left, top_right = st.columns([7, 3])
with top_left:
    st.markdown('### <span class="rex-status">● REX</span>', unsafe_allow_html=True)
    st.caption("JHOSAI REX Model")
with top_right:
    st.caption("ACTIVE MODEL")
    st.write(st.session_state.last_model_used or st.session_state.model)

# ============================================================
# MAIN CONTENT
# ============================================================
if not st.session_state.messages:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=300)
    st.title("What are we working on?")
    st.caption("JHOSAI REX Model is ready.")
else:
    for message in st.session_state.messages:
        role = message.get("role", "assistant")
        content = message.get("content", "")
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(content)

# ============================================================
# ATTACHMENTS
# ============================================================
attach_col, upload_col = st.columns([1, 9])
with attach_col:
    if st.button("＋", help="Attach files"):
        st.session_state.show_upload = not st.session_state.show_upload

with upload_col:
    if st.session_state.show_upload:
        uploaded = st.file_uploader(
            "Attach files",
            type=["pdf", "txt", "docx", "csv", "json", "png", "jpg", "jpeg"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )
        if uploaded:
            st.session_state.uploaded_files = uploaded
            st.caption("Attached: " + ", ".join(f.name for f in uploaded))

# ============================================================
# CHAT INPUT
# ============================================================
prompt = st.chat_input("Ask REX anything...")

if prompt:
    history = list(st.session_state.messages)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("REX is thinking..."):
        response = generate_response(
            prompt,
            history=history,
            files=st.session_state.uploaded_files,
            model=st.session_state.model,
        )

    st.session_state.messages.append({"role": "assistant", "content": str(response)})
    save_current_session()
    st.rerun()

st.caption("JHOSAI REX Model · AI responses may require verification")
