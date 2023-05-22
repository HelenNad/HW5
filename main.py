import asyncio
import logging
import platform
import sys
from datetime import datetime, timedelta
from time import time

import aiohttp


def search_money(result):
    date_value = {"USD": None, "EUR": None}
    list_value = []

    for exchange in dict(result).values():
        if isinstance(exchange, list):
            list_value.extend(exchange)

    for el in list_value:
        if el["currency"] == "USD":
            dollar = {'sale': el["saleRate"], 'purchase': el["purchaseRate"]}
            date_value["USD"] = dollar

        elif el["currency"] == "EUR":
            euro = {'sale': el["saleRate"], 'purchase': el["purchaseRate"]}
            date_value["EUR"] = euro

    dict_value = {result["date"]: date_value}
    return dict_value


async def main():
    lv = []
    async with aiohttp.ClientSession() as sess:
        day_now = datetime.now()
        four_days_interval = timedelta(days=1)

        for i in range(0, int(message)):
            async with sess.get('https://api.privatbank.ua/p24api/exchange_rates?date=' + day_now.strftime("%d.%m.%Y"))\
                    as response:
                if response.status == 200:
                    result = await response.json()

                else:
                    logging.error(f"Error status {response.status}")
            lv.append(search_money(result))
            day_now = day_now - four_days_interval
            i += 1
    return lv


if __name__ == "__main__":
    try:
        message = sys.argv[1]
        start = time()
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        if 0 < int(message) < 11:
            r = asyncio.run(main())
            print(r)
        else:
            print("Enter the number of days for which you want to view the exchange rate")
        print(time() - start)
    except ValueError:
        print("Enter the number of days for which you want to view the exchange rate")
