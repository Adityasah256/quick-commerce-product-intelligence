import pandas as pd

df = pd.read_csv(
    "blinkit_products.csv"
)

print("\n===== DATASET OVERVIEW =====")
print(df.shape)

# BRAND ASSORTMENT
print("\n===== BRAND DISTRIBUTION =====")
print(
    df["brand"]
    .value_counts()
)

# PRODUCT CATEGORY
print("\n===== PRODUCT CATEGORY =====")
print(
    df["product_category"]
    .value_counts()
)

# PRICE SEGMENT
print("\n===== PRICE SEGMENT =====")
print(
    df["price_segment"]
    .value_counts()
)

# INVENTORY
print("\n===== TOP INVENTORY PRODUCTS =====")
print(
    df[
        [
            "product_name",
            "inventory",
            "inventory_bucket"
        ]
    ]
    .sort_values(
        "inventory",
        ascending=False
    )
)

# BEST VALUE
print("\n===== BEST VALUE PRODUCTS =====")
print(
    df[
        [
            "product_name",
            "price_per_100ml"
        ]
    ]
    .sort_values(
        "price_per_100ml"
    )
)

# RATINGS
print("\n===== HIGHEST RATED PRODUCTS =====")
print(
    df[
        [
            "product_name",
            "rating"
        ]
    ]
    .sort_values(
        "rating",
        ascending=False
    )
)

# BRAND ANALYSIS
print("\n===== BRAND ASSORTMENT =====")

brand_analysis = (
    df.groupby("brand")
      .size()
      .reset_index(name="sku_count")
      .sort_values(
          "sku_count",
          ascending=False
      )
)

print(brand_analysis)

# INVENTORY ANALYSIS
print("\n===== INVENTORY ANALYSIS =====")

inventory_analysis = (
    df.groupby("brand")["inventory"]
      .mean()
      .reset_index()
      .sort_values(
          "inventory",
          ascending=False
      )
)

print(inventory_analysis)

# PRICE ANALYSIS
print("\n===== PRICE POSITIONING =====")

price_analysis = (
    df.groupby("brand")["price_per_100ml"]
      .mean()
      .reset_index()
      .sort_values(
          "price_per_100ml",
          ascending=False
      )
)

print(price_analysis)

# CUSTOMER PREFERENCE
print("\n===== CUSTOMER PREFERENCE =====")

rating_analysis = (
    df.groupby("brand")["rating"]
      .mean()
      .reset_index()
      .sort_values(
          "rating",
          ascending=False
      )
)

print(rating_analysis)