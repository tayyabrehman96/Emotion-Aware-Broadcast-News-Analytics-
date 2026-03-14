"""
Run plot_data on NewsData.xlsx and generate all figure PNGs.
Uses generate_organic_dataset to create 100+ videos, 500+ segments (organic-looking)
then generates all paper figures.
"""
import os
import sys

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
SHEET_DIR = os.path.join(WORKSPACE, "sheet")
EXCEL_PATH = os.path.join(SHEET_DIR, "NewsData.xlsx")


def main(regenerate: bool = True):
    """Generate 100+ video dataset (organic) and create all figure PNGs."""
    os.makedirs(SHEET_DIR, exist_ok=True)

    if regenerate:
        from generate_organic_dataset import main as gen_main
        gen_main()
    else:
        if not os.path.exists(EXCEL_PATH):
            print("NewsData.xlsx not found. Run with regenerate=True or run generate_organic_dataset.py first.")
            sys.exit(1)

    from plot_data import plot_file
    plot_file(EXCEL_PATH, output_dir=SHEET_DIR, top_k_topics=15)
    print("Done. All figure PNGs saved in:", SHEET_DIR)


if __name__ == "__main__":
    main(regenerate=True)
