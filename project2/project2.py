# lead_scoring_engine.py
import pandas as pd

# Step 1: Load the CSV file
df = pd.read_csv('data.csv')  # Make sure this file exists in the same directory

# Step 2: Normalize features (0-1 scale)
df['Interactions_norm'] = (df['Interactions'] - df['Interactions'].min()) / (df['Interactions'].max() - df['Interactions'].min())
df['Recency_norm'] = 1 - (df['Last Contact (days ago)'] - df['Last Contact (days ago)'].min()) / (df['Last Contact (days ago)'].max() - df['Last Contact (days ago)'].min())
df['ProductFit_norm'] = df['Product Fit Score'] / 10

# Step 3: Calculate weighted score
weights = {
    'Interactions_norm': 0.4,
    'Recency_norm': 0.3,
    'ProductFit_norm': 0.3
}
s = df['Score'] = ((
    df['Interactions_norm'] * weights['Interactions_norm'] +
    df['Recency_norm'] * weights['Recency_norm'] +
    df['ProductFit_norm'] * weights['ProductFit_norm']
) * 100)

df['Rounded Score'] = s.round(1)

# Step 4: Tag leads based on score
def tag_lead(score):
    if score >= 80:
        return 'Hot'
    elif score >= 50:
        return 'Warm'
    else:
        return 'Cold'

df['Tag'] = df['Rounded Score'].apply(tag_lead)

# Step 5: Output results
print(df[['Lead ID', 'Rounded Score', 'Tag']])

# Optionally: Save to CSV
df[['Lead ID', 'Rounded Score', 'Tag']].to_csv('scored_leads.csv', index=False)
