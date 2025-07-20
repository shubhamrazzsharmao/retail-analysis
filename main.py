import pandas as pd
import pymysql
import json

# Step 1: Connect to MySQL
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='password',
    database='retail_question'
)

print("✅ Connected to MySQL database 'retail_question'")

# Step 2: Load data from the correct table and columns
query = "SELECT Returns, Avg_Basket, Footfall FROM retail_data"
df = pd.read_sql(query, conn)
conn.close()

# Step 3: Calculate Pearson correlation coefficients
correlations = {
    "Returns-Avg_Basket": df['Returns'].corr(df['Avg_Basket']),
    "Returns-Footfall": df['Returns'].corr(df['Footfall']),
    "Avg_Basket-Footfall": df['Avg_Basket'].corr(df['Footfall'])
}

# Step 4: Identify the strongest correlation (by absolute value)
strongest_pair = max(correlations, key=lambda k: abs(correlations[k]))

# Step 5: Prepare result as JSON
result = {
    "pair": strongest_pair,
    "correlation": round(correlations[strongest_pair], 4)
}

# Step 6: Save to JSON file
with open("correlation_result.json", "w") as f:
    json.dump(result, f, indent=4)

print("✅ JSON file 'correlation_result.json' created with result:")
print(json.dumps(result, indent=4))
