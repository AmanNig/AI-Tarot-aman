import pandas as pd
from utils.intent import classify_intent
from core.tarot_reader import perform_reading

# 1. Load your test questions
df = pd.read_csv("50_Test_Questions.csv")

# 2. Iterate and collect results
rows = []
for q in df['question']:
    intent = classify_intent(q)
    # no conversation history needed for batch
    res = perform_reading(q, intent, history=[])
    rows.append({
        "question": q,
        "intent": intent,
        "interpretation": res.get("interpretation", ""),
        "card": res.get("card", ""),
        "date_start": (res.get("date_range") or ["",""])[0],
        "date_end":   (res.get("date_range") or ["",""])[1],
        "cards_drawn": ", ".join(res.get("cards", []))
    })

# 3. Save to CSV for review
out = pd.DataFrame(rows)
#out.to_csv("batch_results.csv", index=False)
print("Batch test complete – see batch_results.csv")
print(out)
