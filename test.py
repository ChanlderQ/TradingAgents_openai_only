import os

# IMPORTANT: Set your OpenAI API key here
# For better security, consider loading this from a .env file or system environment
os.environ["OPENAI_API_KEY"] = "your api key"

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Initialize the trading graph. Using debug=True provides more detailed output.
ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# Define the ticker and date for the analysis
ticker = "MSFT"
trade_date = "2025-07-04"

print(f"Running trading agent analysis for {ticker} on {trade_date}...")

# Run the analysis to get a trading decision
final_state, decision = ta.propagate(ticker, trade_date)

print("\n--- Trading Decision ---")
print(decision)