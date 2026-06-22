"""Language translation helper with API support and an offline demo fallback."""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Dict, Mapping, Optional, Tuple
from urllib import request
from urllib.error import URLError


class TranslationError(ValueError):
    """Raised when translation input is invalid or an API call fails."""


@dataclass(frozen=True)
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    provider: str


LANGUAGE_ALIASES: Mapping[str, str] = {
    "en": "en",
    "eng": "en",
    "english": "en",
    "hi": "hi",
    "hindi": "hi",
    "te": "te",
    "telugu": "te",
    "es": "es",
    "spanish": "es",
    "fr": "fr",
    "french": "fr",
    "de": "de",
    "german": "de",
}

PHRASEBOOK: Mapping[Tuple[str, str], Mapping[str, str]] = {
    ("en", "hi"): {
        "hello": "Namaste",
        "hello, how are you?": "Namaste, aap kaise hain?",
        "thank you": "Dhanyavaad",
        "good morning": "Suprabhat",
        "artificial intelligence": "Kritrim buddhimatta",
    },
    ("en", "te"): {
        "hello": "Namaskaram",
        "hello, how are you?": "Namaskaram, meeru ela unnaru?",
        "thank you": "Dhanyavadalu",
        "good morning": "Subhodayam",
        "artificial intelligence": "Krutrima medhassu",
    },
    ("en", "es"): {
        "hello": "Hola",
        "hello, how are you?": "Hola, como estas?",
        "thank you": "Gracias",
        "good morning": "Buenos dias",
        "artificial intelligence": "Inteligencia artificial",
    },
    ("en", "fr"): {
        "hello": "Bonjour",
        "hello, how are you?": "Bonjour, comment ca va?",
        "thank you": "Merci",
        "good morning": "Bonjour",
        "artificial intelligence": "Intelligence artificielle",
    },
    ("en", "de"): {
        "hello": "Hallo",
        "hello, how are you?": "Hallo, wie geht es dir?",
        "thank you": "Danke",
        "good morning": "Guten Morgen",
        "artificial intelligence": "Kunstliche Intelligenz",
    },
}


def normalize_language(language: str) -> str:
    key = language.strip().lower()
    if key not in LANGUAGE_ALIASES:
        supported = ", ".join(sorted(set(LANGUAGE_ALIASES.values())))
        raise TranslationError(f"Unsupported language '{language}'. Supported codes: {supported}")
    return LANGUAGE_ALIASES[key]


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip()).lower()


def translate_text(
    text: str,
    source_language: str,
    target_language: str,
    *,
    api_url: Optional[str] = None,
    api_key: Optional[str] = None,
    allow_offline_fallback: bool = True,
) -> TranslationResult:
    """Translate text using a LibreTranslate-style API or a small offline phrasebook.

    The offline phrasebook is intentionally transparent: when a phrase is unknown,
    it returns a clear message instead of pretending to translate arbitrary text.
    """

    original = text.strip()
    if not original:
        raise TranslationError("Text to translate cannot be empty.")

    source = normalize_language(source_language)
    target = normalize_language(target_language)
    if source == target:
        return TranslationResult(original, original, source, target, "identity")

    if api_url:
        try:
            translated = _translate_with_api(original, source, target, api_url, api_key)
            return TranslationResult(original, translated, source, target, "translation_api")
        except TranslationError:
            if not allow_offline_fallback:
                raise

    translated = _translate_with_phrasebook(original, source, target)
    return TranslationResult(original, translated, source, target, "offline_phrasebook")


def _translate_with_api(
    text: str,
    source: str,
    target: str,
    api_url: str,
    api_key: Optional[str],
) -> str:
    payload: Dict[str, str] = {
        "q": text,
        "source": source,
        "target": target,
        "format": "text",
    }
    if api_key:
        payload["api_key"] = api_key

    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        api_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (OSError, URLError, json.JSONDecodeError) as exc:
        raise TranslationError(f"Translation API request failed: {exc}") from exc

    translated = data.get("translatedText") or data.get("translation")
    if not translated:
        raise TranslationError("Translation API response did not include translated text.")
    return str(translated)


def _translate_with_phrasebook(text: str, source: str, target: str) -> str:
    phrase_map = PHRASEBOOK.get((source, target), {})
    phrase = normalize_text(text)
    if phrase in phrase_map:
        return phrase_map[phrase]

    return (
        f"No offline translation is available for '{text}'. "
        "Add an API URL/key in the app for full translation coverage."
    )
