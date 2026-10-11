# E-commerce Customer Value Analysis

A compact SQL and Python project for exploring customer purchasing behavior.
It builds a local SQLite database, ranks customers by recorded order spend,
and visualizes customer value tiers and their geographic distribution.

> **This is a demonstration project using synthetic data.** The setup script
> creates 100 mock customers and 100 mock orders with a fixed random seed.
> The records do not represent real customers or transactions.

## Project overview

The analysis uses SQLite window functions and Python visualizations to:

- Aggregate each customer’s recorded order spend and order count.
- Assign customers to **High**, **Medium**, or **Low** spend tiers using
  `NTILE(3)`.
- Compare total spend and customer counts across tiers.
- Explore customer spend by city and state with an interactive map.

The spend tiers are descriptive rankings within this sample, **not a forecast
of customer lifetime value**. The SQL sums all recorded orders, regardless of
status; it does not estimate future purchases, discount cash flows, or exclude
cancelled orders.

## Tech stack

- **Python** for database setup and analysis
- **SQLite** for storing customers and orders
- **SQL** for customer-level aggregation and spend-tier ranking
- **pandas** for querying and shaping analysis data
- **Matplotlib** and **Seaborn** for visualizations
- **Plotly** and **GeoPy** for the interactive customer map

## Run the analysis

Use Python 3.10 or newer. From the project root, create an environment and
install the core dependencies:

```bash
python -m venv .venv
```

Activate it, then install packages:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

```bash
# macOS or Linux
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Create or reset the sample database:

```bash
python src/setup_db.py
```

Open `notebooks/customer_analysis.ipynb` in Jupyter or VS Code and run its
cells from top to bottom. The notebook reads `queries/clv_analysis.sql`,
creates the spend-tier chart, and displays an interactive map.

### Interactive map dependencies

The map cell additionally requires `geopy` and `plotly`:

```bash
python -m pip install geopy plotly
```

It geocodes the sample city/state locations using OpenStreetMap's Nominatim
service. An internet connection is required, and geocoding requests are
rate-limited.

## Repository structure

```text
.
├── data/
│   └── store.db                   # Generated SQLite database
├── notebooks/
│   ├── customer_analysis.ipynb    # Analysis and visualizations
│   └── clv_distribution.png       # Saved spend-tier chart
├── queries/
│   └── clv_analysis.sql           # Customer spend aggregation and ranking
├── src/
│   └── setup_db.py                # Creates and seeds the sample database
└── requirements.txt               # Core Python dependencies
```

## Reproducibility

The database setup uses a fixed random seed, so rebuilding it produces the
same mock customer and order data. Running `src/setup_db.py` replaces the
existing customer and order rows in `data/store.db`.
