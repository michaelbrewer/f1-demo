import asyncio
import json
from typing import Any, Dict, Union

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

from .f1_client import F1Client

logger = Logger()
tracer = Tracer()


def build_response(status: int, context_type: str, result: Union[str, dict, list]) -> Dict[str, Any]:
    body = result if isinstance(result, str) else json.dumps(result)
    return {
        "statusCode": status,
        "headers": {"Content-Type": context_type},
        "body": body,
    }


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler(capture_error=True, capture_response=True)
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    logger.debug("Testing debug message...")
    f1_client = F1Client()
    data = asyncio.run(f1_client.race_results())
    logger.debug(data)
    return build_response(
        200,
        "application-json",
        data["MRData"]["RaceTable"]["Races"][0]["Results"],
    )
