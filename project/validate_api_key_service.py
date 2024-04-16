import prisma
import prisma.models
from fastapi import HTTPException
from pydantic import BaseModel


class ValidateAPIKeyResponse(BaseModel):
    """
    Response model for the API key validation process. Being a HEAD request, the typical use case doesn't expect a body in the response, but standard HTTP status codes will be used to indicate the result of the validation. A 200 means validation success, while a 401 would indicate failure.
    """

    validation_status: str


async def validate_api_key(api_key: str) -> ValidateAPIKeyResponse:
    """
    Validates the provided API key before processing the QR code generation request.
    This function checks if the given API key exists in the database and returns a corresponding
    response object indicating the validation result.

    Args:
    api_key (str): The API key provided by the client for validation.

    Returns:
    ValidateAPIKeyResponse: Response model for the API key validation process. Being a HEAD request,
    the typical use case doesn't expect a body in the response, but standard HTTP status codes will
    be used to indicate the result of the validation. A 200 means validation success, while a 401
    would indicate failure.

    Raises:
    HTTPException: If the API key is not found, indicating invalid or expired API key.
    """
    api_key_instance = await prisma.models.ApiKey.prisma().find_unique(
        where={"key": api_key}
    )
    if api_key_instance:
        return ValidateAPIKeyResponse(validation_status="200 OK")
    else:
        raise HTTPException(status_code=401, detail="Invalid API key")
