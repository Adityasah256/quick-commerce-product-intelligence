import pandas as pd
from pathlib import Path

DATASET_PATH = Path("data/final/analytics_dataset.csv")
REPORT_PATH = Path("reports/analytics_report.txt")
REPORTS_DIR = Path("reports")

def log(message=""):

    print(message)

    with open(
        REPORT_PATH,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            str(message) + "\n"
        )

def section(title):

    log()

    log("=" * 70)

    log(title)

    log("=" * 70)

# ==========================
# Load Dataset
# ==========================

def load_data():

    return pd.read_csv(DATASET_PATH)


# ==========================
# Executive Summary
# ==========================

def executive_summary(df):

    log()
    log("=" * 70)
    log("QUICK COMMERCE PRODUCT ANALYTICS REPORT")
    log("=" * 70)

    log()
    log("EXECUTIVE SUMMARY")
    log()

    log(f"Total Products      : {len(df)}")
    log(f"Total Brands        : {df['brand'].nunique()}")
    log(f"Average Price       : ₹{df['price'].mean():.2f}")
    log(f"Average Rating      : {df['rating'].mean():.2f}")
    log(f"Average Discount    : {df['discount_percent'].mean():.2f}%")
    log(f"Average Inventory   : {df['inventory'].mean():.2f}")

    log("=" * 70)


# ==========================
# Brand Analysis
# ==========================

def brand_analysis(df):

    section("TOP BRANDS")

    brand_summary = (
        df.groupby("brand")
        .agg(
            Products=("product_name", "count"),
            Avg_Price=("price", "mean"),
            Avg_Rating=("rating", "mean")
        )
        .round(2)
        .fillna("N/A")
        .sort_values(
            "Products",
            ascending=False
        )
    )

    log(brand_summary.head(10).to_string())


# ==========================
# Pricing Analysis
# ==========================

def pricing_analysis(df):

    section("PRICING ANALYSIS")

    log(f"Average Price      : ₹{df['price'].mean():.2f}")
    log(f"Median Price       : ₹{df['price'].median():.2f}")
    log(f"Minimum Price      : ₹{df['price'].min():.2f}")
    log(f"Maximum Price      : ₹{df['price'].max():.2f}")

    log()
    log("Most Expensive Products")
    log()

    expensive = (
        df.sort_values(
            "price",
            ascending=False
        )
        [["product_name", "brand", "price"]]
        .head(10)
    )

    log(expensive.to_string(index=False))


# ==========================
# Inventory Analysis
# ==========================

def inventory_analysis(df):

    section("INVENTORY ANALYSIS")

    log()
    log("Inventory Bucket Distribution")
    log()

    log(df["inventory_bucket"].value_counts().to_string())

    log()
    log("Highest Inventory Products")
    log()

    inventory = (
        df.sort_values(
            "inventory",
            ascending=False
        )
        [["product_name", "inventory"]]
        .head(10)
    )

    log(inventory.to_string(index=False))


# ==========================
# Customer Analysis
# ==========================

def customer_analysis(df):

    section("CUSTOMER INSIGHTS")

    log()
    log("Highest Rated Products")
    log()

    top_rated = (
        df.sort_values(
            "rating",
            ascending=False
        )
        [["product_name", "brand", "rating"]]
        .head(10)
    )

    log(top_rated.to_string(index=False))

    log()
    log("Rating Distribution")
    log()

    log(df["rating_bucket"].value_counts().to_string())


# ==========================
# Value Analysis
# ==========================

def value_analysis(df):

    section("VALUE ANALYSIS")

    log()
    log("Top Discounted Products")
    log()

    discounts = (
        df.sort_values(
            "discount_percent",
            ascending=False
        )
        [[
            "product_name",
            "discount_percent",
            "savings"
        ]]
        .head(10)
    )

    log(discounts.to_string(index=False))

    log()
    log("Best Value Products")
    log()

    value = (
        df.sort_values(
            "value_score",
            ascending=False
        )
        [[
            "product_name",
            "brand",
            "value_score"
        ]]
        .head(10)
    )

    log(value.to_string(index=False))


# ==========================
# Business Recommendations
# ==========================

def business_recommendations(df):

    section("BUSINESS RECOMMENDATIONS")

    top_brand = (
        df["brand"]
        .value_counts()
        .idxmax()
    )

    top_segment = (
        df["price_segment"]
        .value_counts()
        .idxmax()
    )

    highest_rating = (
        df["rating"]
        .max()
    )

    avg_discount = (
        df["discount_percent"]
        .mean()
    )

    log(f"• {top_brand} has the largest product assortment.")
    log(f"• {top_segment} products dominate the catalogue.")
    log(f"• Highest product rating observed is {highest_rating:.2f}.")
    log(f"• Average discount across products is {avg_discount:.2f}%.")

    log(
        "• Consider tracking daily price movements for competitive intelligence."
    )

    log(
        "• Build a Power BI dashboard for pricing, assortment and inventory monitoring."
    )

    log("=" * 70)


# ==========================
# Main
# ==========================

def main():

    REPORTS_DIR.mkdir(exist_ok=True)

    REPORT_PATH.write_text("", encoding="utf-8")

    df = load_data()

    executive_summary(df)

    brand_analysis(df)

    pricing_analysis(df)

    inventory_analysis(df)

    customer_analysis(df)

    value_analysis(df)

    business_recommendations(df)


if __name__ == "__main__":

    main()