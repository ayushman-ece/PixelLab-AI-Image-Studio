
import os
from io import BytesIO

import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from dotenv import load_dotenv
from google import genai
from google.genai import types
from groq import Groq


# ==========================================================
# PIXELLAB | PROFESSIONAL AI IMAGE STUDIO
# ==========================================================

load_dotenv()

st.set_page_config(
    page_title="PixelLab | Creative Studio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# PRIVATE API CONFIGURATION
# ==========================================================

def get_secret(name):
    """Read keys privately from Streamlit Secrets or local .env."""
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""

    return value or os.getenv(name, "")


GEMINI_API_KEY = get_secret("GEMINI_API_KEY")
GROQ_API_KEY = get_secret("GROQ_API_KEY")

GEMINI_ANALYSIS_MODEL = "gemini-2.5-flash"
GEMINI_IMAGE_MODEL = "gemini-3.1-flash-image"
GROQ_MODEL = "openai/gpt-oss-20b"


# ==========================================================
# SESSION STATE
# ==========================================================

DEFAULTS = {
    "original": None,
    "upload_id": None,
    "ai_result": None,
    "ai_explanation": "",
    "analysis": "",
    "chat_history": [],
    "edit_prompt": "",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================================
# PROFESSIONAL UI DESIGN
# ==========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #090c14;
    --panel: #121827;
    --panel2: #192235;
    --border: #29344a;
    --accent: #9382ff;
    --cyan: #50d9e7;
    --muted: #98a5bc;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 80% 0%, #25204a 0%, transparent 35%),
        radial-gradient(ellipse at 0% 65%, #102b38 0%, transparent 32%),
        var(--bg);
    color: #f5f6fc;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #0d1220;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #f5f6fc !important;
    letter-spacing: -0.5px;
}

.brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -1.5px;
    background: linear-gradient(100deg, #a99aff, #50d9e7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero {
    padding: 34px;
    border-radius: 22px;
    border: 1px solid #35405c;
    background: linear-gradient(115deg, #1b1e3b, #12303d);
    margin-bottom: 25px;
}

.eyebrow {
    color: #a99aff;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(28px, 4vw, 43px);
    font-weight: 800;
    line-height: 1.2;
    margin-top: 9px;
}

.hero-description {
    color: #bac5d9;
    font-size: 14px;
    margin-top: 12px;
}

.panel {
    background: #131b2a;
    border: 1px solid var(--border);
    padding: 20px;
    border-radius: 16px;
}

.feature-card {
    background: linear-gradient(145deg, #172034, #101725);
    border: 1px solid #2b3850;
    padding: 19px;
    border-radius: 15px;
    min-height: 135px;
}

.feature-icon {
    font-size: 25px;
    margin-bottom: 12px;
}

.feature-name {
    font-weight: 700;
    font-size: 14px;
}

.feature-description {
    color: var(--muted);
    font-size: 12px;
    margin-top: 7px;
}

.muted {
    color: var(--muted);
    font-size: 13px;
}

div[data-testid="stMetric"] {
    background: #151e2e;
    border: 1px solid #2b3850;
    padding: 15px;
    border-radius: 13px;
}

div[data-testid="stMetricValue"] {
    color: #aa9bff;
}

div.stButton > button,
div.stDownloadButton > button {
    border-radius: 10px;
    min-height: 43px;
    font-weight: 700;
}

div.stDownloadButton > button {
    background: linear-gradient(100deg, #7969eb, #318ca9);
    color: white;
    border: none;
}

div.stButton > button:hover {
    border-color: #a99aff;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: #111827;
    padding: 8px;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 9px;
    font-weight: 700;
}

div[data-testid="stFileUploader"] {
    background: #131b2a;
    border: 1px dashed #647197;
    border-radius: 15px;
    padding: 12px;
}

hr {
    border-color: #29344a;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ==========================================================
# IMAGE PROCESSING FUNCTIONS
# ==========================================================

def image_to_bytes(image, fmt="PNG"):
    buffer = BytesIO()

    if fmt == "JPEG":
        image = image.convert("RGB")

    image.save(buffer, format=fmt)
    return buffer.getvalue()


def resize_image(image, max_size=1400):
    result = image.copy()
    result.thumbnail((max_size, max_size))
    return result


def process_image(image, operation, settings):
    result = image.copy()

    if operation == "Original":
        pass

    elif operation == "Grayscale":
        result = ImageOps.grayscale(result).convert("RGB")

    elif operation == "Black & White":
        gray = ImageOps.grayscale(result)
        result = gray.point(
            lambda p: 255 if p > settings["threshold"] else 0
        ).convert("RGB")

    elif operation == "Brightness":
        result = ImageEnhance.Brightness(result).enhance(
            settings["brightness"]
        )

    elif operation == "Contrast":
        result = ImageEnhance.Contrast(result).enhance(
            settings["contrast"]
        )

    elif operation == "Saturation":
        result = ImageEnhance.Color(result).enhance(
            settings["saturation"]
        )

    elif operation == "Blur":
        result = result.filter(
            ImageFilter.GaussianBlur(settings["blur"])
        )

    elif operation == "Sharpen":
        result = ImageEnhance.Sharpness(result).enhance(
            settings["sharpness"]
        )

    elif operation == "Edge Detection":
        result = result.filter(ImageFilter.FIND_EDGES)

    elif operation == "Vintage":
        result = ImageOps.grayscale(result).convert("RGB")
        result = ImageEnhance.Color(result).enhance(0.5)
        result = ImageEnhance.Contrast(result).enhance(1.25)

    elif operation == "Rotate":
        result = result.rotate(
            settings["angle"],
            expand=True
        )

    elif operation == "Flip Horizontal":
        result = ImageOps.mirror(result)

    elif operation == "Flip Vertical":
        result = ImageOps.flip(result)

    elif operation == "Sepia":
        gray = ImageOps.grayscale(result)
        result = ImageOps.colorize(
            gray,
            black="#302019",
            white="#f2d7a0"
        ).convert("RGB")

    return result


# ==========================================================
# GEMINI FUNCTIONS
# ==========================================================

def analyze_image(image, question):
    if not GEMINI_API_KEY:
        raise ValueError(
            "Gemini is not configured on the server."
        )

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model=GEMINI_ANALYSIS_MODEL,
        contents=[
            question,
            resize_image(image)
        ]
    )

    return response.text or "No analysis was returned."


def edit_image_with_gemini(image, prompt):
    if not GEMINI_API_KEY:
        raise ValueError(
            "Gemini is not configured on the server."
        )

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model=GEMINI_IMAGE_MODEL,
        contents=[
            prompt,
            resize_image(image)
        ],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"]
        )
    )

    output_image = None
    explanation = ""

    for part in response.parts:
        if part.text:
            explanation += part.text + "\n"

        if part.inline_data is not None:
            output_image = part.as_image()

    if output_image is None:
        raise ValueError(
            "The image model returned no image. "
            "Try a different prompt or check model access."
        )

    return output_image, explanation


# ==========================================================
# GROQ AI ASSISTANT
# ==========================================================

def ask_groq(question, image_info, history):
    if not GROQ_API_KEY:
        raise ValueError(
            "The AI assistant is not configured on the server."
        )

    client = Groq(api_key=GROQ_API_KEY)

    messages = [
        {
            "role": "system",
            "content": """
You are PixelLab AI, a professional image editing assistant.

Help users with:
- Photography and image composition
- Image enhancement
- Image filters and processing
- Lighting and color correction
- Editing recommendations

Be concise, helpful and practical.

When the user wants an AI image edit, write a clear
prompt that can be used by an image generation model.

Do not claim that you personally edited an image.
"""
        },
        {
            "role": "user",
            "content": "Current image information: " + image_info
        }
    ]

    # Keep a limited amount of conversation history.
    for item in history[-8:]:
        messages.append(item)

    messages.append({
        "role": "user",
        "content": question
    })

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.5,
        max_completion_tokens=1000
    )

    return response.choices[0].message.content


# ==========================================================
# ERROR HANDLING
# ==========================================================

def show_api_error(error, service):
    message = str(error)
    lower = message.lower()

    if "429" in lower or "resource_exhausted" in lower:
        st.error(
            f"{service} usage limit reached. "
            "Check your API quota, billing and model availability. "
            "Wait for the quota reset or use an eligible plan."
        )

    elif "401" in lower or "403" in lower or "api key" in lower:
        st.error(
            f"{service} authentication failed. "
            "Check the server-side API key configuration."
        )

    elif "404" in lower or "not found" in lower:
        st.error(
            f"{service} model or endpoint is unavailable. "
            "Check the configured model name and API access."
        )

    else:
        st.error(
            f"{service} request failed. "
            "Please try again. Technical detail: "
            + message[:350]
        )


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">✦ PixelLab</div>',
        unsafe_allow_html=True
    )

    st.caption("AI IMAGE PROCESSING STUDIO")

    st.divider()

    st.markdown("### 🎨 Editing Studio")

    operation = st.selectbox(
        "Choose an image operation",
        [
            "Original",
            "Grayscale",
            "Black & White",
            "Brightness",
            "Contrast",
            "Saturation",
            "Blur",
            "Sharpen",
            "Edge Detection",
            "Vintage",
            "Sepia",
            "Rotate",
            "Flip Horizontal",
            "Flip Vertical"
        ]
    )

    settings = {}

    if operation == "Black & White":
        settings["threshold"] = st.slider(
            "Threshold", 0, 255, 128
        )

    elif operation == "Brightness":
        settings["brightness"] = st.slider(
            "Brightness", 0.1, 3.0, 1.0, 0.1
        )

    elif operation == "Contrast":
        settings["contrast"] = st.slider(
            "Contrast", 0.1, 3.0, 1.0, 0.1
        )

    elif operation == "Saturation":
        settings["saturation"] = st.slider(
            "Saturation", 0.0, 3.0, 1.0, 0.1
        )

    elif operation == "Blur":
        settings["blur"] = st.slider(
            "Blur strength", 1, 25, 5
        )

    elif operation == "Sharpen":
        settings["sharpness"] = st.slider(
            "Sharpness", 0.1, 4.0, 2.0, 0.1
        )

    elif operation == "Rotate":
        settings["angle"] = st.slider(
            "Rotation angle", 0, 360, 90
        )

    st.divider()

    st.markdown("### ✦ Studio Information")

    st.caption("Local image processing is available without AI keys.")

    st.caption("AI tools use private server-side configuration.")

    st.caption("PIXELLAB • VERSION 2.0")


# ==========================================================
# HEADER
# ==========================================================

st.markdown("""
<div class="hero">
    <div class="eyebrow">CREATIVE WORKSPACE / IMAGE INTELLIGENCE</div>
    <div class="hero-title">Create. Enhance. Transform.</div>
    <div class="hero-description">
        A creative image processing workspace with intelligent
        image analysis and AI-assisted editing.
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# UPLOAD
# ==========================================================

uploaded = st.file_uploader(
    "Upload your image",
    type=["png", "jpg", "jpeg", "webp"],
    help="Supported formats: PNG, JPG, JPEG and WebP."
)

if uploaded is not None:

    try:
        raw_data = uploaded.getvalue()

        if st.session_state.upload_id != raw_data:

            image = Image.open(
                BytesIO(raw_data)
            ).convert("RGB")

            st.session_state.original = image
            st.session_state.upload_id = raw_data
            st.session_state.ai_result = None
            st.session_state.ai_explanation = ""
            st.session_state.analysis = ""
            st.session_state.chat_history = []

    except Exception:
        st.error("Unable to open this image. Please upload a valid image.")
        st.stop()


# ==========================================================
# WORKSPACE
# ==========================================================

if st.session_state.original is not None:

    original = st.session_state.original

    processed = process_image(
        original,
        operation,
        settings
    )

    st.markdown("## Your Workspace")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Width", f"{original.width} px")
    m2.metric("Height", f"{original.height} px")
    m3.metric("File size", f"{len(uploaded.getvalue()) / 1024:.1f} KB")
    m4.metric("Active tool", operation)

    st.divider()

    st.markdown("## Image Preview")

    preview_tab, result_tab = st.tabs([
        "✦ Original vs Edited",
        "✧ AI Result"
    ])

    with preview_tab:

        left, right = st.columns(2, gap="large")

        with left:
            st.markdown("**ORIGINAL**")
            st.image(
                original,
                use_container_width=True
            )

        with right:
            st.markdown("**PROCESSED**")
            st.image(
                processed,
                use_container_width=True
            )

    with result_tab:

        if st.session_state.ai_result is not None:

            st.image(
                st.session_state.ai_result,
                use_container_width=True
            )

            if st.session_state.ai_explanation:
                st.markdown(st.session_state.ai_explanation)

            st.download_button(
                "⬇ Download AI Result",
                data=image_to_bytes(
                    st.session_state.ai_result
                ),
                file_name="pixellab_ai_result.png",
                mime="image/png",
                use_container_width=True
            )

        else:
            st.info(
                "Your AI edited image will appear here "
                "after a successful generation."
            )

    # ======================================================
    # EXPORT
    # ======================================================

    st.divider()

    st.markdown("## Export Your Image")

    export_col1, export_col2 = st.columns([2, 1])

    with export_col1:
        export_format = st.selectbox(
            "File format",
            ["PNG", "JPEG"],
            key="export_format"
        )

    with export_col2:

        if export_format == "PNG":
            export_data = image_to_bytes(processed, "PNG")
            mime_type = "image/png"
            file_name = "pixellab_edited.png"

        else:
            export_data = image_to_bytes(processed, "JPEG")
            mime_type = "image/jpeg"
            file_name = "pixellab_edited.jpg"

        st.write("")
        st.download_button(
            "⬇ Download Image",
            data=export_data,
            file_name=file_name,
            mime=mime_type,
            use_container_width=True
        )

    # ======================================================
    # AI CREATIVE WORKSPACE
    # ======================================================

    st.divider()

    st.markdown("## ✨ AI Creative Workspace")

    ai_edit_tab, analysis_tab, assistant_tab = st.tabs([
        "✦ AI Image Editor",
        "◈ Image Intelligence",
        "✧ AI Assistant"
    ])

    # ======================================================
    # GEMINI IMAGE EDITOR
    # ======================================================

    with ai_edit_tab:

        st.markdown("### Transform your image")

        st.caption(
            "Describe the changes you want. Gemini will "
            "attempt to generate an edited version."
        )

        prompt_options = [
            "Give it a cinematic look",
            "Improve the lighting professionally",
            "Change the background to a beach",
            "Make it look like a studio photograph"
        ]

        selected_prompt = st.selectbox(
            "Quick editing ideas",
            ["Choose a suggestion..."] + prompt_options
        )

        if selected_prompt != "Choose a suggestion...":
            if st.button("Use this suggestion"):
                st.session_state.edit_prompt = selected_prompt
                st.rerun()

        edit_prompt = st.text_area(
            "Describe your edit",
            key="edit_prompt",
            height=120,
            placeholder=(
                "Example: Place a mountain background behind "
                "the subject, improve lighting and preserve "
                "the person's original appearance."
            )
        )

        if st.button(
            "✦ Generate AI Edit",
            type="primary",
            use_container_width=True
        ):

            if not GEMINI_API_KEY:
                st.error(
                    "AI image editing is not configured by the administrator."
                )

            elif not edit_prompt.strip():
                st.warning("Please enter an editing prompt.")

            else:

                try:
                    with st.spinner(
                        "Gemini is working on your image..."
                    ):

                        result, explanation = edit_image_with_gemini(
                            original,
                            edit_prompt.strip()
                        )

                    st.session_state.ai_result = result
                    st.session_state.ai_explanation = explanation

                    st.success("Your AI edit is ready!")
                    st.rerun()

                except Exception as error:
                    show_api_error(error, "Gemini image editing")

    # ======================================================
    # GEMINI IMAGE ANALYSIS
    # ======================================================

    with analysis_tab:

        st.markdown("### Understand your image")

        analysis_question = st.selectbox(
            "Choose an analysis",
            [
                "Describe this image in detail.",
                "Analyze its lighting and image quality.",
                "Identify the main objects and background.",
                "Suggest improvements to make it professional.",
                "Analyze colors and composition."
            ]
        )

        if st.button(
            "◈ Analyze Image",
            use_container_width=True
        ):

            if not GEMINI_API_KEY:
                st.error("Image analysis is not configured.")

            else:

                try:
                    with st.spinner("Analyzing your image..."):

                        answer = analyze_image(
                            original,
                            analysis_question
                        )

                    st.session_state.analysis = answer

                except Exception as error:
                    show_api_error(error, "Gemini analysis")

        if st.session_state.analysis:

            st.markdown("### Analysis Report")

            st.markdown(
                '<div class="panel">'
                + st.session_state.analysis
                + '</div>',
                unsafe_allow_html=True
            )

    # ======================================================
    # GROQ ASSISTANT
    # ======================================================

    with assistant_tab:

        st.markdown("### Meet PixelLab AI")

        st.caption(
            "Get photography tips, editing instructions "
            "and image enhancement suggestions."
        )

        for message in st.session_state.chat_history:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_question = st.chat_input(
            "Ask PixelLab AI..."
        )

        if user_question:

            if not GROQ_API_KEY:
                st.error("The AI assistant is not configured.")

            else:

                history = st.session_state.chat_history.copy()

                st.session_state.chat_history.append({
                    "role": "user",
                    "content": user_question
                })

                with st.chat_message("user"):
                    st.markdown(user_question)

                try:

                    image_info = (
                        f"Image dimensions: {original.width} x "
                        f"{original.height}. "
                        f"Selected editing tool: {operation}."
                    )

                    with st.chat_message("assistant"):

                        with st.spinner("PixelLab AI is thinking..."):

                            answer = ask_groq(
                                user_question,
                                image_info,
                                history
                            )

                        st.markdown(answer)

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as error:

                    st.session_state.chat_history.pop()

                    show_api_error(error, "Groq assistant")

    # ======================================================
    # RESET
    # ======================================================

    st.divider()

    if st.button(
        "↺ Reset Workspace",
        use_container_width=True
    ):

        for key, value in DEFAULTS.items():
            st.session_state[key] = value

        st.rerun()


# ==========================================================
# EMPTY STATE
# ==========================================================

else:

    st.markdown("""
    <div class="panel" style="text-align:center;padding:55px 20px;">
        <div style="font-size:55px;">✦</div>
        <h2>Welcome to your creative studio</h2>
        <p style="color:#98a5bc;">
            Upload an image above to unlock your editing workspace.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Explore your tools")

    cards = [
        ("🎨", "Image Editing",
         "Brightness, contrast, filters and transformations."),

        ("✦", "Gemini AI",
         "AI image editing and intelligent image analysis."),

        ("◈", "Image Intelligence",
         "Understand image quality, colors and composition."),

        ("⚡", "Groq Assistant",
         "Get fast image editing recommendations.")
    ]

    columns = st.columns(4)

    for column, card in zip(columns, cards):

        with column:

            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{card[0]}</div>
                <div class="feature-name">{card[1]}</div>
                <div class="feature-description">{card[2]}</div>
            </div>
            """, unsafe_allow_html=True)


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown("""
<div style="text-align:center;padding:20px;">
    <div class="brand" style="font-size:25px;">✦ PixelLab</div>
    <p style="color:#98a5bc;font-size:12px;">
        Professional AI Image Processing Studio
    </p>
    <p style="color:#69768f;font-size:11px;">
        Create. Enhance. Transform.
    </p>
</div>
""", unsafe_allow_html=True)
