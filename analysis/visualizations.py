import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from dataclasses import dataclass

# =====================================
# Project Paths
# =====================================

DATASET_PATH = Path("data/final/analytics_dataset.csv")
CHARTS_DIR = Path("assets/charts")

FIGURE_SIZE = (12, 6)
DPI = 400

# =====================================
# Chart Result
# =====================================

@dataclass
class ChartResult:
    title: str
    filename: str
    insight: str


# =====================================
# Load Dataset
# =====================================

def load_data() -> pd.DataFrame:
    """
    Load the analytics dataset.
    """

    return pd.read_csv(DATASET_PATH)


# =====================================
# Create Output Directory
# =====================================

def create_output_directory() -> None:
    """
    Create the charts directory if it doesn't exist.
    """

    CHARTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


# =====================================
# Save Plot
# =====================================

def save_plot(filename: str) -> None:
    """
    Save the current matplotlib figure.
    """

    plt.tight_layout()

    plt.savefig(
        CHARTS_DIR / filename,
        dpi=DPI,
        bbox_inches="tight"
    )

    plt.close()


# =====================================
# Brand Distribution
# =====================================

def plot_brand_distribution(df: pd.DataFrame) -> ChartResult:
    """
    Generate the Top 15 Brand Distribution chart.
    """

    brand_counts = (
        df["brand"]
        .value_counts()
        .head(15)
        .sort_values()
    )

    plt.figure(figsize=FIGURE_SIZE)

    ax = brand_counts.plot(
        kind="barh",
        width=0.7,
        color="steelblue"
    )

    for container in ax.containers:
        ax.bar_label(
            container,
            fontsize=9,
            padding=3
        )

    plt.title(
        "Top 15 Brands by Product Count",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel(
        "Number of Products",
        fontsize=12
    )

    plt.ylabel(
        "Brand",
        fontsize=12
)

    plt.grid(
        axis="x",
        alpha=0.3
    )

    save_plot(
        "brand_distribution.png"
    )

    top_brand = brand_counts.idxmax()
    top_products = brand_counts.max()

    insight = (
        f"{top_brand} leads the assortment with "
        f"{top_products} products."
    )

    return ChartResult(
        title="Brand Distribution",
        filename="brand_distribution.png",
        insight=insight
    )

# =====================================
# Price Distribution
# =====================================

def plot_price_distribution(df: pd.DataFrame) -> ChartResult:
    """
    Generate the Price Distribution chart.
    """

    plt.figure(figsize=FIGURE_SIZE)

    plt.hist(
        df["price"],
        bins=25,
        edgecolor="black",
        color="slateblue"
    )

    plt.axvline(
        df["price"].mean(),
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Average Price: ₹{df['price'].mean():.0f}"
    )

    plt.legend()

    plt.title(
        "Price Distribution of Products",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel(
        "Price (₹)",
        fontsize=12
    )

    plt.ylabel(
        "Number of Products",
        fontsize=12
    )

    plt.grid(
        axis="y",
        alpha=0.3
    )

    save_plot(
        "price_distribution.png"
    )

    budget_share = (
        (df["price"] < 100).mean() * 100
    )

    median_price = df["price"].median()

    insight = (
        f"{budget_share:.1f}% of products are priced below ₹100 "
        f"(Median: ₹{median_price:.0f})."
    )

    return ChartResult(
        title="Price Distribution",
        filename="price_distribution.png",
        insight=insight
    )

# =====================================
# Inventory Distribution
# =====================================

def plot_inventory_distribution(df: pd.DataFrame) -> ChartResult:
    """
    Generate the Inventory Distribution chart.
    """

    inventory_counts = (
        df["inventory_bucket"]
        .value_counts()
        .reindex(["Low", "Medium", "High"])
    )

    plt.figure(figsize=FIGURE_SIZE)

    ax = inventory_counts.plot(
        kind="bar",
        width=0.6,
        color="darkorange"
    )

    for container in ax.containers:
        ax.bar_label(
            container,
            fontsize=10
        )

    plt.xticks(rotation=0)

    plt.title(
        "Inventory Distribution",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel(
        "Inventory Bucket",
        fontsize=12
    )

    plt.ylabel(
        "Number of Products",
        fontsize=12
    )

    plt.grid(
        axis="y",
        alpha=0.3
    )

    save_plot(
        "inventory_distribution.png"
    )

    dominant_bucket = inventory_counts.idxmax()
    dominant_count = inventory_counts.max()

    percentage = (
        dominant_count / inventory_counts.sum()
    ) * 100

    insight = (
        f"{percentage:.1f}% of products fall into the "
        f"{dominant_bucket} inventory bucket based on the "
        f"defined inventory thresholds."
    )

    return ChartResult(
        title="Inventory Distribution",
        filename="inventory_distribution.png",
        insight=insight
    )

# =====================================
# Rating Distribution
# =====================================

def plot_rating_distribution(df: pd.DataFrame) -> ChartResult:
    """
    Generate the Rating Distribution chart.
    """

    rating_counts = (
        df["rating_bucket"]
        .value_counts()
        .reindex(["Poor", "Good", "Excellent"])
    )

    plt.figure(figsize=FIGURE_SIZE)

    ax = rating_counts.plot(
        kind="bar",
        width=0.6,
        color="forestgreen"
    )

    for container in ax.containers:
        ax.bar_label(
            container,
            fontsize=10
        )

    plt.xticks(rotation=0)

    plt.title(
        "Rating Distribution",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel(
        "Rating Bucket",
        fontsize=12
    )

    plt.ylabel(
        "Number of Products",
        fontsize=12
    )

    plt.grid(
        axis="y",
        alpha=0.3
    )

    save_plot(
        "rating_distribution.png"
    )

    dominant_bucket = rating_counts.idxmax()
    dominant_count = rating_counts.max()

    percentage = (
        dominant_count / rating_counts.sum()
    ) * 100

    insight = (
        f"{percentage:.1f}% of products fall into the "
        f"{dominant_bucket} rating bucket."
    )

    return ChartResult(
        title="Rating Distribution",
        filename="rating_distribution.png",
        insight=insight
    )

# =====================================
# Discount Distribution
# =====================================

def plot_discount_distribution(df: pd.DataFrame) -> ChartResult:
    """
    Generate the Discount Distribution chart.
    """

    plt.figure(figsize=FIGURE_SIZE)

    plt.hist(
        df["discount_percent"],
        bins=20,
        edgecolor="black",
        color="mediumpurple"
    )

    average_discount = df["discount_percent"].mean()

    plt.axvline(
        average_discount,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Average: {average_discount:.1f}%"
    )

    plt.legend()

    plt.title(
        "Discount Distribution",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel(
        "Discount (%)",
        fontsize=12
    )

    plt.ylabel(
        "Number of Products",
        fontsize=12
    )

    plt.grid(
        axis="y",
        alpha=0.3
    )

    save_plot(
        "discount_distribution.png"
    )

    discounted_products = (
        (df["discount_percent"] > 0).sum()
    )

    percentage = (
        discounted_products / len(df)
    ) * 100

    insight = (
        f"{percentage:.1f}% of products offer a discount, "
        f"with an average discount of {average_discount:.1f}%."
    )

    return ChartResult(
        title="Discount Distribution",
        filename="discount_distribution.png",
        insight=insight
    )

# =====================================
# Value Score Distribution
# =====================================

def plot_value_score_distribution(df: pd.DataFrame) -> ChartResult:
    """
    Generate the Value Score Distribution chart.
    """

    plt.figure(figsize=FIGURE_SIZE)

    plt.hist(
        df["value_score"],
        bins=20,
        edgecolor="black",
        color="teal"
    )

    average_score = df["value_score"].mean()

    plt.axvline(
        average_score,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"Average: {average_score:.1f}"
    )

    plt.legend()

    plt.title(
        "Value Score Distribution",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel(
        "Value Score",
        fontsize=12
    )

    plt.ylabel(
        "Number of Products",
        fontsize=12
    )

    plt.grid(
        axis="y",
        alpha=0.3
    )

    save_plot(
        "value_score_distribution.png"
    )

    best_product = df.loc[
        df["value_score"].idxmax()
    ]

    insight = (
        f"{best_product['brand']} offers the highest value-scoring product "
        f"with a score of {best_product['value_score']:.2f}."
    )

    return ChartResult(
        title="Value Score Distribution",
        filename="value_score_distribution.png",
        insight=insight
    )

# =====================================
# Price Segment Distribution
# =====================================

def plot_price_segment_distribution(df: pd.DataFrame) -> ChartResult:
    """
    Generate the Price Segment Distribution chart.
    """

    segment_counts = (
        df["price_segment"]
        .value_counts()
        .reindex(["Budget", "Mid Range", "Premium"])
    )

    plt.figure(figsize=FIGURE_SIZE)

    ax = segment_counts.plot(
        kind="bar",
        width=0.6,
        color="royalblue"
    )

    for container in ax.containers:
        ax.bar_label(
            container,
            fontsize=10
        )

    plt.xticks(rotation=0)

    plt.title(
        "Price Segment Distribution",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel(
        "Price Segment",
        fontsize=12
    )

    plt.ylabel(
        "Number of Products",
        fontsize=12
    )

    plt.grid(
        axis="y",
        alpha=0.3
    )

    save_plot(
        "price_segment_distribution.png"
    )

    budget = segment_counts["Budget"]
    mid = segment_counts["Mid Range"]
    premium = segment_counts["Premium"]

    if abs(mid - budget) <= 5:

        insight = (
            f"The catalogue is nearly evenly split between "
            f"Budget ({budget}) and Mid Range ({mid}) products, "
            f"with {premium} Premium products."
        )

    else:

        dominant_segment = segment_counts.idxmax()

        percentage = (
            segment_counts.max() / segment_counts.sum()
        ) * 100

        insight = (
            f"{percentage:.1f}% of products belong to the "
            f"{dominant_segment} price segment."
        )

    return ChartResult(
        title="Price Segment Distribution",
        filename="price_segment_distribution.png",
        insight=insight
    )

# =====================================
# Generate All Visualizations
# =====================================

def generate_visualizations(df: pd.DataFrame) -> None:
    results = [

        plot_brand_distribution(df),

        plot_price_distribution(df),

        plot_inventory_distribution(df),

        plot_rating_distribution(df),

        plot_discount_distribution(df),

        plot_value_score_distribution(df),

        plot_price_segment_distribution(df)

    ]

    for result in results:

        print(f"✓ {result.title} Chart Generated")

        print(f"  → {result.insight}")

        print()

# =====================================
# Main
# =====================================

def main():

    print("=" * 50)
    print("PRODUCT VISUAL ANALYTICS")
    print("=" * 50)

    df = load_data()

    print("✓ Dataset Loaded")

    if df.empty:
        raise ValueError("Dataset is empty.")

    create_output_directory()

    print("✓ Charts Directory Ready")

    generate_visualizations(df)

    print()

    print("Visual Analytics Completed Successfully.")


if __name__ == "__main__":

    main()