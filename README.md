# 📊 Lead Scoring Engine

This Python script calculates a weighted lead score based on input CRM data and categorizes leads as "Hot," "Warm," or "Cold." It is ideal for sales and marketing teams who want to prioritize outreach based on lead quality.

---

## 🚀 How It Works

1. Loads a CSV file (leads\_input.csv) containing lead interaction data.
2. Normalizes selected features to bring them into the same scale.
3. Applies a weighted formula to calculate a score for each lead.
4. Tags the lead based on the score (Hot, Warm, or Cold).
5. Outputs the results to a clean CSV file (scored\_leads.csv).

---

## 📁 CSV Input Format (leads\_input.csv)

The CSV must contain the following columns:

| Column Name             | Description                              |
| ----------------------- | ---------------------------------------- |
| Lead ID                 | Unique identifier for each lead          |
| Interactions            | Number of interactions (messages/clicks) |
| Last Contact (days ago) | Days since last contact (lower = better) |
| Product Fit Score       | Fit score from 0 to 10 (higher = better) |

📌 Example:

```csv
Lead ID,Interactions,Last Contact (days ago),Product Fit Score
L001,12,2,9.5
L002,3,14,6.0
L003,8,5,7.5
```

---

## 🧮 Scoring Formula

The score is calculated using normalized values:

```python
Score = (0.4 × Interactions_norm) +
        (0.3 × Recency_norm) +
        (0.3 × ProductFit_norm)
```

The final score is scaled to a 0–100 range.

---

## 🏷️ Lead Tags

| Score Range | Tag  |
| ----------- | ---- |
| 80–100      | Hot  |
| 50–79.9     | Warm |
| 0–49.9      | Cold |

---

## 💾 Output

A new file called `scored_leads.csv` will be saved, containing:

| Lead ID | Score | Tag  |
| ------- | ----- | ---- |
| L001    | 91.5  | Hot  |
| L002    | 46.2  | Cold |

---

## ✅ Requirements

* Python 3.7+
* pandas

Install with:

```bash
pip install pandas
```

---

## 👩‍💻 To Run

Place `leads_input.csv` in the same folder as the script and run:

```bash
python lead_scoring_engine.py
```

---

## 📬 Questions?

Feel free to reach out if you'd like to customize the scoring logic, weights, or integrate into iMBrace workflows!
