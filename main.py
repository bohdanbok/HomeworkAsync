import aiohttp
import asyncio
from datetime import date, timedelta


async def fetch_exchange_rates(days):

    base_url = "https://api.privatbank.ua/p24api/exchange_rates"
    results = []

    async with aiohttp.ClientSession() as session:
        for day in days:
            print(day.strftime('%d.%m.%Y'))
            async with session.get(f"{base_url}?json&date={day.strftime('%d.%m.%Y')}", ssl=False) as response:
                if response.status == 200:
                    data = await response.json()

                    rates = {f'{day}': {
                        "EUR": {
                            "sale": data["exchangeRate"][8]['saleRateNB'],
                            "purchase": data["exchangeRate"][8]['purchaseRate'],
                        },
                        "USD": {
                            "sale": data["exchangeRate"][-3]['saleRateNB'],
                            "purchase": data["exchangeRate"][-3]['purchaseRate'],
                        },
                    }}

                    results.append(rates)
                else:
                    print(f"Error fetching data for day {day}: {response.status}")

    return results

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python main.py <number_of_days>")
        sys.exit(1)

    try:
        days = int(sys.argv[1])
        if days < 1 or days > 10:
            raise ValueError("Number of days must be between 1 and 10.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        sys.exit(1)

    date = date.today()

    info_days = int(sys.argv[1])
    days = [date - timedelta(days=i) for i in range(info_days)]

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(fetch_exchange_rates(days))
    print(results)
