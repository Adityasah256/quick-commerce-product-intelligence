import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# =====================================
# Project Paths
# =====================================

DATASET_PATH = Path("data/final/analytics_dataset.csv")
CHARTS_DIR = Path("assets/charts")


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
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# =====================================
# Main
# =====================================

def main():

    load_data()

    create_output_directory()

    print("Visual Analytics Pipeline Initialized")


if __name__ == "__main__":

    main()