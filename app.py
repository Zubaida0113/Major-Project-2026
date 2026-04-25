from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from model.transcription import transcribe_audio
from model.categorization import categorize  # ensure correct function name
from model.scoring import *
from model.geo import *
import pandas as pd
import os

app = Flask(__name__, template_folder="templates")
CORS(app)

# ✅ Load rulebook ONCE (IMPORTANT)
rules_db = pd.read_excel(
    "data/RWA_RuleBook.xlsx",
    sheet_name=None
)

# ✅ Ensure uploads folder exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")


@app.route("/")
def home():
    return render_template("resident-dashboard.html")


@app.route("/analyze-audio", methods=["POST"])
def analyze_audio():
    print("🔥 API HIT")

    # 1️⃣ Save audio
    audio = request.files["audio"]
    file_path = os.path.join("uploads", audio.filename)
    audio.save(file_path)

    # 2️⃣ Transcription
    text, V_STT = transcribe_audio(file_path)

    # 3️⃣ Categorization
    category, nlp_confidence = categorize(text, rules_db)

    # 4️⃣ Geo
    gps = capture_gps()
    complaint = create_complaint_object(text, gps)

    resolved_address = resolve_location(
        complaint["latitude"],
        complaint["longitude"]
    )

    complaint["resolved_location"] = resolved_address

    V_Geo = compute_V_Geo(
        text,
        resolved_address,
        complaint["gps_accuracy"]
    )

    # 5️⃣ Scoring
    P_Sev = compute_P_Sev(text)
    P_Infra = compute_P_Infra(resolved_address)
    P_Hist = compute_P_Hist(0)

    V_User = 0.5

    S_T = compute_trust_score(V_STT, V_Geo, V_User)
    S_P = compute_priority_score(P_Sev, P_Infra, P_Hist)
    S_Triage = compute_S_Triage(S_T, S_P)

    # ✅ FIXED classify_action call
    action = classify_action(
        S_T=S_T,
        S_P=S_P,
        S_Triage=S_Triage,
        V_User=V_User,
        has_history=False,
        P_Hist=P_Hist,
        category=category,
        essential_categories=[],  # you can pass your computed list
        V_STT=V_STT,
        nlp_confidence=nlp_confidence,
        complaint_text=text
    )

    # 6️⃣ RETURN REAL OUTPUT
    return jsonify({
        "transcript": text,
        "category": category,
        "address": resolved_address,
        "priority": action,
        "S_T": S_T,
        "S_P": S_P,
        "S_Triage": S_Triage
    })


if __name__ == "__main__":
    app.run(debug=True)