import pandas as pd

from economist import te_bar, te_boxplot, te_line


def main():

    # Wide time‑series data for te_line
    df_wide = pd.DataFrame(
        {
            "year": [2018, 2019, 2020, 2021, 2022],
            "series_a": [10, 12, 15, 14, 18],
            "series_b": [8, 9, 11, 13, 16],
        }
    )

    # Long data for te_bar
    df_long = pd.DataFrame(
        {
            "sector": ["Tech", "Finance", "Health", "Energy", "Industry"] * 2,
            "series": ["2019–2021"] * 5 + ["2022–2024"] * 5,
            "value": [5.2, 3.1, 4.7, 2.9, 3.8, 3.4, 2.0, 3.9, 1.8, 2.6],
        }
    )

    # Long data for te_boxplot
    df_box = pd.DataFrame(
        {
            "group": ["G1"] * 10 + ["G2"] * 10,
            "value": [
                1,
                2,
                3,
                4,
                5,
                2,
                3,
                4,
                5,
                6,
                1.5,
                2.5,
                3.5,
                4.5,
                5.5,
                2.5,
                3.5,
                4.5,
                5.5,
                6.5,
            ],
        }
    )

    # ── Build charts -----------------------------------------------------------

    # Line chart from wide data (te_line will reshape internally)
    p_line = te_line(
        df=df_wide,
        x_var_name="year",
        x_axis_title="Year",
        y_axis_title="Value",
        chart_title="Example line chart",
        chart_subtitle="Wide data automatically converted to long",
        cap="Source: synthetic data",
        breaks=range(2018, 2023),
    )

    # Grouped bar chart from long data
    p_bar = te_bar(
        df=df_long,
        x_var_name="sector",
        x_axis_title="Sector",
        y_axis_title="Return (%)",
        chart_title="Average annual returns by sector",
        chart_subtitle="Two periods, long-format input",
        cap="Source: synthetic data",
        # y_var_names is not needed here because df_long is already long
    )

    # Box‑and‑whisker plot
    p_box = te_boxplot(
        df=df_box,
        x_var_name="group",
        y_var_name="value",
        x_axis_title="Group",
        y_axis_title="Score",
        chart_title="Example boxplot",
        chart_subtitle="Two groups, synthetic data",
        cap="Source: synthetic data",
    )

    # ── Save outputs -----------------------------------------------------------

    # Option 1: save each chart separately
    p_line.save("example_line.png", width=8, height=5, dpi=150)
    p_bar.save("example_bar.png", width=8, height=5, dpi=150)
    p_box.save("example_box.png", width=8, height=5, dpi=150)

    df = pd.read_csv("test_data/m.csv")

    tl = te_line(
        df=df,
        x_var_name="YEAR",
        x_axis_title="Year",
        y_axis_title="Quantity",
        chart_title="Quantity in the Loop, 2000–2025",
        chart_subtitle="All available data on the hood, 2000–2025",
        cap="Source: The Universe",
        breaks=range(2002, 2026, 4),
    )
    tl.save("example_line_series.png", width=8, height=5, dpi=150)


if __name__ == "__main__":
    main()
