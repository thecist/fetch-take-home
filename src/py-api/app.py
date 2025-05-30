import uvicorn
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from model import Receipt, ReceiptProcessResponse, ReceiptPointResponse

app = FastAPI()
PORT = int(os.getenv("PORT", 8000))

# @app.post("/receipts/process")
# async def process_receipt()
  
@app.get("/")
async def root():
  return {"message": "Hello World"}

# Fallback route handler for 404s
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
  if exc.status_code == 404:
    return JSONResponse(
      status_code=404,
      content={
        "error": "Route not found",
        "message": "This endpoint isn't part of the take-home assessment. [Insert cute cat gif here]"
      },
    )
  return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


if __name__ == "__main__":
  uvicorn.run("app:app", host="0.0.0.0", port=PORT, reload=True)
