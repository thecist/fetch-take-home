"""
This module implements a FastAPI application for processing and scoring receipts.
Endpoints:
- POST /receipts/process: Accepts a receipt, processes it asynchronously, and returns a unique receipt ID.
- GET /receipts/{id}/points: Returns the calculated points for a given receipt ID.
- Custom 404 handler: Returns a friendly message for undefined routes.
Functions:
- store_and_calculate(receipt_id: str, receipt: Receipt) -> int:
  Stores the receipt and calculates points based on retailer name, total amount, item descriptions, purchase date, and time.
  Points are cached in-memory for quick retrieval.
Notes:
- In-memory dictionaries are used for storage and caching (not suitable for production).
- Receipt and response models are imported from the local 'model' module.
- The application is intended for demonstration and assessment purposes.
"""
import uvicorn
import os
import uuid
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, Path, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from .model import Receipt, ReceiptProcessResponse, ReceiptPointResponse
from .helper_module import store_and_calculate

app = FastAPI(
  title="Receipt Processor",
  description="A simple receipt processor",
  version="1.0.0",
  contact={
    "name": "Your Name",
    "github": "https://github.com/tayomide"
  }
)
PORT = int(os.getenv("PORT", 8000))

# In-memory storage for receipts and their points
# Note: In a production environment, I would use a database and redis for cache
receipt_store = {}
point_cache = {}

@app.post(
  "/receipts/process",
  response_model=ReceiptProcessResponse,
  summary="Submits a receipt for processing.",
  description="Submits a receipt for processing.",
  response_description="Returns the ID assigned to the receipt."
)
async def process_receipt(receipt: Receipt, background_tasks: BackgroundTasks) -> ReceiptProcessResponse:
  """
  Asynchronously processes a receipt by generating a unique receipt ID, scheduling background post-processing, and returning the receipt ID.
  Args:
    receipt (Receipt): The receipt object to be processed.
    background_tasks (BackgroundTasks): FastAPI background tasks manager for scheduling post-processing.
  Returns:
    ReceiptProcessResponse: Response object containing the generated receipt ID.
  """

  # Create a unique ID for the receipt
  receipt_id = str(uuid.uuid4())

  # Performs post-processing in the background, reducing response time
  background_tasks.add_task(store_and_calculate, receipt_id, receipt, receipt_store, point_cache)

  # Return the receipt ID immediately
  return ReceiptProcessResponse(id=receipt_id)

@app.get(
  "/receipts/{id}/points",
  response_model=ReceiptPointResponse,
  summary="Returns the points awarded for the receipt.",
  description="Returns the points awarded for the receipt.",
  response_description="The number of points awarded."
)
async def get_receipt_points(id: str = Path(
  ...,
  description='The ID assigned to the receipt.',
  example='adb6b560-0eef-42bc-9d16-df48f30e89b2',
  pattern=r'^\S+$'
)) -> ReceiptPointResponse:
  """
  Retrieve the points associated with a specific receipt by its ID.
  Args:
    id (str): The unique identifier assigned to the receipt. Must be a non-whitespace string.
  Returns:
    ReceiptPointResponse: An object containing the calculated points for the specified receipt.
  Raises:
    StarletteHTTPException: If the receipt with the given ID is not found (404 error).
  Path Parameters:
    id (str): The ID assigned to the receipt (example: 'adb6b560-0eef-42bc-9d16-df48f30e89b2').
  """
  
  # Check if the receipt ID exists in the store
  if id not in receipt_store:
    raise StarletteHTTPException(status_code=404, detail="Receipt not found")
  # If the receipt ID exists, check if points are already cached
  # If not cached, calculate and store the points
  if id not in point_cache:
    points = store_and_calculate(id, receipt=receipt_store[id])
  # If points are cached, retrieve them
  else:
    points = point_cache[id]
  # Return the points in the response model
  return ReceiptPointResponse(points=points)

# Fallback route handler for 404s
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
  """
  Custom HTTP exception handler for FastAPI/Starlette applications.
  Handles 404 "Not Found" errors with a custom JSON response, including a user-friendly error message.
  All other HTTP exceptions are returned with their default status code and detail.
  Args:
    request (Request): The incoming HTTP request.
    exc (StarletteHTTPException): The HTTP exception raised during request processing.
  Returns:
    JSONResponse: A JSON response with appropriate status code and error details.
  """

  # If the exception is a 404 with "Not Found", return a custom message
  if exc.status_code == 404 and exc.detail == "Not Found":
    return JSONResponse(
      status_code=404,
      content={
        "error": "Route not found",
        "message": "This endpoint isn't part of the take-home assessment. [Insert cute cat gif here]"
      },
    )
  
  # For all other exceptions, return the default error response
  return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


if __name__ == "__main__":
  uvicorn.run("app:app", host="0.0.0.0", port=PORT, reload=True)
