from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import re

def capture_gps():
    return {
        "latitude": 28.591060641277412,
        "longitude": 77.44408987259794,
        "accuracy_meters": 8,
        "timestamp": "2025-02-12T10:45:00"
    }

def create_complaint_object(text, gps):
    return {
        "complaint_text": text,
        "latitude": gps["latitude"],
        "longitude": gps["longitude"],
        "gps_accuracy": gps["accuracy_meters"],
        "timestamp": gps["timestamp"]
    }



geolocator = Nominatim(user_agent="rwa-complaint-system")
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)

def resolve_location(lat, lon):
    try:
        location = reverse((lat, lon), exactly_one=True)
        return location.address if location else "Location not found"
    except:
        return "Location not found"
    
def extract_text_location(text):
    patterns = [
        r'\b[A-Z]\d{3}\b',
        r'\bFlat\s?\d+\b',
        r'\bSector\s?\d+\b'
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)

    return None

def text_geo_match_score(text_location, resolved_address):
    if not text_location:
        return 0.3

    if text_location.lower() in resolved_address.lower():
        return 1.0

    return 0.5

def compute_V_Geo(complaint_text, resolved_address, gps_accuracy_m=10):
    text_location = extract_text_location(complaint_text)
    text_match = text_geo_match_score(text_location, resolved_address)

    if gps_accuracy_m <= 10:
        gps_reliability = 1.0
    elif gps_accuracy_m <= 25:
        gps_reliability = 0.7
    else:
        gps_reliability = 0.4

    V_Geo = (0.6 * text_match) + (0.4 * gps_reliability)

    return round(V_Geo, 3)