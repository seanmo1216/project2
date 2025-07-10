# funnel_analyzer.py
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load journey data from CSV
# Expected format: User ID, Timestamp, Stage

df = pd.read_csv('journey_input.csv')

# Ensure timestamp is parsed as datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Step 2: Sort and keep first entry per user per stage (in case of repeated stages)
df_sorted = df.sort_values(by=['User ID', 'Timestamp'])
df_unique = df_sorted.drop_duplicates(subset=['User ID', 'Stage'], keep='first')

# Step 3: Define ordered journey stages
stage_order = ['Awareness', 'Interest', 'Contact', 'Demo', 'Purchase']
df_unique['Stage'] = pd.Categorical(df_unique['Stage'], categories=stage_order, ordered=True)

# Step 4: Count unique users per stage
stage_counts = df_unique.groupby('Stage')['User ID'].nunique().reindex(stage_order)

# Step 5: Calculate conversion and drop-off rates
stage_data = pd.DataFrame({
    'Stage': stage_counts.index,
    'User Count': stage_counts.values
})

stage_data['Conversion Rate (%)'] = stage_data['User Count'].pct_change(-1).abs().fillna(0) * 100
stage_data['Drop-off (%)'] = 100 - stage_data['Conversion Rate (%)']

# Step 6: Plot funnel chart
plt.figure(figsize=(10, 6))
plt.barh(stage_data['Stage'], stage_data['User Count'])
plt.gca().invert_yaxis()
plt.title('Customer Journey Funnel')
plt.xlabel('Number of Users')
plt.tight_layout()
plt.savefig('funnel_chart.png')
plt.show()

# Step 7: Output results
print(stage_data)
stage_data.to_csv('funnel_summary.csv', index=False)
