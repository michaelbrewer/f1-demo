import asyncio
from typing import Dict

import aiohttp
from aiohttp import ClientTimeout
from aws_lambda_powertools.tracing import aiohttp_trace_config


class F1Client:
    def __init__(self):
        self.timeout = 10
        self.batch_size = 5
        self.base_url = "https://ergast.com/api/f1"

    async def _session(self):
        return aiohttp.ClientSession(
            timeout=ClientTimeout(total=self.timeout),
            headers={"Content-Type": "application-json"},
            trace_configs=[aiohttp_trace_config()],
        )

    async def schedule(self, season: str = "current") -> Dict:
        async with await self._session() as session:
            async with session.get(f"{self.base_url}/{season}.json") as response:
                return await response.json()

    async def race_results(self, season: str = "current", race: str = "last") -> Dict:
        async with await self._session() as session:
            return await self.fetch_race(session, season, race)

    async def race_results_for_season(self, season: str, races: int):
        tasks = []
        async with await self._session() as session:
            for race in range(1, races + 1):
                tasks.append(asyncio.ensure_future(self.fetch_race(session, season, str(race))))
            responses = await asyncio.gather(*tasks)
        return responses

    async def fetch_race(self, session, season: str, race: str) -> Dict:
        async with session.get(f"{self.base_url}/{season}/{race}/results.json") as response:
            return await response.json()
