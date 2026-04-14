import json

def generate_variations(text):
    return [
        text,
        f"In simple terms, {text}",
        f"{text} This is important for understanding heart health.",
        f"{text} Doctors use this for diagnosis and treatment.",
        f"{text} It plays a key role in patient care.",
        f"{text} This helps in managing cardiovascular conditions.",
        f"{text} It is essential in cardiology practice.",
        f"{text} This improves overall heart function.",
        f"{text} It contributes to better health outcomes.",
        f"{text} This is widely used in medical treatment."
    ]

# Load your dataset
with open("cardiology.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Add 10 variations to ALL records
for item in data:
    item["variations"] = generate_variations(item["text"])

# Save updated dataset
with open("cardiology_updated.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("All 50 records now have 10 variations!")