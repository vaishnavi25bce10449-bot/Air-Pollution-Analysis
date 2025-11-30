import kagglehub
import os # Import the os module for path manipulation
path = kagglehub.dataset_download("kunshbhatia/delhi-air-quality-dataset")
print("Path to dataset files:", path)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score
# Construct the full path to the CSV file using the downloaded path
df = pd.read_csv(os.path.join(path, "final_dataset.csv"))
df.head()
df.tail()
df.shape
df.info()
df.isnull().sum()
df.duplicated().sum()
df = df.drop(columns=['Date'])
plt.figure(figsize=(10,7))
sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="crest")
plt.title("Correlation Heatmap")
plt.show()
X = df.drop(columns=['AQI'])
y = df['AQI']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
lr = LinearRegression()
lr.fit(X_train, y_train)
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)
lasso = Lasso(alpha=0.01)
lasso.fit(X_train, y_train)
models = {"Linear": lr, "Ridge": ridge, "Lasso": lasso}
for name, model in models.items():
    pred = model.predict(X_test)
    print(name)
    print("R2 Score:", r2_score(y_test, pred))
    # Calculate RMSE by taking the square root of MSE
    print("RMSE:", np.sqrt(mean_squared_error(y_test, pred)))
    print("-"*40)
plt.figure(figsize=(8,6))
plt.scatter(y_test, lr.predict(X_test))
plt.xlabel("Actual AQI")
plt.ylabel("Predicted AQI")
plt.title("Actual vs Predicted AQI (Linear Regression)")
plt.show()
importance = pd.Series(lasso.coef_, index=X.columns)
importance.sort_values().plot(kind='bar', figsize=(10,6))
plt.title("Feature Importance using Lasso Regression")
plt.show()
plt.figure(figsize=(8,6))
plt.scatter(y_test, lr.predict(X_test))
plt.xlabel("Actual AQI")
plt.ylabel("Predicted AQI")
plt.title("Actual vs Predicted AQI (Linear Regression)")
plt.show()
importance = pd.Series(lasso.coef_, index=X.columns)
importance.sort_values().plot(kind='bar', figsize=(10,6))
plt.title("Feature Importance using Lasso Regression")
plt.show()
