# Project 2: Lead Scoring Simulation Engine
from flask import Flask, request, jsonify

app = Flask(__name__)

# Weight configuration for scoring logic
WEIGHTS = {
    'interaction_count': 0.4,
    'recency': 0.3,
    'product_interest_score': 0.3
}

# Normalization bounds
BOUNDS = {
    'interaction_count': 30,
    'days_since_last_contact': 30,
    'product_interest_score': 10
}

@app.route('/lead_score', methods=['POST'])
def lead_score():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing JSON body'}), 400

    # Expecting customer profile data directly in JSON
    lead = {
        'interaction_count': data.get('interaction_count', 0),
        'days_since_last_contact': data.get('days_since_last_contact', BOUNDS['days_since_last_contact']),
        'product_interest_score': data.get('product_interest_score', 5.0)
    }

    # Clamp and normalize values
    interaction = min(max(lead['interaction_count'], 0), BOUNDS['interaction_count'])
    recency = min(max(lead['days_since_last_contact'], 0), BOUNDS['days_since_last_contact'])
    interest = min(max(lead['product_interest_score'], 0), BOUNDS['product_interest_score'])

    interaction_norm = interaction / BOUNDS['interaction_count']
    recency_norm = (BOUNDS['days_since_last_contact'] - recency) / BOUNDS['days_since_last_contact']
    interest_norm = interest / BOUNDS['product_interest_score']

    # Weighted scoring
    score = 100 * (
        WEIGHTS['interaction_count'] * interaction_norm +
        WEIGHTS['recency'] * recency_norm +
        WEIGHTS['product_interest_score'] * interest_norm
    )

    return jsonify({
        'score': round(score, 1),
        'normalized_inputs': {
            'interaction_count': round(interaction_norm, 2),
            'recency': round(recency_norm, 2),
            'product_interest_score': round(interest_norm, 2)
        },
        'weights': WEIGHTS,
        'bounds': BOUNDS
    })

if __name__ == '__main__':
    app.run(debug=True)
