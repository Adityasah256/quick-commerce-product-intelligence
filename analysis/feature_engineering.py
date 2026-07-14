import pandas as pd
from pathlib import Path

# =====================================
# Project Paths
# =====================================

INPUT_PATH = Path("data/processed/milk_products.csv")
OUTPUT_PATH = Path("data/final/analytics_dataset.csv")

df = pd.read_csv(INPUT_PATH)

# discount_percent

df["discount_percent"] = (
    (df["mrp"] - df["price"]) / df["mrp"] * 100
).round(2)

df["discount_percent"] = df["discount_percent"].fillna(0)

# savings

df["savings"] = df["mrp"] - df["price"]

# Inventory Bycket

def inventory_bucket(x):
    if x <= 5:
        return "Low"
    elif x <= 20:
        return "Medium"
    else:
        return "High"

df["inventory_bucket"] = df["inventory"].apply(inventory_bucket)

# Stock Status

def stock_status(x):
    if x == 0:
        return "Out of Stock"
    elif x <= 5:
        return "Low Stock"
    else:
        return "In Stock"

df["stock_status"] = df["inventory"].apply(stock_status)

# Price Segment

def price_segment(price):
    if price < 50:
        return "Budget"
    elif price < 150:
        return "Mid Range"
    else:
        return "Premium"

df["price_segment"] = df["price"].apply(price_segment)

# Rating Bucket

def rating_bucket(rating):
    if rating < 3.5:
        return "Poor"
    elif rating < 4.5:
        return "Good"
    else:
        return "Excellent"

df["rating_bucket"] = df["rating"].apply(rating_bucket)

# Value Score (Custom KPI)

df["value_score"] = (
    df["rating"] * 20
    + df["discount_percent"] * 2
    - df["price"] * 0.05
).round(2)

# Saving the analytics dataset:

df.to_csv(OUTPUT_PATH, index=False)

print(f"Analytics dataset saved to {OUTPUT_PATH}")