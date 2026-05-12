# economist.py

## Overview
The `economist` package creates publication-ready charts in The Economist style using [plotnine](https://plotnine.readthedocs.io/), a Python implementation of ggplot2. It supports line, bar, and boxplot charts with flexible wide or long data formats.[file:1]

Key features include a custom theme with Economist colors (light blue background, white horizontal grids), automatic data reshaping, and color palettes from the publication.[file:1]

## Requirement
- Python 3.14+
- `plotnine`
- `pandas`
- `numpy`

Install via pip (after packaging):
```
pip install economist
```
Font "Roboto" is recommended for exact styling; falls back to defaults.[file:1]

## Installation
For development:
```
pip install -r requirements.txt  # plotnine, pandas, numpy
```
The package exposes `theme_economist`, `te_line`, `te_bar`, `te_boxplot` via `__all__`.[file:1]

## Usage

### Line Charts
```python
import pandas as pd
from economist import te_line

df = pd.DataFrame({
    'year': [2020, 2021, 2022],
    'sales_a': [100, 120, 140],
    'sales_b': [90, 110, 130]
})

chart = te_line(
    df, x_var_name='year',
    x_axis_title='Year', y_axis_title='Sales',
    chart_title='Sales Growth', chart_subtitle='Two series',
    cap='Source: Example', y_var_names=['sales_a', 'sales_b']
)
chart.save('line_chart.png', width=10, height=6, dpi=300)
```
Handles wide data automatically.[file:1]

### Bar Charts
```python
from economist import te_bar

chart = te_bar(
    df, x_var_name='year',
    x_axis_title='Year', y_axis_title='Sales',
    chart_title='Sales by Year', chart_subtitle='Grouped',
    cap='Source: Example', y_var_names=['sales_a', 'sales_b']
)
```
Supports dodged bars for groups.[file:1]

### Boxplots
```python
from economist import te_boxplot

df_long = pd.DataFrame({
    'category': ['A']*50 + ['B']*50,
    'value': list(range(50)) + list(range(40, 90))
})

chart = te_boxplot(
    df_long, x_var_name='category', y_var_name='value',
    x_axis_title='Category', y_axis_title='Value',
    chart_title='Distribution', chart_subtitle='By group',
    cap='Source: Example'
)
```
Adds jitter for individual points.[file:1]

## Functions

| Function     | Input Data | Key Parameters                          | Output                  |
|--------------|------------|-----------------------------------------|-------------------------|
| `te_line`    | Wide/Long  | `df`, `x_var_name`, titles, `y_var_names` (wide) | Line + points plot [file:1] |
| `te_bar`     | Wide/Long  | Same as above                           | Dodged bar plot [file:1] |
| `te_boxplot` | Long       | `df`, `x_var_name`, `y_var_name`, titles | Boxplot + jitter [file:1] |
| `theme_economist` | None | -                                       | Theme object [file:1] |

All use `ECON_PALETTE` for colors: #006BA2, #E3120B, etc.[file:1]

## Customization
Apply theme manually:
```python
from plotnine import ggplot, aes, geom_line
from economist import theme_economist

p = (ggplot(df, aes('x', 'y')) + geom_line() + theme_economist())
```

## License
MIT License - Diego Carvalho - d.carvalho@ieee.org

### Permissions
You can freely use, copy, modify, merge, publish, distribute, sublicense, or sell the software commercially or privately, including in proprietary projects.

### Requirements
Include the original copyright notice and full license text in all copies or substantial portions of the software.

### Limitations
No warranties; software is "as is." Authors cannot be held liable for damages, claims, or issues from use.
