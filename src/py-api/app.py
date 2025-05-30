import uvicorn
import os
from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from model import Receipt, ReceiptProcessResponse, ReceiptPointResponse

app = FastAPI()
PORT = int(os.getenv("PORT", 8000))

# @app.post("/receipts/process")
# async def process_receipt()
# In-memory storage for receipts and their points
receipt_store = {}
point_cache = {}

@app.post("/receipts/process", response_model=ReceiptProcessResponse)
async def process_receipt(receipt: Receipt) -> ReceiptProcessResponse:
  # Dummy logic
  return ReceiptProcessResponse(id="some-generated-id")

@app.get("/receipts/{id}/points", response_model=ReceiptPointResponse)
async def get_receipt_points(id: str = Path(
  ...,
  description='The ID assigned to the receipt.',
  examples='adb6b560-0eef-42bc-9d16-df48f30e89b2',
  pattern=r'^\S+$'
)) -> ReceiptPointResponse:
  # Dummy logic
  return ReceiptPointResponse(points=100)

# Fallback route handler for 404s
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(exc: StarletteHTTPException):
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
