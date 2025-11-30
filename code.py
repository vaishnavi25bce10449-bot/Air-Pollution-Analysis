# -----------------------------------------
# Air Quality Analysis - Delhi (Python)
# -----------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
# Step 1: Load Dataset
file_path = "delhi_air_quality.csv"   # Change path as needed
df = pd.read_csv(file_path)
# Step 2: Understanding the dataset
print("\n📌 Dataset Info:")
print(df.info())
print("\n📌 First 5 rows:")
print(df.head())
# Convert Date column to datetime format (if available)
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
# Step 3: Check for missing values
print("\n📌 Missing Values in Dataset:")
print(df.isnull().sum())
# Fill missing values with column mean
df.fillna(df.mean(numeric_only=True), inplace=True)
# Step 4: Basic statistics
print("\n📌 Pollutant Statistics:")
print(df.describe())
# Step 5: Yearly/Monthly PM2.5 Trend
if 'PM2.5' in df.columns:
    #df['PM2.5'].resample('M').mean().plot()
    plt.title("Monthly Average PM2.5 Levels in Delhi")
    plt.xlabel("Year")
    plt.ylabel("PM2.5 concentration (µg/m³)")
    plt.show()
# Step 6: Correlation Heatmap
if df.select_dtypes(include=['float64', 'int64']).shape[1] > 1:
    corr = df.corr()
    print("\n📌 Pollutant Correlation Matrix:")
    print(corr)
    plt.matshow(corr)
    plt.title("Pollutant Correlation Heatmap")
    plt.colorbar()
    plt.show()
# Step 7: AQI Category based on PM2.5
def get_aqi_category(pm25):
    if pm25 <= 50: return "Good"
    elif pm25 <= 100: return "Satisfactory"
    elif pm25 <= 200: return "Moderate"
    elif pm25 <= 300: return "Poor"
    elif pm25 <= 400: return "Very Poor"
    else: return "Severe"
if 'PM2.5' in df.columns:
    df['AQI_Category'] = df['PM2.5'].apply(get_aqi_category)
    print("\n📌 AQI Category Count:")
    print(df['AQI_Category'].value_counts())
    df['AQI_Category'].value_counts().plot(kind='bar')
    plt.title("Delhi Air Quality Index Category Distribution")
    plt.xlabel("AQI Category")
    plt.ylabel("Number of Days")
    plt.show()

   
 
