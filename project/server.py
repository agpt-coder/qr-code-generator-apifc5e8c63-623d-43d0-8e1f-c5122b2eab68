import io
import logging
from contextlib import asynccontextmanager

import prisma
import project.generate_qr_code_service
import project.validate_api_key_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, StreamingResponse
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="QR Code Generator API",
    lifespan=lifespan,
    description="""The task involves creating an endpoint that accepts a URL input, generates a QR code image that encodes the provided URL, and enables customization options for the QR code such as size, color, and error correction level, before returning the QR code image in PNG format. Based on previous interactions and searches, here are the compiled steps and technologies to accomplish this:

1. **Programming Language**: Python - A versatile and widely used programming language that is suitable for web development and manipulating images, making it an optimal choice for generating customized QR codes.

2. **API Framework**: FastAPI - A modern, fast (high-performance) web framework for building APIs with Python 3.7+ that includes automatic Swagger UI documentation. It's asynchronous which makes it suitable for IO-bound tasks like generating and sending images.

3. **Database**: PostgreSQL - While the task specifically doesn't require database interactions, PostgreSQL is chosen for future extensions where storing URLs or generated QR codes might be necessary.

4. **ORM**: Prisma - An ORM for contemporary app development with support for Python. Optimal for integrating with PostgreSQL for any data persistence needs.

**Implementation Details**:
- Use the `qrcode` Python library to generate QR codes. This library allows specifying parameters like `version`, `error_correction`, `box_size`, and colors (`fill_color`, `back_color`) to customize the QR code according to user preferences.
- `FastAPI` will be used to set up the web server and define the endpoint. The endpoint will leverage query parameters or request body to accept customization options (size, color, error correction level) and the URL to generate the QR code.
- `Prisma` and `PostgreSQL` are part of the tech stack for scalability and future-proofing the application, despite not being directly involved in generating or serving QR codes.
- To return the QR code image in PNG format, FastAPI's `FileResponse` class can be used to send the generated image back to the client.

**Important Notes**:
- Ensure input validation on the FastAPI endpoint to prevent injection or other malicious activities.
- Incorporate error handling for scenarios where the QR code cannot be generated (e.g., invalid URL, unsupported customization options).
- Consider implementing caching or a storage solution for generated QR codes to improve performance and reduce processing time for repeat requests.

This comprehensive solution outlines the steps, technologies, and considerations for building a service that dynamically generates and returns customized QR codes in PNG format.""",
)


@app.post(
    "/generate-qr", response_model=project.generate_qr_code_service.GenerateQRResponse
)
async def api_post_generate_qr_code(
    url: str, size: int, color: str, backgroundColor: str, errorCorrectionLevel: str
) -> project.generate_qr_code_service.GenerateQRResponse | Response:
    """
    Generates a QR code based on provided URL and customization options like size, color, and error correction level.
    """
    try:
        res = project.generate_qr_code_service.generate_qr_code(
            url, size, color, backgroundColor, errorCorrectionLevel
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.head(
    "/validate-key",
    response_model=project.validate_api_key_service.ValidateAPIKeyResponse,
)
async def api_head_validate_api_key(
    api_key: str,
) -> project.validate_api_key_service.ValidateAPIKeyResponse | Response:
    """
    Validates the provided API key before processing the QR code generation request.
    """
    try:
        res = await project.validate_api_key_service.validate_api_key(api_key)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
