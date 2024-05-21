from googlesearch import search
import re
from urllib.parse import unquote
import yfinance as yf
import pandas as pd
import os
from functools import cache

YFINANCE_RE = "https://finance.yahoo.com/quote/([^/]+)/.*"
DATA_PATH = "./data/"


class TickerNotFoundError(Exception):
    """
    Raise when the ticker for supplied name is not found.
    """


@cache
def get_ticker(name: str) -> str:
    for result in search(term=f"yfinance {name}", num_results=10):
        if ticker := re.findall(YFINANCE_RE, result):
            return unquote(ticker[0])

    raise TickerNotFoundError


def download_df(tickers: list[str]):
    required_ticker_downloads = {}

    for ticker in tickers:
        cleaned_ticker = re.sub("[^0-9a-zA-Z]+", "", ticker)
        filename = DATA_PATH + cleaned_ticker
        if os.path.isfile(filename):
            continue
        required_ticker_downloads[ticker] = filename

    if not required_ticker_downloads:
        return

    df: pd.DataFrame = yf.download(
        tickers=list(required_ticker_downloads.keys()), progress=False
    )
    df.columns = df.columns.swaplevel(0, 1)

    for ticker, filename in required_ticker_downloads.items():
        ticker_df: pd.DataFrame = df[ticker]
        ticker_df = ticker_df.dropna()
        ticker_df.to_csv(filename)


if __name__ == "__main__":
    print(get_ticker("microsoft"), "MSFT")
    print(get_ticker("nifty 50"), "^NSEI")
    print(get_ticker("tcs"), "TCS.NS")
    print(get_ticker("neuland lab"), "NEULANDLAB.NS")

    names = [
        "microsoft",
        "nifty 50",
        "jubilant pharma",
        "neuland lab",
        "tcs",
        "infosys",
        "adani ports",
        "adani green",
    ]
    tickers = list(map(get_ticker, names))
    print(tickers)
    df = download_df(tickers)
