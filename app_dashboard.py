import os
import io
import json
import datetime
from pathlib import Path

import streamlit as st


# ============================================================
# JHOSAI REX MODEL — UPGRADED EXISTING DASHBOARD
# ============================================================

st.set_page_config(
    page_title="JHOSAI REX Model",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_DIR = Path(__file__).resolve().parent


# ============================================================
# LOGO
# ============================================================

LOGO_CANDIDATES = [
    APP_DIR / "jhosai_rex_logo.png",
    APP_DIR / "jhosai_rex_logo.png(1).png",
    APP_DIR / "jhosai_rex_logo.png.png",
    APP_DIR / "jhosai_rex_logo_original.png",
]

LOGO_PATH = next(
    (p for p in LOGO_CANDIDATES if p.exists()),
    next(
        iter(APP_DIR.glob("jhosai_rex_logo*.png")),
        APP_DIR / "jhosai_rex_logo.png",
    ),
)


# ============================================================
# SESSION STORAGE
# ============================================================

SESSIONS_DIR = APP_DIR / "saved_sessions"
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# MODEL SETTINGS
# ============================================================

AUTOMATIC_MODEL = "Automatic — Free fallback"

KNOWN_FREE_MODELS = [
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "nvidia/nemotron-3.5-lightning:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
]

FREE_MODEL_CACHE_SECONDS = 300
MAX_FILE_CHARS = 30000


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "messages": [],
    "model": AUTOMATIC_MODEL,
    "last_model_used": "",
    "last_prompt": "",
    "last_files": [],
    "search_term": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# JHOSAI REX DARK UI
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL APPLICATION
       ======================================================== */

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background-color: #080A0D !important;
        color: #F5F7FA !important;
    }

    [data-testid="stMainBlockContainer"],
    .block-container {
        background-color: #080A0D !important;
    }

    [data-testid="stHeader"] {
        background-color: #080A0D !important;
    }

    [data-testid="stDecoration"] {
        background-color: #080A0D !important;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background-color: #0B0D10 !important;
        border-right: 1px solid #1B2026 !important;
    }

    section[data-testid="stSidebar"] > div {
        background-color: #0B0D10 !important;
    }

    [data-testid="stSidebarContent"] {
        background-color: #0B0D10 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #F5F7FA;
    }

    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"],
    section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
        background-color: transparent !important;
    }


    /* ========================================================
       GENERAL TEXT
       ======================================================== */

    h1,
    h2,
    h3,
    h4,
    p,
    span,
    label {
        color: #F5F7FA;
    }

    [data-testid="stCaptionContainer"],
    .stCaption {
        color: #9BA3AD !important;
    }


    /* ========================================================
       MODEL SELECTOR
       DARK BOX + VISIBLE WHITE TEXT
       ======================================================== */

    [data-testid="stSelectbox"] [data-baseweb="select"] {
        background-color: #151A1F !important;
        border-color: #303940 !important;
    }

    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background-color: #151A1F !important;
        border: 1px solid #303940 !important;
        color: #F5F7FA !important;
    }

    [data-testid="stSelectbox"] [data-baseweb="select"] div {
        background-color: #151A1F !important;
        color: #F5F7FA !important;
    }

    [data-testid="stSelectbox"] [data-baseweb="select"] span {
        color: #F5F7FA !important;
        -webkit-text-fill-color: #F5F7FA !important;
    }

    [data-testid="stSelectbox"] [data-baseweb="select"] input {
        color: #F5F7FA !important;
        -webkit-text-fill-color: #F5F7FA !important;
    }

    [data-testid="stSelectbox"] svg {
        color: #F5F7FA !important;
        fill: #F5F7FA !important;
    }


    /* ========================================================
       MODEL DROPDOWN MENU
       ======================================================== */

    [data-baseweb="popover"] {
        background-color: #151A1F !important;
    }

    [data-baseweb="popover"] > div {
        background-color: #151A1F !important;
    }

    [data-baseweb="menu"] {
        background-color: #151A1F !important;
    }

    [data-baseweb="menu"] li {
        background-color: #151A1F !important;
        color: #F5F7FA !important;
    }

    [data-baseweb="menu"] li * {
        color: #F5F7FA !important;
    }

    [data-baseweb="menu"] li:hover {
        background-color: #20272E !important;
        color: #00E5FF !important;
    }


    /* ========================================================
       SEARCH MESSAGES
       WHITE BOX — INTENTIONAL
       ======================================================== */

    [data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        border: 1px solid #D5D9DE !important;
        border-radius: 10px !important;
        opacity: 1 !important;
    }

    [data-testid="stTextInput"] input::placeholder {
        color: #7A818A !important;
        -webkit-text-fill-color: #7A818A !important;
        opacity: 1 !important;
    }

    [data-testid="stTextInput"] input:focus {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        border-color: #00E5FF !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        background-color: #11161A !important;
        color: #F5F7FA !important;
        border: 1px solid #293139 !important;
        border-radius: 10px !important;
    }

    .stButton > button:hover {
        background-color: #151C21 !important;
        color: #00EAF2 !important;
        border-color: #00EAF2 !important;
    }


    /* ========================================================
       DOWNLOAD / EXPORT BUTTON
       ======================================================== */

    .stDownloadButton > button {
        background-color: #11161A !important;
        color: #F5F7FA !important;
        border: 1px solid #293139 !important;
        border-radius: 10px !important;
    }

    .stDownloadButton > button:hover {
        background-color: #151C21 !important;
        color: #00EAF2 !important;
        border-color: #00EAF2 !important;
    }


    /* ========================================================
       CHAT MESSAGES
       ======================================================== */

    div[data-testid="stChatMessage"] {
        background-color: #101419 !important;
        color: #F5F7FA !important;
        border: 1px solid #20272E !important;
        border-radius: 14px !important;
        margin-bottom: 12px !important;
        padding: 0.4rem 0.8rem !important;
    }

    div[data-testid="stChatMessage"] p {
        color: #F5F7FA !important;
    }

    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        color: #F5F7FA !important;
    }


    /* ========================================================
       CHAT INPUT
       WHITE BOX — INTENTIONAL
       ======================================================== */

    [data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border: 2px solid #00E5FF !important;
        border-radius: 15px !important;
    }

    [data-testid="stChatInput"] > div {
        background-color: #FFFFFF !important;
    }

    [data-testid="stChatInput"] textarea {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        caret-color: #00B8CC !important;
        opacity: 1 !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        background-color: #FFFFFF !important;
        color: #666666 !important;
        -webkit-text-fill-color: #666666 !important;
        opacity: 1 !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
    }


    /* ========================================================
       CHAT INPUT BUTTONS
       ======================================================== */

    [data-testid="stChatInput"] button {
        background-color: #EEF1F5 !important;
        color: #111111 !important;
        border-radius: 10px !important;
    }

    [data-testid="stChatInput"] button:hover {
        background-color: #E1E7ED !important;
    }

    [data-testid="stChatInput"] button svg {
        color: #111111 !important;
        fill: #111111 !important;
    }


    /* ========================================================
       FILE UPLOADER
       ======================================================== */

    [data-testid="stFileUploader"] {
        background-color: #101419 !important;
        color: #F5F7FA !important;
    }

    [data-testid="stFileUploader"] section {
        background-color: #101419 !important;
        border-color: #303940 !important;
    }

    [data-testid="stFileUploader"] * {
        color: #F5F7FA !important;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border-color: #20262C !important;
    }


    /* ========================================================
       REX STATUS
       ======================================================== */

    .rex-status {
        color: #00F5FF !important;
        font-weight: 700;
        letter-spacing: 0.08em;
    }


    /* ========================================================
       FILE CHIP
       ======================================================== */

    .file-chip {
        display: inline-block;
        border: 1px solid #00E5FF;
        border-radius: 999px;
        padding: 4px 10px;
        margin: 3px;
        color: #00E5FF !important;
        background: #101419;
        font-size: 0.82rem;
    }


    /* ========================================================
       SCROLLBAR
       ======================================================== */

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #080A0D;
    }

    ::-webkit-scrollbar-thumb {
        background: #303940;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #00E5FF;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# MODEL DISCOVERY
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
        "embed",
        "rerank",
        "moderation",
        "content-safety",
        "whisper",
        "asr",
        "transcription",
        "tts",
        "audio",
        "speech",
    )

    return bool(model_id) and not any(
        word in model_id for word in blocked
    )


@st.cache_data(
    ttl=FREE_MODEL_CACHE_SECONDS,
    show_spinner=False,
)
def discover_free_models():

    import urllib.request

    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/models",
        headers={
            "Accept": "application/json",
            "User-Agent": "JHOSAI-REX-Model/2.0",
        },
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        payload = json.loads(
            response.read().decode("utf-8")
        )

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


# ============================================================
# FILE READING
# ============================================================

def extract_file_text(uploaded_file) -> str:
    """
    Read common text/document files so REX receives file contents.
    """

    name = uploaded_file.name.lower()
    raw = uploaded_file.getvalue()

    try:

        # ----------------------------------------------------
        # TXT / JSON / CSV
        # ----------------------------------------------------

        if name.endswith((".txt", ".json", ".csv")):

            return raw.decode(
                "utf-8",
                errors="ignore",
            )[:MAX_FILE_CHARS]


        # ----------------------------------------------------
        # PDF
        # ----------------------------------------------------

        if name.endswith(".pdf"):

            try:

                from pypdf import PdfReader

                reader = PdfReader(
                    io.BytesIO(raw)
                )

                pages = []

                for page in reader.pages:
                    pages.append(
                        page.extract_text() or ""
                    )

                return "\n".join(
                    pages
                )[:MAX_FILE_CHARS]

            except ImportError:

                return (
                    "[PDF attached. Install pypdf "
                    "to read its text: pip install pypdf]"
                )


        # ----------------------------------------------------
        # DOCX
        # ----------------------------------------------------

        if name.endswith(".docx"):

            try:

                from docx import Document

                doc = Document(
                    io.BytesIO(raw)
                )

                text = "\n".join(
                    p.text
                    for p in doc.paragraphs
                )

                return text[:MAX_FILE_CHARS]

            except ImportError:

                return (
                    "[DOCX attached. Install python-docx "
                    "to read its text: "
                    "pip install python-docx]"
                )


        # ----------------------------------------------------
        # IMAGES
        # ----------------------------------------------------

        if name.endswith(
            (".png", ".jpg", ".jpeg")
        ):

            return (
                "[Image attached. The file is available "
                "to REX, but image understanding depends "
                "on the selected OpenRouter model.]"
            )

    except Exception as exc:

        return (
            f"[Could not read "
            f"{uploaded_file.name}: {exc}]"
        )

    return f"[Attached file: {uploaded_file.name}]"


def build_file_context(files) -> str:

    if not files:
        return ""

    sections = []

    for uploaded_file in files:

        text = extract_file_text(
            uploaded_file
        )

        sections.append(
            f"\n===== FILE: "
            f"{uploaded_file.name} =====\n"
            f"{text}"
        )

    return "\n".join(sections)


# ============================================================
# OPENROUTER
# ============================================================

def generate_response(
    prompt: str,
    history=None,
    files=None,
    model=None,
) -> str:

    api_key = os.getenv(
        "OPENROUTER_API_KEY"
    )

    if not api_key:

        return (
            "OpenRouter is not configured. "
            "Set OPENROUTER_API_KEY in PowerShell "
            "and restart Streamlit."
        )


    # --------------------------------------------------------
    # OPENAI PACKAGE
    # --------------------------------------------------------

    try:

        from openai import OpenAI

    except ImportError:

        return (
            "The 'openai' package is missing. "
            "Run: pip install openai"
        )


    history = history or []
    files = files or []

    selected_model = (
        model
        or st.session_state.model
    )

    free_models = get_free_models()


    # --------------------------------------------------------
    # AUTOMATIC MODEL
    # --------------------------------------------------------

    if selected_model == AUTOMATIC_MODEL:

        selected_model = (
            free_models[0]
            if free_models
            else KNOWN_FREE_MODELS[0]
        )


    # --------------------------------------------------------
    # BUILD MESSAGES
    # --------------------------------------------------------

    messages = []

    for item in history:

        role = item.get("role")
        content = item.get("content", "")

        if role in (
            "user",
            "assistant",
        ) and content:

            messages.append(
                {
                    "role": role,
                    "content": content,
                }
            )


    # --------------------------------------------------------
    # FILE CONTEXT
    # --------------------------------------------------------

    file_context = build_file_context(
        files
    )

    final_prompt = prompt

    if file_context:

        final_prompt += (
            "\n\nUse the following uploaded "
            "file contents when relevant. "
            "If the file text is unavailable, "
            "say so clearly.\n"
            + file_context
        )


    messages.append(
        {
            "role": "user",
            "content": final_prompt,
        }
    )


    # --------------------------------------------------------
    # FALLBACK MODELS
    # --------------------------------------------------------

    fallback_models = [
        selected_model,
        *[
            m
            for m in free_models
            if m != selected_model
        ][:2],
    ]


    # --------------------------------------------------------
    # OPENROUTER REQUEST
    # --------------------------------------------------------

    try:

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer":
                    "http://localhost:8501",

                "X-Title":
                    "JHOSAI REX Model",
            },
        )

        response = (
            client.chat.completions.create(
                model=selected_model,
                messages=messages,
                max_tokens=1800,
                extra_body={
                    "models": fallback_models
                },
            )
        )


        # ----------------------------------------------------
        # RECORD MODEL USED
        # ----------------------------------------------------

        st.session_state.last_model_used = (
            getattr(
                response,
                "model",
                None,
            )
            or selected_model
        )


        # ----------------------------------------------------
        # RETURN RESPONSE
        # ----------------------------------------------------

        return (
            response
            .choices[0]
            .message
            .content
            or "REX did not return a response."
        )


    except Exception as exc:

        return (
            f"REX Model error: {exc}"
        )


# ============================================================
# SESSION / EXPORT
# ============================================================

def save_current_session():

    if not st.session_state.messages:
        return


    title = (
        st.session_state.messages[0]
        .get(
            "content",
            "Conversation",
        )
        .strip()
    )

    title = (
        title[:40]
        + ("..." if len(title) > 40 else "")
    )


    stamp = datetime.datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


    data = {
        "title": title,
        "messages": st.session_state.messages,
        "updated": datetime.datetime.now().isoformat(),
    }


    (
        SESSIONS_DIR
        / f"session_{stamp}.json"
    ).write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def export_text():

    lines = [
        "JHOSAI REX MODEL",
        "=" * 50,
        "",
    ]

    for message in st.session_state.messages:

        role = message.get(
            "role",
            "assistant",
        ).upper()

        lines.append(
            f"{role}:"
        )

        lines.append(
            message.get(
                "content",
                "",
            )
        )

        lines.append("")

    return "\n".join(lines)


# ============================================================
# REGENERATE
# ============================================================

def regenerate_last_response():

    if not st.session_state.messages:
        return


    if (
        st.session_state.messages[-1]
        .get("role")
        == "assistant"
    ):

        st.session_state.messages.pop()


    if not st.session_state.messages:
        return


    last_user = (
        st.session_state.messages[-1]
    )


    if (
        last_user.get("role")
        != "user"
    ):

        return


    prompt = last_user.get(
        "content",
        "",
    )

    history = (
        st.session_state.messages[:-1]
    )


    with st.spinner(
        "REX is thinking again..."
    ):

        response = generate_response(
            prompt,
            history=history,
            files=st.session_state.last_files,
            model=st.session_state.model,
        )


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": str(response),
        }
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # LOGO
    # --------------------------------------------------------

    if LOGO_PATH.exists():

        st.image(
            str(LOGO_PATH),
            width=210,
        )

    else:

        st.title(
            "JHOSAI REX"
        )

        st.caption(
            "MODEL BOT"
        )

        st.caption(
            "Logo file not found in project folder."
        )


    st.divider()


    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    if st.button(
        "＋  New chat",
        use_container_width=True,
    ):

        st.session_state.messages = []
        st.session_state.last_model_used = ""
        st.session_state.last_prompt = ""
        st.session_state.last_files = []

        st.rerun()


    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    st.caption("MODEL")

    free_models = get_free_models()

    model_options = [
        AUTOMATIC_MODEL,
        *free_models,
    ]


    current_model = (
        st.session_state.model
        if st.session_state.model
        in model_options
        else AUTOMATIC_MODEL
    )


    st.session_state.model = (
        st.selectbox(
            "Model",
            model_options,
            index=model_options.index(
                current_model
            ),
            label_visibility="collapsed",
        )
    )


    st.caption(
        f"{len(free_models)} free models available"
    )


    st.divider()


    # --------------------------------------------------------
    # CONVERSATION
    # --------------------------------------------------------

    st.caption(
        "CONVERSATION"
    )


    search_term = st.text_input(
        "Search",
        value=st.session_state.search_term,
        placeholder="Search messages...",
        label_visibility="collapsed",
    )


    st.session_state.search_term = (
        search_term
    )


    if st.session_state.messages:

        matching = []

        for message in (
            st.session_state.messages
        ):

            content = message.get(
                "content",
                "",
            )

            if (
                not search_term
                or search_term.lower()
                in content.lower()
            ):

                matching.append(
                    content
                )


        if matching:

            for text in matching[:5]:

                st.caption(
                    text[:45]
                )

        else:

            st.caption(
                "No matching messages."
            )

    else:

        st.caption(
            "No conversations yet."
        )


    st.divider()


    # --------------------------------------------------------
    # TOOLS
    # --------------------------------------------------------

    st.caption(
        "TOOLS"
    )


    if st.session_state.messages:

        st.download_button(
            "⬇  Export conversation",
            data=export_text(),
            file_name=(
                "jhosai_rex_conversation.txt"
            ),
            mime="text/plain",
            use_container_width=True,
        )


    if st.button(
        "🗑  Clear conversation",
        use_container_width=True,
    ):

        st.session_state.messages = []
        st.session_state.last_model_used = ""
        st.session_state.last_files = []

        st.rerun()


    st.divider()


    st.caption(
        "JHOSAI REX MODEL"
    )


# ============================================================
# TOP BAR
# ============================================================

top_left, top_right = st.columns(
    [7, 3]
)


with top_left:

    st.markdown(
        '### <span class="rex-status">● REX</span>',
        unsafe_allow_html=True,
    )

    st.caption(
        "JHOSAI REX Model"
    )


with top_right:

    st.caption(
        "ACTIVE MODEL"
    )

    st.write(
        st.session_state.last_model_used
        or st.session_state.model
    )


# ============================================================
# MAIN CHAT
# ============================================================

if not st.session_state.messages:

    if LOGO_PATH.exists():

        st.image(
            str(LOGO_PATH),
            width=300,
        )


    st.title(
        "What are we working on?"
    )


    st.caption(
        "JHOSAI REX Model is ready. "
        "Attach a file or ask REX anything."
    )


else:

    for message in (
        st.session_state.messages
    ):

        role = message.get(
            "role",
            "assistant",
        )

        content = message.get(
            "content",
            "",
        )


        with st.chat_message(
            "user"
            if role == "user"
            else "assistant"
        ):

            st.markdown(
                content
            )


# ============================================================
# CHAT ACTIONS
# ============================================================

if st.session_state.messages:

    last_role = (
        st.session_state.messages[-1]
        .get("role")
    )


    if last_role == "assistant":

        action1, action2 = st.columns(
            [1, 8]
        )


        with action1:

            if st.button(
                "🔄",
                help="Regenerate response",
            ):

                regenerate_last_response()

                st.rerun()


        with action2:

            st.caption(
                "REX used: "
                + (
                    st.session_state.last_model_used
                    or st.session_state.model
                )
            )


# ============================================================
# CHAT INPUT WITH FILE ATTACHMENT
# ============================================================

chat_value = st.chat_input(
    "Ask REX anything...",
    accept_file=True,
    file_type=[
        "pdf",
        "txt",
        "docx",
        "csv",
        "json",
        "png",
        "jpg",
        "jpeg",
    ],
)


if chat_value:

    # --------------------------------------------------------
    # STREAMLIT CHAT INPUT VALUE
    # --------------------------------------------------------

    if isinstance(
        chat_value,
        str,
    ):

        prompt = chat_value
        uploaded_files = []

    else:

        prompt = (
            getattr(
                chat_value,
                "text",
                "",
            )
            or ""
        )

        uploaded_files = list(
            getattr(
                chat_value,
                "files",
                [],
            )
            or []
        )


    # --------------------------------------------------------
    # PROMPT / FILE CHECK
    # --------------------------------------------------------

    if (
        prompt.strip()
        or uploaded_files
    ):

        history = list(
            st.session_state.messages
        )


        # ----------------------------------------------------
        # FILE ONLY MESSAGE
        # ----------------------------------------------------

        if (
            not prompt.strip()
            and uploaded_files
        ):

            prompt = (
                "Please analyze the attached "
                "file(s) and explain the "
                "important information clearly."
            )


        st.session_state.last_prompt = (
            prompt
        )

        st.session_state.last_files = (
            uploaded_files
        )


        # ----------------------------------------------------
        # ADD USER MESSAGE
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )


        # ----------------------------------------------------
        # GENERATE RESPONSE
        # ----------------------------------------------------

        with st.spinner(
            "REX is thinking..."
        ):

            response = generate_response(
                prompt,
                history=history,
                files=uploaded_files,
                model=st.session_state.model,
            )


        # ----------------------------------------------------
        # ADD ASSISTANT RESPONSE
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": str(response),
            }
        )


        # ----------------------------------------------------
        # SAVE SESSION
        # ----------------------------------------------------

        save_current_session()

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "JHOSAI REX Model · "
    "AI responses may require verification"
)