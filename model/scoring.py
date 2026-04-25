from fuzzywuzzy import fuzz

SEVERITY_KEYWORDS = {
    "fire": 1.0,
    "gas leak": 1.0,
    "short circuit": 1.0,
    "electric shock": 1.0,

    "no water": 0.7,
    "water supply": 0.7,
    "no electricity": 0.7,
    "power outage": 0.7,

    "leak": 0.6,
    "overflow": 0.6,
    "seepage": 0.6,

    "damage": 0.5,
    "broken": 0.5
}

EMERGENCY_PATTERNS = [
    "fire","gas","gas smell","smell of gas",
    "leak","electric shock","short circuit",
    "sparks","burning"
]

def compute_P_Sev(text):
    text = text.lower()

    for pattern in EMERGENCY_PATTERNS:
        if pattern in text:
            return 1.0

    scores = []
    for keyword, sev_score in SEVERITY_KEYWORDS.items():
        similarity = fuzz.partial_ratio(keyword, text) / 100
        if similarity > 0.6:
            scores.append(sev_score * similarity)

    return round(max(scores), 2) if scores else 0.3

CRITICAL_LOCATIONS = {
    "hospital": 1.0,
    "transformer": 0.9,
    "main pipeline": 0.85,
    "water tank": 0.8
}

PROXIMITY_BOOST = ["near","beside","adjacent","outside","inside"]

def compute_P_Infra(location_text):
    text = location_text.lower()
    scores = []

    for infra, weight in CRITICAL_LOCATIONS.items():
        similarity = fuzz.partial_ratio(infra, text) / 100

        if similarity > 0.7:
            base = weight * similarity

            if any(word in text for word in PROXIMITY_BOOST):
                base = min(1.0, base + 0.1)

            scores.append(base)

    return round(max(scores), 2) if scores else 0.0

def compute_P_Hist(count, has_history=False):
    if not has_history:
        return 0.5

    if count >= 4:
        return 0.8
    elif count >= 2:
        return 0.6
    elif count >= 1:
        return 0.4
    return 0.5

def compute_trust_score(V_STT, V_Geo, V_User, w1=1, w2=2, w3=3):
    numerator = (w1 * V_STT) + (w2 * V_Geo) + (w3 * V_User)
    denominator = w1 + w2 + w3
    return round(numerator / denominator, 3)

def compute_priority_score(P_Sev, P_Infra, P_Hist, k1=3, k2=4, k3=2):
    raw_score = ((k1 * P_Sev) + (k2 * P_Infra) + (k3 * P_Hist)) / (k1 + k2 + k3)

    if P_Sev >= 0.7:
        raw_score = max(raw_score, 0.4)

    return round(raw_score, 3)

def compute_S_Triage(S_T, S_P):
    return round(S_T * S_P, 3)

def classify_action(S_T, S_P, S_Triage):
    if S_P >= 0.7 and S_T >= 0.5:
        return "Critical Priority"

    if S_Triage >= 0.5:
        return "High Priority"
    elif S_Triage >= 0.20:
        return "Normal Priority"

    if S_T < 0.4:
        return "Flagged for Verification"

    return "Normal Priority"