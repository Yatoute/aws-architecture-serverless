#!/usr/bin/env python

# Réalisé par: Komi Amégbor Richard GOZAN

from constructs import Construct
from cdktf import App, TerraformStack, TerraformAsset, AssetType

from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.lambda_function import LambdaFunction
from cdktf_cdktf_provider_aws.lambda_event_source_mapping import LambdaEventSourceMapping
from cdktf_cdktf_provider_aws.data_aws_caller_identity import DataAwsCallerIdentity
from cdktf_cdktf_provider_aws.sqs_queue import SqsQueue


class LambdaStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)
        AwsProvider(self, "AWS", region="us-east-1")
        account_id = DataAwsCallerIdentity(self, "acount_id").account_id

        # Création des deux files d'attente
        input_queue = SqsQueue(
            self,
            "input_queue",
            name = "input_queue",
            visibility_timeout_seconds = 60
        )
        output_queue = SqsQueue(
            self,
            "output_queue",
            name = "output_queue",
            visibility_timeout_seconds = 60
        )

        # Packagage du code
        code = TerraformAsset(self, "lambda_code", path="./lambda", type=AssetType.DATA)

        # Création de la fonction lambda
        lambda_function = LambdaFunction(self,
                "lambda",
                function_name="calculatrice",
                runtime="python3.9",
                memory_size=128,
                timeout=60,
                role=f"arn:aws:iam::{account_id}:role/LabRole",
                filename= code.path,
                handler="lambda_function.lambda_handler",
                environment={"variables": {"OUTPUT_QUEUE_URL": output_queue.url}}
            )

        # Lie input_queue commme source Lambda
        LambdaEventSourceMapping(
            self, "event_source_mapping",
            event_source_arn=input_queue.arn,
            function_name=lambda_function.arn
        )


app = App()
LambdaStack(app, "graded_lab")

app.synth()
