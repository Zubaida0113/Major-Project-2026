# Voice-Based AI Triage System for MCMS-RWA

This is a Streamlit web app for the MCMS-RWA complaint management system. It transcribes voice complaints, computes trust and priority scores, and triages them.

## Setup

1. Ensure you have Python 3.8+ installed.
2. Install dependencies: `pip install -r requirements.txt`
3. Place audio files and `RWA_RuleBook.xlsx` in an `audio_files/` folder.

## Run

`streamlit run app.py`

Open the URL in your browser, upload an audio file, and get results.

## Files

- `app.py`: Main Streamlit app
- `triage_model.py`: Core logic
- `requirements.txt`: Dependencies
- `audio_files/`: Audio and Excel files