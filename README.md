# Language Translation Tool

Standalone language translation project with a Streamlit interface.

## Features

- Text input with source and target language selection
- LibreTranslate-style API support through optional URL/key fields
- Offline phrasebook fallback for demo and testing
- Streamlit user interface
- Unit tests for translation behavior and validation

## Run Tests

```powershell
python -m unittest discover -s tests -v
```

## Run Demo

```powershell
python run_demo.py
```

Demo output is written to `outputs/translation_demo.txt`.

## Run UI

```powershell
python -m pip install -r requirements.txt
streamlit run apps/translation_app.py
```

## Files

- `language_translation/translation.py` - translation logic
- `apps/translation_app.py` - Streamlit interface
- `tests/test_translation.py` - automated tests
