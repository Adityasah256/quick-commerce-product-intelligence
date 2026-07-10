import json
import pandas as pd

with open(
    "blinkit_response.json",
    encoding="utf-8"
) as f:
    data = json.load(f)

products = []

for item in data["response"]["snippets"]:

    try:
        product = item["data"]["atc_action"]["add_to_cart"]["cart_item"]

        rating = None

        if "rating" in item["data"]:
            rating = item["data"]["rating"]["bar"]["value"]

        products.append({
            "product_id":
                product["product_id"],

            "product_name":
                product["product_name"],

            "brand":
                product["brand"],

            "price":
                product["price"],

            "mrp":
                product["mrp"],

            "unit":
                product["unit"],

            "inventory":
                product["inventory"],

            "merchant_id":
                product["merchant_id"],

            "rating":
                rating,

            "eta":
                product["eta_identifier"]
        })

    except:
        pass

df = pd.DataFrame(products)

# Discount Percentage
df["discount_pct"] = (
    (df["mrp"] - df["price"])
    / df["mrp"]
) * 100

df["discount_pct"] = df["discount_pct"].round(2)

# Inventory Bucket
def inventory_bucket(x):
    if x <= 10:
        return "Low"
    elif x <= 30:
        return "Medium"
    else:
        return "High"

df["inventory_bucket"] = (
    df["inventory"]
    .apply(inventory_bucket)
)

# Product Category
def get_category(product):

    product = product.lower()

    if "organic" in product:
        return "Organic"

    elif "skim" in product:
        return "Skimmed"

    elif "toned" in product:
        return "Toned"

    elif "full cream" in product:
        return "Full Cream"

    else:
        return "Regular"

df["product_category"] = (
    df["product_name"]
    .apply(get_category)
)

# Stock Status
df["stock_status"] = (
    df["inventory"]
    .apply(
        lambda x:
        "Out of Stock"
        if x == 0
        else "Available"
    )
)

# Pack Size in ML
def convert_to_ml(unit):

    unit = unit.lower()

    if "ltr" in unit:
        return float(
            unit.replace("ltr","").strip()
        ) * 1000

    elif "ml" in unit:

        if "x" in unit:

            parts = unit.split("x")

            return (
                float(parts[0].strip())
                *
                float(
                    parts[1]
                    .replace("ml","")
                    .strip()
                )
            )

        return float(
            unit.replace("ml","").strip()
        )

    return None


df["pack_size_ml"] = (
    df["unit"]
    .apply(convert_to_ml)
)

# Price per 100ml
df["price_per_100ml"] = (
    df["price"]
    /
    df["pack_size_ml"]
) * 100

df["price_per_100ml"] = (
    df["price_per_100ml"]
    .round(2)
)

# Segment
def segment(price):
    if price < 35:
        return "Budget"
    elif price < 80:
        return "Mid"
    else:
        return "Premium"

df["price_segment"] = (
    df["price"]
    .apply(segment)
)

# Premium Flag
df["is_premium"] = (
    df["price_segment"]
    == "Premium"
)

# Organic Flag
df["is_organic"] = (
    df["product_name"]
    .str.lower()
    .str.contains("organic")
)

# Inventory Score
def inventory_score(x):

    if x >= 40:
        return 5

    elif x >= 20:
        return 4

    elif x >= 10:
        return 3

    elif x >= 5:
        return 2

    return 1


df["inventory_score"] = (
    df["inventory"]
    .apply(inventory_score)
)

print(df.head())
print(df.columns)
print(df.shape)

print("\n===== DATASET OVERVIEW =====")
print(df.shape)

print("\n===== BRAND DISTRIBUTION =====")
print(df["brand"].value_counts())

print("\n===== PRODUCT CATEGORY =====")
print(df["product_category"].value_counts())

print("\n===== PRICE SEGMENT =====")
print(df["price_segment"].value_counts())

print("\n===== TOP INVENTORY PRODUCTS =====")
print(
    df[
        [
            "product_name",
            "inventory",
            "inventory_bucket"
        ]
    ].sort_values(
        "inventory",
        ascending=False
    )
)

print("\n===== BEST VALUE PRODUCTS =====")
print(
    df[
        [
            "product_name",
            "price_per_100ml"
        ]
    ].sort_values(
        "price_per_100ml"
    )
)

print("\n===== HIGHEST RATED PRODUCTS =====")
print(
    df[
        [
            "product_name",
            "rating"
        ]
    ].sort_values(
        "rating",
        ascending=False
    )
)

df.to_csv(
    "blinkit_products.csv",
    index=False
)

print("\nSaved Successfully")