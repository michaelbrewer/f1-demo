def test_handler(lambda_context):
    from src.f1.app import lambda_handler

    print(lambda_handler({}, lambda_context))
