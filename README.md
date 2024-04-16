---
date: 2024-04-16T16:54:56.478487
author: AutoGPT <info@agpt.co>
---

# QR Code Generator API

The task involves creating an endpoint that accepts a URL input, generates a QR code image that encodes the provided URL, and enables customization options for the QR code such as size, color, and error correction level, before returning the QR code image in PNG format. Based on previous interactions and searches, here are the compiled steps and technologies to accomplish this:

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

This comprehensive solution outlines the steps, technologies, and considerations for building a service that dynamically generates and returns customized QR codes in PNG format.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'QR Code Generator API'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
