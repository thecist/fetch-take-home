import uvicorn
import os
from fastapi import FastAPI, Request, Response

app = FastAPI()
PORT = int(os.getenv("PORT", 8000))

# @app.post("/receipts/process")
# async def process_receipt()
  
@app.get("/")
async def root():
  return {"message": "Hello World"}

#TODO: Create a fallback route to handle any other requests - something like 404
#not found or route not required for assesment (something funny but professional)

if __name__ == "__main__":
  uvicorn.run("app:app", host="0.0.0.0", port=PORT, reload=True)
