import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
print("⚙ Creating Dummy Dataset...")
# Create a date range for the index
dates = pd.date_range('2023-01-01', periods=365, freq='D')

# Create synthetic pollutant data
np.random.seed(42) # for reproducibility
pm25_base = 150 # Base level for PM2.5 (usually high in Delhi)
pm25_data = np.abs(np.random.normal(loc=pm25_base, scale=80, size=len(dates)))
co_data = np.abs(np.random.normal(loc=1.5, scale=0.8, size=len(dates)))
so2_data = np.abs(np.random.normal(loc=15, scale=10, size=len(dates)))

# Introduce some NaN values to test the missing value handling
pm25_data[::25] = np.nan
co_data[::50] = np.nan

df = pd.DataFrame({
    'PM2.5': pm25_data,
    'CO': co_data,
    'SO2': so2_data
}, index=dates)

df.index.name = 'Date' # Set index name for clarity

# --- Step 2: Understanding and Cleaning ---
print("\n📌 Dataset Info:")
print(df.info())

# Step 3: Check and Fill missing values
print("\n📌 Missing Values in Dataset (Before Fill):")
print(df.isnull().sum())

# Fill missing values with column mean
df.fillna(df.mean(numeric_only=True), inplace=True)

print("\n📌 Missing Values in Dataset (After Fill):")
print(df.isnull().sum())

# Step 4: Basic statistics
print("\n📌 Pollutant Statistics:")
print(df.describe().T)

# --- Step 5: Yearly/Monthly PM2.5 Trend ---
plt.figure(figsize=(12, 5))
df['PM2.5'].resample('ME').mean().plot(marker='o', linestyle='-') # Changed 'M' to 'ME'
plt.title("Monthly Average PM2.5 Levels (Simulated)", fontsize=14)
plt.xlabel("Month")
plt.ylabel("PM2.5 concentration (µg/m³)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# --- Step 6: Correlation Heatmap ---
numeric_df = df.select_dtypes(include=['float64', 'int64'])
if numeric_df.shape[1] > 1:
    corr = numeric_df.corr()
    print("\n📌 Pollutant Correlation Matrix:")
    print(corr)

    # Use object-oriented plotting with plt.subplots to avoid figure management issues
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.matshow(corr.values, cmap='viridis')
    fig.colorbar(im, ax=ax, label='Correlation Coefficient')

    # Add labels to the heatmap - use ax methods
    cols = numeric_df.columns
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(cols, rotation=45, ha='left')
    ax.set_yticks(range(len(cols)))
    ax.set_yticklabels(cols)

    # Add correlation values on the heatmap
    for i in range(len(cols)):
        for j in range(len(cols)):
            ax.text(j, i, f'{corr.iloc[i, j]:.2f}', ha='center', va='center', color='w', fontsize=10)

    ax.set_title("Pollutant Correlation Heatmap", y=1.2, fontsize=14)
    plt.show()

# --- Step 7: AQI Category based on PM2.5 ---
def get_aqi_category(pm25):
    if pm25 <= 50: return "Good"
    elif pm25 <= 100: return "Satisfactory"
    elif pm25 <= 200: return "Moderate"
    elif pm25 <= 300: return "Poor"
    elif pm25 <= 400: return "Very Poor"
    else: return "Severe"

df['AQI_Category'] = df['PM2.5'].apply(get_aqi_category)

print("\n📌 AQI Category Count:")
print(df['AQI_Category'].value_counts())

plt.figure(figsize=(10, 6))
df['AQI_Category'].value_counts().reindex(['Good', 'Satisfactory', 'Moderate', 'Poor', 'Very Poor', 'Severe']).plot(
    kind='bar', color=plt.cm.Spectral(np.linspace(0, 1, 6))
)
plt.title("Air Quality Index Category Distribution (Simulated)", fontsize=14)
plt.xlabel("AQI Category")
plt.ylabel("Count")
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
