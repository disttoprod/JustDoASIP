from functools import cache
import os
import re

from googlesearch import search
from urllib.parse import unquote
import numpy as np
import pandas as pd
import yfinance as yf

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


@cache
def get_filename_for_ticker(ticker: str) -> str:
    cleaned_ticker = re.sub("[^0-9a-zA-Z]+", "", ticker)
    return DATA_PATH + cleaned_ticker


def download_df(tickers: list[str]):
    # TODO: Add action to force update the file; since data might be outdated!
    required_ticker_downloads = {}

    for ticker in tickers:
        filename = get_filename_for_ticker(ticker)
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


@cache
def get_df(ticker: str) -> pd.DataFrame:
    filename = get_filename_for_ticker(ticker)
    return pd.read_csv(filename, index_col="Date")


@cache
def get_row(ticker: str, date: str) -> pd.Series:
    df = get_df(ticker)
    # Make sure the latest date accessed is a trading date + is in bounds.
    i = min(np.searchsorted(df.index, date), len(df.index))
    return df.iloc[i]


def get_buy_price(ticker: str, date: str) -> float:
    return get_row(ticker, date)["High"]


def get_sell_price(ticker: str, date: str) -> float:
    return get_row(ticker, date)["Low"]


if __name__ == "__main__":
    print(get_ticker("microsoft"), "MSFT")
    print(get_ticker("nifty 50"), "^NSEI")
    print(get_ticker("tcs"), "TCS.NS")

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

    print(get_row("TCS.NS", "2024-05-21"))
    print(get_buy_price("TCS.NS", "2024-05-18"))
    print(get_sell_price("TCS.NS", "2024-05-17"))
