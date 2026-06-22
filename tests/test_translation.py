import unittest

from language_translation.translation import TranslationError, translate_text


class TranslationTests(unittest.TestCase):
    def test_translates_known_phrase_with_offline_phrasebook(self):
        result = translate_text("Hello, how are you?", "English", "Hindi")

        self.assertEqual(result.translated_text, "Namaste, aap kaise hain?")
        self.assertEqual(result.provider, "offline_phrasebook")
        self.assertEqual(result.source_language, "en")
        self.assertEqual(result.target_language, "hi")

    def test_rejects_empty_input(self):
        with self.assertRaises(TranslationError):
            translate_text("   ", "English", "Spanish")

    def test_reports_missing_phrase_without_fake_translation(self):
        result = translate_text("This exact sentence is not in the demo dictionary.", "English", "Telugu")

        self.assertIn("No offline translation", result.translated_text)
        self.assertEqual(result.provider, "offline_phrasebook")


if __name__ == "__main__":
    unittest.main()
