# Web Scraping FastAPI Service

- A FastAPI application to scrape university course data and save it into text files asynchronously. The project provides endpoints to trigger scraping and to save the data into a structured folder.

# Features

- Scrape course data from universities asynchronously.

- Save each course into a separate .txt file with sanitized names.

- Middleware for measuring request processing time (X-Process-Time header).

- Clean project structure separating routes, services, and middleware.

- Handles errors gracefully using FastAPI’s HTTP exceptions.

