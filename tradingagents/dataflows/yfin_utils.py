# gets data/stats

import yfinance as yf
from typing import Annotated, Callable, Any, Optional
from pandas import DataFrame
import pandas as pd
from functools import wraps

from .utils import save_output, SavePathType, decorate_all_methods


def init_ticker(func: Callable) -> Callable:
    """Decorator to initialize yf.Ticker and pass it to the function."""

    @wraps(func)
    def wrapper(symbol: Annotated[str, "ticker symbol"], *args, **kwargs) -> Any:
        ticker = yf.Ticker(symbol)
        return func(ticker, *args, **kwargs)

    return wrapper


@decorate_all_methods(init_ticker)
class YFinanceUtils:

    def get_stock_data(
        symbol: Annotated[str, "ticker symbol"],
        start_date: Annotated[
            str, "start date for retrieving stock price data, YYYY-mm-dd"
        ],
        end_date: Annotated[
            str, "end date for retrieving stock price data, YYYY-mm-dd"
        ],
        save_path: SavePathType = None,
    ) -> DataFrame:
        """retrieve stock price data for designated ticker symbol"""
        ticker = symbol
        # add one day to the end_date so that the data range is inclusive
        end_date = pd.to_datetime(end_date) + pd.DateOffset(days=1)
        end_date = end_date.strftime("%Y-%m-%d")
        stock_data = ticker.history(start=start_date, end=end_date)
        # save_output(stock_data, f"Stock data for {ticker.ticker}", save_path)
        return stock_data

    def get_stock_info(
        symbol: Annotated[str, "ticker symbol"],
    ) -> dict:
        """Fetches and returns latest stock information."""
        ticker = symbol
        stock_info = ticker.info
        return stock_info

    def get_company_info(
        symbol: Annotated[str, "ticker symbol"],
        save_path: Optional[str] = None,
    ) -> DataFrame:
        """Fetches and returns company information as a DataFrame."""
        ticker = symbol
        info = ticker.info
        company_info = {
            "Company Name": info.get("shortName", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "Country": info.get("country", "N/A"),
            "Website": info.get("website", "N/A"),
        }
        company_info_df = DataFrame([company_info])
        if save_path:
            company_info_df.to_csv(save_path)
            print(f"Company info for {ticker.ticker} saved to {save_path}")
        return company_info_df

    def get_stock_dividends(
        symbol: Annotated[str, "ticker symbol"],
        save_path: Optional[str] = None,
    ) -> DataFrame:
        """Fetches and returns the latest dividends data as a DataFrame."""
        ticker = symbol
        dividends = ticker.dividends
        if save_path:
            dividends.to_csv(save_path)
            print(f"Dividends for {ticker.ticker} saved to {save_path}")
        return dividends

    def get_income_stmt(symbol: Annotated[str, "ticker symbol"]) -> DataFrame:
        """Fetches and returns the latest income statement of the company as a DataFrame."""
        ticker = symbol
        income_stmt = ticker.financials
        return income_stmt

    def get_balance_sheet(symbol: Annotated[str, "ticker symbol"]) -> DataFrame:
        """Fetches and returns the latest balance sheet of the company as a DataFrame."""
        ticker = symbol
        balance_sheet = ticker.balance_sheet
        return balance_sheet

    def get_cash_flow(symbol: Annotated[str, "ticker symbol"]) -> DataFrame:
        """Fetches and returns the latest cash flow statement of the company as a DataFrame."""
        ticker = symbol
        cash_flow = ticker.cashflow
        return cash_flow

    def get_analyst_recommendations(symbol: Annotated[str, "ticker symbol"]) -> tuple:
        """Fetches the latest analyst recommendations and returns the most common recommendation and its count."""
        ticker = symbol
        recommendations = ticker.recommendations
        if recommendations.empty:
            return None, 0  # No recommendations available

        # Assuming 'period' column exists and needs to be excluded
        row_0 = recommendations.iloc[0, 1:]  # Exclude 'period' column if necessary

        # Find the maximum voting result
        max_votes = row_0.max()
        majority_voting_result = row_0[row_0 == max_votes].index.tolist()

        return majority_voting_result[0], max_votes

    def get_yfin_news(
        ticker: Annotated[yf.Ticker, "yfinance Ticker object"],
    ) -> str:
        """
        Retrieve news about a company.
        Args:
            ticker (yf.Ticker): yfinance Ticker object for the company you are interested in
        Returns:
            str: containing the news of the company
        """
        news = ticker.news
        combined_result = ""
        for entry in news:
            current_news = (
                "### " + entry["title"] + f" ({pd.to_datetime(entry['providerPublishTime'], unit='s')})" + "\n" + entry.get('summary', 'No summary available.')
            )
            combined_result += current_news + "\n\n"
        return f"## {ticker.ticker} News:\n" + str(combined_result)

    def get_yfin_insider_transactions(
        ticker: Annotated[yf.Ticker, "yfinance Ticker object"],
    ) -> str:
        """
        Retrieve insider transcaction information about a company.
        Args:
            ticker (yf.Ticker): yfinance Ticker object for the company
        Returns:
            str: a report of the company's insider transaction/trading informtaion
        """
        insider_transactions = ticker.insider_transactions
        if insider_transactions.empty:
            return ""
        return f"## {ticker.ticker} insider transactions:\n" + str(insider_transactions)


if __name__ == "__main__":
    # Example usage:
    ticker_symbol = "AAPL"
    start_date = "2023-01-01"
    end_date = "2023-12-31"

    # Get stock data
    stock_data = YFinanceUtils.get_stock_data(ticker_symbol, start_date, end_date)
    print("Stock Data:")
    print(stock_data.head())

    # Get company info
    company_info = YFinanceUtils.get_company_info(ticker_symbol)
    print("\nCompany Info:")
    print(company_info)

    # Get dividends
    dividends = YFinanceUtils.get_stock_dividends(ticker_symbol)
    print("\nDividends:")
    print(dividends.head())

    # Get income statement
    income_stmt = YFinanceUtils.get_income_stmt(ticker_symbol)
    print("\nIncome Statement:")
    print(income_stmt.head())

    # Get balance sheet
    balance_sheet = YFinanceUtils.get_balance_sheet(ticker_symbol)
    print("\nBalance Sheet:")
    print(balance_sheet.head())

    # Get cash flow
    cash_flow = YFinanceUtils.get_cash_flow(ticker_symbol)
    print("\nCash Flow:")
    print(cash_flow.head())

    # Get analyst recommendations
    recommendation, votes = YFinanceUtils.get_analyst_recommendations(ticker_symbol)
    print(f"\nAnalyst Recommendation: {recommendation} ({votes} votes)")