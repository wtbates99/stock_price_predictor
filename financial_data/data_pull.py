import pandas as pd
import yfinance as yf


def fetch_write_financial_data(conn):
    table = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
    tickers = table[~table["Symbol"].str.contains(r"\.")]["Symbol"].tolist()
    batch_size = 503

    def quant_data(tickers) -> pd.DataFrame:
        all_data = []
        for i in range(0, len(tickers), batch_size):
            batch = tickers[i : i + batch_size]
            data = yf.download(
                batch, interval="1d", group_by="ticker", auto_adjust=True
            )
            all_data.append(data)
        concatenated_data = pd.concat(all_data)
        quant_data = (
            concatenated_data.stack(level=0)
            .reset_index()
            .rename(columns={"level_1": "Ticker"})
        )

        quant_data.to_sql("stock_data", conn, if_exists="replace", index=False)

    def qual_data(tickers) -> pd.DataFrame:
        stock_information = []
        for i in range(0, len(tickers), batch_size):
            batch = tickers[i : i + batch_size]
            for ticker in batch:
                stock_info = yf.Ticker(ticker).info
                stock_data = {
                    "Ticker": ticker,
                    "Sector": stock_info.get("sector", "N/A"),
                    "Subsector": stock_info.get("industry", "N/A"),
                    "FullName": stock_info.get("longName", "N/A"),
                    "MarketCap": stock_info.get("marketCap", "N/A"),
                    "Country": stock_info.get("country", "N/A"),
                    "Website": stock_info.get("website", "N/A"),
                    "Description": stock_info.get("longBusinessSummary", "N/A"),
                    "CEO": stock_info.get("ceo", "N/A"),
                    "Employees": stock_info.get("fullTimeEmployees", "N/A"),
                    "City": stock_info.get("city", "N/A"),
                    "State": stock_info.get("state", "N/A"),
                    "Zip": stock_info.get("zip", "N/A"),
                    "Address": stock_info.get("address1", "N/A"),
                    "Phone": stock_info.get("phone", "N/A"),
                    "Exchange": stock_info.get("exchange", "N/A"),
                    "Currency": stock_info.get("currency", "N/A"),
                    "QuoteType": stock_info.get("quoteType", "N/A"),
                    "ShortName": stock_info.get("shortName", "N/A"),
                    "Price": stock_info.get("regularMarketPrice", "N/A"),
                    "52WeekHigh": stock_info.get("fiftyTwoWeekHigh", "N/A"),
                    "52WeekLow": stock_info.get("fiftyTwoWeekLow", "N/A"),
                    "DividendRate": stock_info.get("dividendRate", "N/A"),
                    "DividendYield": stock_info.get("dividendYield", "N/A"),
                    "PayoutRatio": stock_info.get("payoutRatio", "N/A"),
                    "Beta": stock_info.get("beta", "N/A"),
                    "PE": stock_info.get("trailingPE", "N/A"),
                    "EPS": stock_info.get("trailingEps", "N/A"),
                    "Revenue": stock_info.get("totalRevenue", "N/A"),
                    "GrossProfit": stock_info.get("grossProfits", "N/A"),
                    "FreeCashFlow": stock_info.get("freeCashflow", "N/A"),
                }
                stock_information.append(stock_data)
        qual_data = pd.DataFrame(stock_information)
        qual_data.to_sql("stock_information", conn, if_exists="replace", index=False)

    qual_data = qual_data(tickers)
    quant_data = quant_data(tickers)
