from datetime import timedelta

import pandas as pd
import requests
import yfinance as yf

from helpers.config import DISCORD_AUTH, DISCORD_URL


def data_retrieval(days_lookback: int, ticker: str, interval: str):
    today = pd.to_datetime("today").normalize()
    start = today - pd.tseries.offsets.BDay(days_lookback)

    # Downloading correct data from yfinance
    df = yf.download(ticker, start=start, interval=interval, prepost=False)
    df = df.xs(ticker, axis=1, level="Ticker")
    df.index = df.index.tz_convert("America/Chicago")

    return df


def date_transform(df):
    # Split Datetime into Date, Time
    # Extract Date
    df['Date'] = df.index.strftime('%Y-%m-%d')
    # Extract Time without timezone
    df['Time'] = df.index.strftime('%H:%M:%S')

    # Drop timezone
    df = df.reset_index(drop=True)

    # Delete all rows with Time between 15:15 & 08:15
    # Convert Time column to datetime.time for proper comparison
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time

    # Define the start and end time boundaries
    start_time = pd.to_datetime("15:15:00", format='%H:%M:%S').time()
    end_time = pd.to_datetime("08:15:00", format='%H:%M:%S').time()

    # Keep only rows where Time is NOT between 15:15:00 and 08:15:00
    df = df[~((df['Time'] >= start_time) | (df['Time'] <= end_time))]

    # Reset index after filtering (optional)
    df = df.reset_index(drop=True)

    return df


def pivots(df, logger):
    max_high = df['High'].max()

    min_low = df['Low'].min()

    latest_close = df['Close'].iloc[-1]

    ran = max_high - min_low

    pp = round((max_high + min_low + latest_close) / 3, 2)

    logger.info(f"Pivot: {pp}")

    r1 = round(2 * pp - min_low, 2)

    logger.info(f"R1: {r1}")

    r2 = round(pp + ran, 2)

    logger.info(f"R2: {r2}")

    r3 = round(pp + ran * 2, 2)

    logger.info(f"R3: {r3}")

    s1 = round(2 * pp - max_high, 2)

    logger.info(f"S1: {s1}")

    s2 = round(pp - ran, 2)

    logger.info(f"S2: {s2}")

    s3 = round(pp - ran * 2, 2)

    logger.info(f"S3: {s3}")

    return pp, r1, r2, r3, s1, s2, s3


def curr_price(ticker: str):
    # Downloading Data
    curr_price = yf.download(
        ticker, start=pd.to_datetime("today") - timedelta(1), )

    # Reformatting Multi-Index
    curr_price = curr_price.xs(ticker, axis=1, level='Ticker')

    # Retrieving Last Price
    last = curr_price[['Close']].iloc[-1]
    last = last.iloc[0]

    return last


def send_discord_msg(content: str):  # , logger):
    """Sending Discord Messages

    This will send a message to the proper Discord channel using
    my username.

    Args:
        content (str): This is what the message will be inside the Discord channel.
    """
    # Send message to Discord with order info
    payload1 = {
        "content": content}

    try:
        res = requests.post(DISCORD_URL, payload1, headers=DISCORD_AUTH)
    except Exception as e:
        # logger.error("\n***** ERROR Sending Discord Msg *****")
        # logger.error(f"{e}\n")
        print((f"{e}\n"))
