from fastapi import FastAPI
from src.endpoint.middleware import add_process_time_header
from src.endpoint import (
    measure_scrape_time,
    scrapedata_save
)

app = FastAPI()

app.middleware("http")(add_process_time_header)

app.include_router(measure_scrape_time.router, prefix="/time", tags=["Time"])
app.include_router(scrapedata_save.router, prefix="/save", tags=["Save"])




