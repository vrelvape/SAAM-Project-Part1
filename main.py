from src.config import (
    REGION,
    LOW_PRICE_THRESHOLD,
    ROLLING_WINDOW_MONTHS,
    MIN_HISTORY_MONTHS,
    STALE_RETURN_THRESHOLD,
)
from src.paths import get_project_paths, ensure_project_directories
from src.loaders import load_raw_datasets
from src.cleaning import (
    prepare_price_data,
    prepare_market_caps_data,
    prepare_carbon_data,
    apply_low_price_filter,
    compute_returns,
    apply_delisting_returns,
)
from src.universe import build_universe_by_year
from src.optimization import compute_mv_weights_by_year
from src.backtest import run_mv_backtest
from src.benchmark import run_vw_backtest
from src.reporting import (
    build_performance_table,
    compute_cumulative_series,
    plot_cumulative_performance,
    export_part1_outputs,
    fill_part1_excel_template,
)



def main():
    # Paths
    paths = get_project_paths()
    ensure_project_directories(paths)

    # Load raw datasets
    static, prices_raw, market_caps_raw, carbon_raw = load_raw_datasets(paths["DATA_RAW"])

    # Regional universe
    em_firms = static[static["Region"] == REGION].copy()
    em_isins = em_firms["ISIN"].tolist()

    # Prepare datasets
    price_data = prepare_price_data(prices_raw, em_isins)
    price_data = apply_low_price_filter(price_data, LOW_PRICE_THRESHOLD)

    market_caps_data = prepare_market_caps_data(market_caps_raw, em_isins)
    carbon_data = prepare_carbon_data(carbon_raw, em_isins)

    # Returns
    returns_matrix = compute_returns(price_data)
    returns_matrix = apply_delisting_returns(price_data, returns_matrix)

    # Dynamic universe
    rebalance_years = list(range(2014, 2026))

    universe_by_year = build_universe_by_year(
        returns_matrix=returns_matrix,
        price_data=price_data,
        carbon_data=carbon_data,
        rebalance_years=rebalance_years,
        rolling_window_months=ROLLING_WINDOW_MONTHS,
        min_history_months=MIN_HISTORY_MONTHS,
        stale_return_threshold=STALE_RETURN_THRESHOLD,
    )

    # Minimum variance weights
    mv_weights_by_year = compute_mv_weights_by_year(
        returns_matrix=returns_matrix,
        universe_by_year=universe_by_year,
        rebalance_years=rebalance_years,
        rolling_window_months=ROLLING_WINDOW_MONTHS,
    )

    # Backtests
    mv_returns_by_year, mv_returns_oos = run_mv_backtest(
        returns_matrix=returns_matrix,
        mv_weights_by_year=mv_weights_by_year,
        rebalance_years=rebalance_years,
    )

    vw_returns_by_year, vw_returns_oos = run_vw_backtest(
        returns_matrix=returns_matrix,
        market_caps_data=market_caps_data,
        universe_by_year=universe_by_year,
        rebalance_years=rebalance_years,
    )

    # Reporting
    performance = build_performance_table(
        mv_returns_oos=mv_returns_oos,
        vw_returns_oos=vw_returns_oos,
    )

    mv_cumulative, vw_cumulative = compute_cumulative_series(
        mv_returns_oos=mv_returns_oos,
        vw_returns_oos=vw_returns_oos,
    )

    figure_path = plot_cumulative_performance(
        mv_cumulative=mv_cumulative,
        vw_cumulative=vw_cumulative,
        figures_dir=paths["FIGURES_DIR"],
        show_plot=False,
    )

    exported_paths = export_part1_outputs(
        mv_returns_oos=mv_returns_oos,
        vw_returns_oos=vw_returns_oos,
        performance=performance,
        tables_dir=paths["TABLES_DIR"],
    )

    print("Part I pipeline completed successfully.")
    print("Figure saved at:", figure_path)
    print("Exported files:")
    for name, path in exported_paths.items():
        print(f"  {name}: {path}")

    filled_template_path = fill_part1_excel_template(
        templates_dir=paths["TEMPLATES_DIR"],
        excel_dir=paths["EXCEL_DIR"],
        figures_dir=paths["FIGURES_DIR"],
        mv_returns_oos=mv_returns_oos,
        vw_returns_oos=vw_returns_oos,
    )

    print("Filled Excel template saved at:", filled_template_path)

if __name__ == "__main__":
    main()