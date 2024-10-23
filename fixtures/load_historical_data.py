# assuming the historical data loading is using csv file to load data to db
# there is load_historical_data.csv file which is used here to load data
# format for the csv file is already in the csv file
# also assuming that we have currency data already in the db, and the id start from 1 to 4
import asyncio
import aiofiles
import datetime
import pandas as pd
import asyncpg

from pathlib import Path
from io import StringIO


async def connect_db(db_config):
    conn = await asyncpg.connect(**db_config)
    return conn


async def main(db_config):
    base_dir = Path(__file__).resolve().parent.parent
    csv_file = "{}/{}".format(base_dir, "/fixtures/load_historical_data.csv")
    # Read the CSV file asynchronously
    async with aiofiles.open(csv_file, mode="r") as file:
        # Load CSV into a pandas DataFrame
        contents = await file.read()
        df = pd.read_csv(StringIO(contents))

        tasks = []
        insert_statement = "INSERT INTO exchange_rate_currencyexchangerate (id, is_deleted, valuation_date, rate_value, exchanged_currency_id, source_currency_id) VALUES (%s, %s, %s, %s, %s, %s)"

        for index, row in df.iterrows():
            cursor = await connect_db(db_config)
            valuation_date = datetime.datetime.strptime(
                row["valuation_date"], "%Y-%m-%d"
            ).date()
            query = (
                insert_statement
                % (
                    index + 1,
                    "false",
                    valuation_date,
                    row["rate_value"],
                    row["exchanged_currency_id"],
                    row["source_currency_id"],
                ),
            )
            tasks.append(cursor.execute(query[0]))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    db_config = {
        "host": "127.0.0.1",
        "port": 5432,
        "user": "postgres",
        "password": "Rajan7347*",
        "database": "my_currency",
    }
    asyncio.run(main(db_config))
