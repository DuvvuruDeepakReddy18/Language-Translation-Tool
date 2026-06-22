from pathlib import Path

from codealpha_ai.translation import translate_text


def main() -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    result = translate_text("Hello, how are you?", "English", "Hindi")
    output_path = output_dir / "translation_demo.txt"
    output_path.write_text(
        f"Input: {result.original_text}\nOutput: {result.translated_text}\n",
        encoding="utf-8",
    )
    print(f"Translation written to {output_path}")


if __name__ == "__main__":
    main()
