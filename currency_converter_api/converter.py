from os import getenv

import aiohttp
import requests
from fastapi import HTTPException

ALPHAVANTAGE_APIKEY = getenv("ALPHAVANTAGE_APIKEY")


def sync_converter(from_curency: str, to_currency: str, price: float) -> dict:
    url = (
        "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&"
        f"from_currency={from_curency}&to_currency={to_currency}"
        f"&apikey={ALPHAVANTAGE_APIKEY}"
    )

    try:
        response = requests.get(url)
    except Exception as error:
        raise HTTPException(status_code=400, detail=error)

    data = response.json()

    if "Realtime Currency Exchange Rate" not in data:
        raise HTTPException(
            status_code=400,
            detail=f"Realtime Currency Exchange Rate not in response. Data: {data}",
        )

    exchange_rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])

    return {to_currency: price * exchange_rate}


async def async_converter(from_curency: str, to_currency: str, price: float) -> dict:
    url = (
        "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&"
        f"from_currency={from_curency}&to_currency={to_currency}"
        f"&apikey={ALPHAVANTAGE_APIKEY}"
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                data = await response.json()
    except Exception as error:
        raise HTTPException(status_code=400, detail=error)

    if "Realtime Currency Exchange Rate" not in data:
        raise HTTPException(
            status_code=400,
            detail=f"Realtime Currency Exchange Rate not in response. Data: {data}",
        )

    exchange_rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])

    return {to_currency: price * exchange_rate}
