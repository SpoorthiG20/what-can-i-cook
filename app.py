import streamlit as st
import smtplib
from email.message import EmailMessage

from google import genai
from google.genai import types

from prompts import (
    SYSTEM_PROMPT,
    WELCOME_MESSAGE_TEMPLATE,
    SUMMARY_REQUEST_PROMPT,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="What Can I Cook?",
    page_icon="🍳",
    layout="centered",
)


# =========================================================
# CONFIGURATION
# =========================================================

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

GMAIL_SENDER_EMAIL = st.secrets["GMAIL_SENDER_EMAIL"]
GMAIL_APP_PASSWORD = st.secrets["GMAIL_APP_PASSWORD"].replace(
    " ",
    "",
)

MODEL_NAME = "gemini-3.5-flash"


# =========================================================
# SESSION STATE
# =========================================================

if "onboarded" not in st.session_state:
    st.session_state.onboarded = False

if "name" not in st.session_state:
    st.session_state.name = ""

if "email_address" not in st.session_state:
    st.session_state.email_address = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "last_recipe" not in st.session_state:
    st.session_state.last_recipe = ""


# =========================================================
# GEMINI FUNCTION
# =========================================================

def ask_gemini(message_parts):
    """
    Send a request to Gemini using a fresh client.

    We intentionally do NOT keep a Gemini Client or Chat
    object in Streamlit session state. This prevents the
    'client has been closed' error.
    """

    client = None

    try:

        # Create a completely fresh client
        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        # Build the conversation for Gemini
        contents = []

        for item in st.session_state.conversation:

            contents.append(
                types.Content(
                    role=item["role"],
                    parts=[
                        types.Part.from_text(
                            text=item["text"]
                        )
                    ],
                )
            )

        # Add the current request
        current_parts = []

        for part in message_parts:

            if isinstance(part, types.Part):
                current_parts.append(part)

            else:
                current_parts.append(
                    types.Part.from_text(
                        text=str(part)
                    )
                )

        contents.append(
            types.Content(
                role="user",
                parts=current_parts,
            )
        )

        # Send request
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            ),
        )

        answer = response.text

        # Save conversation for future questions
        user_text_for_history = []

        for part in message_parts:

            if isinstance(part, types.Part):
                continue

            user_text_for_history.append(
                str(part)
            )

        history_text = " ".join(
            user_text_for_history
        ).strip()

        if not history_text:
            history_text = (
                "User uploaded an ingredient photo."
            )

        st.session_state.conversation.append(
            {
                "role": "user",
                "text": history_text,
            }
        )

        st.session_state.conversation.append(
            {
                "role": "model",
                "text": answer,
            }
        )

        return answer

    except Exception as error:

        return f"Gemini error: {error}"

    finally:

        # Close only this request's client.
        # Nothing closed is stored in session state.
        if client is not None:

            try:
                client.close()
            except Exception:
                pass


# =========================================================
# EMAIL FUNCTION
# =========================================================

def send_email(
    to_email,
    user_name,
    recipe,
):

    try:

        message = EmailMessage()

        message["Subject"] = (
            "🍳 Your What Can I Cook? Recipe"
        )

        message["From"] = GMAIL_SENDER_EMAIL

        message["To"] = to_email

        message.set_content(
            f"Hi {user_name}!\n\n"
            "Here's your What Can I Cook? recipe:\n\n"
            f"{recipe}\n\n"
            "Enjoy your meal! 👩‍🍳\n\n"
            "— What Can I Cook?"
        )

        with smtplib.SMTP(
            "smtp.gmail.com",
            587,
        ) as server:

            server.starttls()

            server.login(
                GMAIL_SENDER_EMAIL,
                GMAIL_APP_PASSWORD,
            )

            server.send_message(message)

        return True, None

    except Exception as error:

        return False, str(error)


# =========================================================
# ONBOARDING
# =========================================================

if not st.session_state.onboarded:

    st.title("🍳 What Can I Cook?")

    st.subheader(
        "Your AI Recipe Assistant"
    )

    st.write(
        "Have some ingredients but don't know "
        "what to make? Upload a photo or tell "
        "me what you have, and I'll help you "
        "turn them into a practical recipe."
    )

    st.divider()

    name = st.text_input(
        "What's your name?",
        placeholder="Enter your name",
    )

    email_address = st.text_input(
        "Where should I send your recipe?",
        placeholder="you@example.com",
    )

    if st.button(
        "Let's cook 🚀",
        use_container_width=True,
        type="primary",
    ):

        if not name.strip():

            st.warning(
                "Please enter your name."
            )

        elif not email_address.strip():

            st.warning(
                "Please enter your email address."
            )

        else:

            st.session_state.name = (
                name.strip()
            )

            st.session_state.email_address = (
                email_address.strip()
            )

            st.session_state.onboarded = True

            welcome_message = (
                WELCOME_MESSAGE_TEMPLATE.format(
                    name=st.session_state.name
                )
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": welcome_message,
                }
            )

            st.rerun()

    st.stop()


# =========================================================
# MAIN APP
# =========================================================

st.title("🍳 What Can I Cook?")

st.caption(
    f"Logged in as {st.session_state.name} • "
    f"Recipes go to "
    f"{st.session_state.email_address}"
)


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# INGREDIENT PHOTO
# =========================================================

uploaded_image = st.file_uploader(
    "📸 Upload a photo of your ingredients",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp",
    ],
)


if uploaded_image is not None:

    st.image(
        uploaded_image,
        caption="Your ingredients",
        use_container_width=True,
    )


# =========================================================
# TEXT INPUT
# =========================================================

user_text = st.chat_input(
    "Tell me what ingredients you have..."
)


# =========================================================
# PROCESS USER MESSAGE
# =========================================================

if user_text or uploaded_image:

    parts = []

    # -----------------------------------------------------
    # IMAGE
    # -----------------------------------------------------

    if uploaded_image:

        image_bytes = (
            uploaded_image.getvalue()
        )

        parts.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=uploaded_image.type,
            )
        )

        parts.append(
            "Analyze the ingredients visible "
            "in this image and suggest a practical "
            "recipe I can make with them."
        )

    # -----------------------------------------------------
    # TEXT
    # -----------------------------------------------------

    if user_text:

        parts.append(user_text)

    # -----------------------------------------------------
    # DISPLAY USER MESSAGE
    # -----------------------------------------------------

    if user_text:

        display_text = user_text

    else:

        display_text = (
            "📸 Uploaded an ingredient photo"
        )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": display_text,
        }
    )

    with st.chat_message("user"):

        st.markdown(display_text)

    # -----------------------------------------------------
    # GEMINI RESPONSE
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking of something delicious... 🍳"
        ):

            recipe = ask_gemini(parts)

        st.markdown(recipe)

    # -----------------------------------------------------
    # SAVE RESPONSE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": recipe,
        }
    )

    st.session_state.last_recipe = recipe


# =========================================================
# EMAIL SECTION
# =========================================================

st.divider()

st.subheader(
    "📧 Like this recipe?"
)

st.write(
    "Send the current recipe to your email "
    "so you can keep it for later."
)


if st.button(
    "📧 Send Recipe",
    use_container_width=True,
):

    if not st.session_state.last_recipe:

        st.warning(
            "Please generate a recipe first."
        )

    else:

        # ---------------------------------------------
        # Use the recipe already generated.
        #
        # We intentionally don't call Gemini again
        # here. This keeps the email feature simple
        # and avoids another Gemini connection.
        # ---------------------------------------------

        email_recipe = (
            st.session_state.last_recipe
        )

        # ---------------------------------------------
        # SEND EMAIL
        # ---------------------------------------------

        with st.spinner(
            "Sending your recipe... 📧"
        ):

            success, error = send_email(
                st.session_state.email_address,
                st.session_state.name,
                email_recipe,
            )

        if success:

            st.success(
                "Recipe sent successfully! 📧"
            )

        else:

            st.error(
                f"Couldn't send the email: {error}"
            )


# =========================================================
# RESET
# =========================================================

st.divider()

if st.button(
    "🔄 Start a new session",
    use_container_width=True,
):

    st.session_state.clear()

    st.rerun()
