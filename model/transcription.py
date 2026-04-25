# model/transcription.py

import whisper
import math

# Load model once (IMPORTANT: do NOT load inside function again & again)
model = whisper.load_model("small")


def transcribe_audio(file_path):
    """
    Takes audio file path
    Returns:
        - transcription text
        - V_STT (confidence score 0–1)
    """

    # 1️⃣ Transcription
    result = model.transcribe(file_path)
    complaint_text = result["text"].strip()

    print("📝 Transcription:")
    print(complaint_text)
    # 2️⃣ Confidence Calculation (YOUR FULL LOGIC)
    weighted_confidence_sum = 0
    total_duration = 0

    for segment in result["segments"]:
        duration = segment["end"] - segment["start"]

        confidence = math.exp(segment["avg_logprob"])

        no_speech_prob = segment.get("no_speech_prob", 0)
        adjusted_confidence = confidence * (1 - no_speech_prob)

        weighted_confidence_sum += adjusted_confidence * duration
        total_duration += duration

    if total_duration > 0:
        final_confidence = weighted_confidence_sum / total_duration
    else:
        final_confidence = 0.0

    # Clamp between 0–1
    final_confidence = max(0, min(final_confidence, 1))

    V_STT = round(final_confidence, 3)

    return complaint_text, V_STT