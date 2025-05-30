import uvicorn
import os
import uuid
import math
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



def store_and_calculate(receipt_id: str, receipt: Receipt):
  # Save receipt and points in memory
  receipt_store[receipt_id] = receipt

  # TODO: Add comments for each step
  for char in receipt.retailer:
    if char.isalnum():
      points += 1
  
  total_int = int(receipt.total)
  if math.floor(total_int) == total_int:
    points += 50
  
  if total_int % 0.25 == 0:
    points += 25

  for i, item in enumerate(receipt.items):
    description_length = len(item.short_description.strip())
    if description_length % 3 == 0:
      points = math.ceil(int(item.price) * 0.2)
    if i % 2 == 1:
      points += 1

  if receipt.purchase_date.day % 2 == 1:
    points += 6
  if receipt.purchase_time.hour >2 and receipt.purchase_time.hour < 4:
    points += 10
  point_cache[receipt_id] = points
  return points

@app.post("/receipts/process", response_model=ReceiptProcessResponse)
async def process_receipt(receipt: Receipt, background_tasks: BackgroundTasks) -> ReceiptProcessResponse:
  receipt_id = str(uuid.uuid4())

  # Performs post-processing in the background, reducing response time
  background_tasks.add_task(store_and_calculate, receipt_id, receipt)

  # Return the receipt ID immediately
  return ReceiptProcessResponse(id=receipt_id)

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
