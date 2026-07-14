import pandas as pd
from pathlib import Path

# =====================================
# Project Paths
# =====================================

INPUT_PATH = Path("data/processed/milk_products.csv")
OUTPUT_PATH = Path("data/final/analytics_dataset.csv")


# =====================================
# Load Dataset
# =====================================

def load_data() -> pd.DataFrame:
    """
    Load the processed dataset.
    """
    return pd.read_csv(INPUT_PATH)


# =====================================
# Helper Functions
# =====================================

def inventory_bucket(inventory: int) -> str:
    """Categorize inventory into Low, Medium, or High."""

    if inventory <= 5:
        return "Low"
    elif inventory <= 20:
        return "Medium"
    else:
        return "High"


def stock_status(inventory: int) -> str:
    """Categorize stock availability."""

    if inventory == 0:
        return "Out of Stock"
    elif inventory <= 5:
        return "Low Stock"
    else:
        return "In Stock"


def price_segment(price: float) -> str:
    """Categorize products by price."""

    if price < 50:
        return "Budget"
    elif price < 150:
        return "Mid Range"
    else:
        return "Premium"


def rating_bucket(rating: float) -> str:
    """Categorize product ratings."""

    if rating < 3.5:
        return "Poor"
    elif rating < 4.5:
        return "Good"
    else:
        return "Excellent"


# =====================================
# Feature Engineering
# =====================================

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create engineered features for product analytics.
    """

    # Discount Percentage

    df["discount_percent"] = (
        (df["mrp"] - df["price"]) / df["mrp"] * 100
    ).round(2)

    df["discount_percent"] = df["discount_percent"].fillna(0)

    # Savings

    df["savings"] = df["mrp"] - df["price"]

    # Inventory

    df["inventory_bucket"] = df["inventory"].apply(
        inventory_bucket
    )

    # Stock Status

    df["stock_status"] = df["inventory"].apply(
        stock_status
    )

    # Price Segment

    df["price_segment"] = df["price"].apply(
        price_segment
    )

    # Rating Bucket

    df["rating_bucket"] = df["rating"].apply(
        rating_bucket
    )

    # Value Score (Custom KPI)

    df["value_score"] = (
        df["rating"] * 20
        + df["discount_percent"] * 2
        - df["price"] * 0.05
    ).round(2)

    return df


# =====================================
# Save Dataset
# =====================================

def save_dataset(df: pd.DataFrame) -> None:
    """
    Save the analytics dataset.
    """

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(f"Analytics dataset saved to {OUTPUT_PATH}")


# =====================================
# Main
# =====================================

def main():

    df = load_data()

    df = engineer_features(df)

    save_dataset(df)


if __name__ == "__main__":

    main()    