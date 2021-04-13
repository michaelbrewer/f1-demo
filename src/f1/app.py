import asyncio
from typing import Any, Dict, List

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import AppSyncResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

from .f1_client import F1Client

logger = Logger()
tracer = Tracer()
f1_client = F1Client()
app = AppSyncResolver()


@app.resolver(type_name="Query", field_name="listResults")
async def race_results(season: str = "current", race: str = "last") -> List:
    data = await f1_client.race_results(season, race)
    logger.debug(data)
    return data["MRData"]["RaceTable"]["Races"][0]["Results"]


@app.resolver(type_name="Query", field_name="listSchedule")
async def schedule(season: str = "current") -> List:
    data = await f1_client.schedule(season)
    logger.debug(data)
    return data["MRData"]["RaceTable"]["Races"]


@app.resolver(type_name="Query", field_name="summaryResults")
async def summary_results(season: str = "current", number_races: str = "17") -> List:
    return await f1_client.summary_results(season, int(number_races))


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler(capture_error=True, capture_response=True)
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    logger.debug("Testing debug message...")
    return asyncio.run(app.resolve(event, context))
