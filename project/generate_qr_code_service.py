import io

import qrcode
from pydantic import BaseModel
from qrcode.constants import (
    ERROR_CORRECT_H,
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
)


class GenerateQRResponse(BaseModel):
    """
    Response model containing the generated QR code in PNG format. On success, returns a binary PNG image file; on failure, provides error details.
    """

    status: str
    message: str
    qr_code: bytes


def generate_qr_code(
    url: str,
    size: int = 250,
    color: str = "black",
    backgroundColor: str = "white",
    errorCorrectionLevel: str = "M",
) -> GenerateQRResponse:
    """
    Generates a QR code based on the provided URL and customization options like size, color, and error correction level.

    Args:
        url (str): The URL to be encoded into the QR code.
        size (int): The size of the QR code in pixels. Default is 250x250.
        color (str): The color of the QR code. Default is black.
        backgroundColor (str): The background color of the QR code. Default is white.
        errorCorrectionLevel (str): The error correction level, allowing the QR code to be scanned even if partially obscured. Values can be L, M, Q, H. Default is M.

    Returns:
        GenerateQRResponse: Response model containing the generated QR code in PNG format.
    """
    error_correction_map = {
        "L": ERROR_CORRECT_L,
        "M": ERROR_CORRECT_M,
        "Q": ERROR_CORRECT_Q,
        "H": ERROR_CORRECT_H,
    }
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=error_correction_map[errorCorrectionLevel],
            box_size=max(1, size // 100),
            border=4,
        )  # TODO(autogpt): "QRCode" is not a known member of module "qrcode". reportAttributeAccessIssue
        #   Found documentation for the module:
        #    To fix the error """"QRCode" is not a known member of module "qrcode". reportAttributeAccessIssue""", ensure that you are correctly implementing the `QRCode` class from the `qrcode` module in your code. Use the following example as a reference on how to properly use the `QRCode` class:
        #
        #   ```python
        #   import qrcode
        #   qr = qrcode.QRCode(
        #       version=1,
        #       error_correction=qrcode.constants.ERROR_CORRECT_L,
        #       box_size=10,
        #       border=4,
        #   )
        #   qr.add_data('Some data')
        #   qr.make(fit=True)
        #
        #   img = qr.make_image(fill_color="black", back_color="white")
        #   ```
        #
        #   This snippet demonstrates the definition of a `QRCode` object with various parameters (version, error correction level, box size, and border size) and generates an image from the data added to the QR code object. Ensure you have the `qrcode` module installed with the necessary dependencies (like Pillow for image generation) by running:
        #
        #   ```
        #   pip install qrcode[pil]
        #   ```
        #
        #   If you encounter this issue because `QRCode` is not being recognized as a member of `qrcode`, double-check the import statements and ensure that there are no naming conflicts or typos in your code.
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color=color, back_color=backgroundColor)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)
        return GenerateQRResponse(
            status="success",
            message="QR code generated successfully.",
            qr_code=img_byte_arr.getvalue(),
        )
    except Exception as e:
        return GenerateQRResponse(
            status="error",
            message="Failed to generate QR code: " + str(e),
            qr_code=None,
        )
