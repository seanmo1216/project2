import streamlit as st
import openai
import re

# Define weights for BANT criteria
WEIGHTS = {
    "Budget": 0.25,
    "Authority": 0.25,
    "Need": 0.30,
    "Timing": 0.20,
}

# Replace with your actual OpenAI API key
client = openai.Client(api_key=st.secrets["openai_api_key"] if "openai_api_key" in st.secrets else "YOUR_API_KEY")

def calculate_score(scores):
    return sum(scores[criterion] * weight for criterion, weight in WEIGHTS.items())

def get_recommendation(score):
    if score >= 8:
        return "✅ Strong fit – actively pursue"
    elif score >= 6:
        return "⚠️ Moderate fit – pursue with caution"
    else:
        return "❌ Weak fit – deprioritize or nurture"

def ask_ai_to_adjust_score(scores, notes, company):
    try:
        prompt = f"""
You are a senior B2B sales advisor evaluating a sales opportunity using the BANT framework: Budget, Authority, Need, and Timing.

You are provided:
- A company name
- BANT scores (0–10) from a sales rep
- Notes explaining each score

Treat the rep’s scores as a subjective baseline. Your job is to:
1. Agree or adjust each score slightly based on the quality of notes and company context.
2. Be stricter when notes are vague, uncertain, or not from decision-makers.
3. Be more lenient if the company is large, strategic, or influential.
4. Assume a typical project budget range of HKD 100,000–10,000,000.

Respond concisely and clearly.

Output format:
Adjusted Scores:
- Budget: X/10
- Authority: X/10
- Need: X/10
- Timing: X/10

Final Score: X.X/10
Justification: (1 short paragraph)

Company: {company}

Sales Rep Scores:
"""
        for key, val in scores.items():
            prompt += f"- {key}: {val}/10\n"

        prompt += "\nSales Rep Notes:\n"
        for key, note in notes.items():
            if note:
                prompt += f"- {key}: {note}\n"

        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Error generating AI response: {e}"

def parse_adjusted_scores(ai_output):
    adjusted = {}
    try:
        for line in ai_output.splitlines():
            match = re.match(r"- (Budget|Authority|Need|Timing): (\d+(\.\d+)?)/10", line.strip())
            if match:
                adjusted[match.group(1)] = float(match.group(2))
    except:
        pass
    return adjusted

st.title("🔍 BANT Sales Qualification Tool + AI Assist")
st.markdown("Rate each factor from 0 (poor) to 10 (excellent). AI will assist based on your notes and company name to refine the score.")

company = st.text_input("Company Name")
scores = {}
notes = {}

for criterion in WEIGHTS:
    scores[criterion] = st.slider(f"{criterion} Score", 0, 10, 5)
    notes[criterion] = st.text_area(f"Notes for {criterion}", "", key=f"note_{criterion}")

if st.button("Calculate Qualification Score"):
    final_score = calculate_score(scores)
    recommendation = get_recommendation(final_score)

    st.subheader("Initial Results")
    st.metric(label="BANT Score", value=f"{final_score:.1f}/10")
    st.success(recommendation)

    st.subheader("Your Notes")
    if company:
        st.markdown(f"**Company:** {company}")
    for criterion in WEIGHTS:
        if notes[criterion]:
            st.markdown(f"**{criterion}:** {notes[criterion]}")

    st.subheader("🤖 AI-Adjusted Assessment")
    ai_output = ask_ai_to_adjust_score(scores, notes, company)
    st.markdown(ai_output)

    st.subheader("📊 AI vs Your Scores")
    adjusted_scores = parse_adjusted_scores(ai_output)
    if adjusted_scores:
        for criterion in WEIGHTS:
            user_score = scores[criterion]
            ai_score = adjusted_scores.get(criterion)
            if ai_score is not None:
                delta = ai_score - user_score
                st.metric(label=f"{criterion}", value=f"AI: {ai_score:.1f}/10", delta=f"{delta:+.1f}")
