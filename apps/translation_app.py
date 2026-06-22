from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st

from codealpha_ai.translation import TranslationError, translate_text


LANGUAGES = ["English", "Hindi", "Telugu", "Spanish", "French", "German"]


st.set_page_config(page_title="CodeAlpha Translation Tool", page_icon="AI", layout="centered")
st.title("Language Translation Tool")

text = st.text_area("Enter text", value="Hello, how are you?", height=140)
source = st.selectbox("Source language", LANGUAGES, index=0)
target = st.selectbox("Target language", LANGUAGES, index=1)
api_url = st.text_input("Optional translation API URL", placeholder="https://libretranslate.com/translate")
api_key = st.text_input("Optional API key", type="password")

if st.button("Translate", type="primary"):
    try:
        result = translate_text(
            text,
            source,
            target,
            api_url=api_url or None,
            api_key=api_key or None,
        )
        st.text_area("Translated text", value=result.translated_text, height=140)
        st.caption(f"Provider: {result.provider} | {result.source_language} -> {result.target_language}")
    except TranslationError as exc:
        st.error(str(exc))
