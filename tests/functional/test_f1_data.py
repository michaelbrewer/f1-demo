import json
from typing import List, Dict

import pytest
import vcr
from dateutil.parser import parse
from pytz import timezone
from rich.console import Console
from rich.table import Table

from src.f1.f1_client import F1Client


@vcr.use_cassette(match_on=["uri", "headers", "body"])
@pytest.mark.asyncio
async def test_race_schedule():
    print("")
    f1_client = F1Client()
    season = "2021"
    results = await f1_client.schedule(season)
    race_table = results["MRData"]["RaceTable"]
    table = Table(title=f"Season - {season}")
    table.add_column("Date")
    table.add_column("Time")
    table.add_column("Round")
    table.add_column("Race name")
    table.add_column("Circuit name")

    for race in race_table["Races"]:
        full_date = parse(race["date"] + " " + race["time"])
        full_date = full_date.astimezone(timezone("US/Pacific"))
        date_str = str(full_date.strftime("%m/%d/%Y"))
        time_str = str(full_date.strftime("%I:%M %p"))

        table.add_row(
            date_str,
            time_str,
            race["round"],
            race["raceName"],
            race["Circuit"]["circuitName"],
        )

    # print("Season", race_table["season"])
    # print("Races", json.dumps(race_table["Races"], indent=4))

    console = Console(width=400)
    console.print(table)


@vcr.use_cassette(match_on=["uri", "headers", "body"])
@pytest.mark.asyncio
async def test_race_results():
    f1_client = F1Client()
    results = await f1_client.race_results("2021", "1")
    print("")
    print(json.dumps(results["MRData"]["RaceTable"]["Races"][0]["Results"], indent=4))


@vcr.use_cassette
@pytest.mark.asyncio
async def test_race_results_for_season():
    f1_client = F1Client()
    season = "2020"

    races: List[Dict] = await f1_client.race_results_for_season(season, 17)
    print("")
    table = Table(title=f"Season - {season}")
    table.add_column("Date")
    table.add_column("Race name")
    table.add_column("1st")
    table.add_column("2nd")
    table.add_column("3rd")
    table.add_column("Fastest Lap")

    for race in races:
        race = race["MRData"]["RaceTable"]["Races"][0]
        # print(json.dumps(race, indent=4))
        results = race["Results"]
        first = results[0]
        second = results[1]
        third = results[2]

        fastest_lap: str = ""
        for result in results:
            if "FastestLap" in result and result["FastestLap"]["rank"] == "1":
                fastest_lap = print_driver_lap(result)

        table.add_row(
            race["date"],
            race["raceName"],
            print_driver(first, True),
            print_driver(second),
            print_driver(third),
            fastest_lap,
        )

    console = Console(width=600)
    console.print(table)


def print_driver_lap(driver):
    return f'{driver["Driver"]["givenName"]} {driver["Driver"]["familyName"]} - {driver["FastestLap"]["Time"]["time"]}'


def print_driver(driver, first: bool = False):
    return (
        f'{driver["Driver"]["givenName"]} {driver["Driver"]["familyName"]} {driver["points"]} pts '
        f'{"" if first else driver["Time"]["time"] + " secs"}'
    )
