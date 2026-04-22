def process_audio(filepath):
    text, confidence = speech_to_text(filepath)

    VUser = 0.5  # default
    VGeo = 0.5   # dummy for now

    trust = (1*confidence + 2*VGeo + 3*VUser) / 6

    severity = extract_severity(text)
    infra = 0.5
    history = 0.5

    priority = (3*severity + 4*infra + 2*history) / 9

    triage = trust * priority

    if triage > 0.7:
        category = "HIGH"
    elif triage > 0.4:
        category = "NORMAL"
    else:
        category = "INVALID"

    return {
        "text": text,
        "trust": round(trust,2),
        "priority": round(priority,2),
        "triage": round(triage,2),
        "category": category
    }