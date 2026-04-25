from fuzzywuzzy import fuzz
import pandas as pd
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    stopwords = {'hi', 'hello', 'please', 'check', 'thanks', 'regards'}
    return [w for w in text.split() if w not in stopwords]

def keyword_match_score(text, rule_keywords):
    text_words = set(clean_text(text))
    keywords = set(clean_text(rule_keywords))
    if not keywords:
        return 0
    return len(text_words & keywords) / len(keywords)


def fuzzy_match_score(text, rule_keywords):
    text_clean_str = ' '.join(clean_text(text))
    keywords_list = clean_text(rule_keywords)

    if not keywords_list:
        return 0

    scores = [fuzz.partial_ratio(text_clean_str, kw) / 100 for kw in keywords_list]
    return max(scores)

def combined_score(text, rule_keywords, alpha=0.6):
    exact = keyword_match_score(text, rule_keywords)
    fuzzy = fuzzy_match_score(text, rule_keywords)
    return alpha * exact + (1 - alpha) * fuzzy

EMERGENCY_TERMS = [
    "gas","gas smell","smell of gas","fire","smoke","sparks",
    "electric shock","short circuit","explosion","burning"
]

def emergency_category_override(text):
    text = text.lower()
    for term in EMERGENCY_TERMS:
        if term in text:
            return "Emergency and Public Service Co"
    return None

def categorize_complaint(complaint_text, rules_db, emergency_override_category=None, threshold=0.2):

    if emergency_override_category:
        return emergency_override_category, 1.0

    best_category = "Uncategorized"
    best_score = 0

    for category, df in rules_db.items():
        if 'Keywords' in df.columns:
            for _, row in df.iterrows():
                rule_keywords = str(row['Keywords']) if pd.notna(row['Keywords']) else ""
                score = combined_score(complaint_text, rule_keywords)
                if score > best_score:
                    best_score = score
                    best_category = category
        elif 'Subject' in df.columns and 'Rule Description' in df.columns:
            for _, row in df.iterrows():
                rule_text = f"{row['Subject']} {row['Rule Description']}".strip()
                score = combined_score(complaint_text, rule_text)
                if score > best_score:
                    best_score = score
                    best_category = category

    if best_score < threshold:
        return "Uncategorized", round(best_score, 3)

    return best_category, round(best_score, 3)