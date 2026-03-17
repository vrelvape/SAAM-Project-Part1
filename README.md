# SAAM Project – Part I

This repository contains the full implementation of **Part I** of the SAAM project on portfolio allocation.

The objective of this project is to construct a **long-only minimum variance portfolio** using monthly equity data and to compare its out-of-sample performance with a **value-weighted benchmark portfolio** over the period **2014–2025**.

The project is implemented using a modular Python pipeline located in the `src` directory, and a final notebook that reproduces the main steps and outputs.

---

## Repository Structure

data_raw/              raw input datasets provided for the project  
data_processed/        reserved for intermediate datasets (not used in Part I)  
notebooks/             final notebook reproducing the analysis  
outputs/  
    tables/            exported CSV tables  
    figures/           exported figures  
    excel/             filled Excel template for Part I  
resources/  
    templates/         official Excel template  
src/                   modular pipeline (cleaning, universe, optimization, backtest, reporting)  
main.py                script running the full Part I pipeline  
requirements.txt       Python dependencies  
README.md              project documentation  

---

## Main Files

- Notebook: `notebooks/SAAM_peoject_part1_analysis.ipynb`  
- Pipeline script: `main.py`

---

## How to Run the Project

### 1. Install dependencies

pip install -r requirements.txt

or:

pip3 install -r requirements.txt

---

### 2. Run the full pipeline

From the root of the repository:

python3 main.py

This script performs the full Part I pipeline:

- loads the raw datasets
- prepares price, market capitalization, and carbon data
- computes monthly returns and applies delisting adjustments
- builds the dynamic investment universe
- computes minimum variance portfolio weights
- runs the minimum variance and value-weighted backtests
- generates performance statistics and cumulative returns
- exports CSV tables and figures
- fills the official Excel template for Part I

---

### 3. Run the notebook

Open:

notebooks/SAAM_peoject_part1_analysis.ipynb

Then run all cells from top to bottom.

The notebook reproduces the main steps of the analysis and generates the same outputs as the pipeline.

---

## Output Files

After execution, the main outputs are available in the `outputs/` folder:

### outputs/tables/
- mv_returns_oos.csv  
- vw_returns_oos.csv  
- portfolio_performance_summary.csv  

### outputs/figures/
- cumulative_portfolio_performance.png  

### outputs/excel/
- Part_I_template_filled.xlsx  

---

## Notes

- All paths are handled automatically; no hard-coded local paths are required.
- The project has been tested in a clean environment (Codespaces).
- The data_processed/ folder is included for potential intermediate datasets, although no processed datasets are saved to disk in Part I.
- The implementation follows a modular structure to improve clarity, reproducibility, and maintainability.