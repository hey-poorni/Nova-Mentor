# Bedrock connectivity test – placeholder
def test_bedrock_connection():
    from app.services.bedrock_client import get_bedrock_client
    client = get_bedrock_client()
    assert client is not None
