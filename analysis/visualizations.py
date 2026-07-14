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

    brand_counts.plot(
        kind="barh",
        width=0.7
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
        edgecolor="black"
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
# Generate All Visualizations
# =====================================

def generate_visualizations(df: pd.DataFrame) -> ChartResult:
    results = [

        plot_brand_distribution(df),

        plot_price_distribution(df)

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