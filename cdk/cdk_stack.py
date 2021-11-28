from aws_cdk import aws_lambda
from aws_cdk import core as cdk
from aws_cdk.aws_lambda import Tracing, Function, Code, Runtime
from aws_cdk.core import Duration, BundlingOptions


class CdkStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Function(
            scope=self,
            id="f1Function",
            function_name="f1-dev",
            handler="f1.app.lambda_handler",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            environment={
                "LOG_LEVEL": "DEBUG",
                "POWERTOOLS_SERVICE_NAME": "f1",
                "POWERTOOLS_METRICS_NAMESPACE": "f1-stats",
            },
            tracing=Tracing.ACTIVE,
            memory_size=1024,
            timeout=Duration.seconds(60),
            architecture=aws_lambda.Architecture.ARM_64,
            code=Code.from_asset(
                "src/",
                bundling=BundlingOptions(
                    image=Runtime.PYTHON_3_9.bundling_image,
                    command=[
                        "bash",
                        "-c",
                        "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output",
                    ],
                ),
            ),
        )
