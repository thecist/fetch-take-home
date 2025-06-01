import pytest
import json
from datetime import date, time
from pathlib import Path
from ...helper_module import store_and_calculate
from ...model import Receipt, Item

# Utility to load receipt JSON and convert it into a Receipt model
def load_receipt(file_name):
  file_path = Path(__file__).resolve().parents[4] / "receipts" / file_name
  with open(file_path) as f:
    raw_data = json.load(f)
    return Receipt(
      retailer=raw_data["retailer"],
      purchase_date=date.fromisoformat(raw_data["purchaseDate"]),
      purchase_time=time.fromisoformat(raw_data["purchaseTime"]),
      total=raw_data["total"],
      items=[
        Item(
          short_description=item["shortDescription"],
          price=item["price"]
        ) for item in raw_data["items"]
      ]
    )

# Unit test to verify store_and_calculate functionality
@pytest.mark.parametrize("file_name", [
  "receipt1.json", "receipt2.json", "receipt3.json", "receipt4.json"
])
def test_store_and_calculate(file_name, memory_stores):
  """
  Tests the `store_and_calculate` function by verifying that a receipt is correctly stored and its points are calculated.
  Args:
    file_name (str): The name of the file containing the receipt data.
    memory_stores (tuple): A tuple containing the receipt store and point cache objects.
  Asserts:
    - The receipt ID is present in the receipt store after processing.
    - The receipt ID is present in the point cache after processing.
    - The returned points value is an integer.
    - The points value in the point cache matches the returned value.
    - The points value is non-negative.
  """

  receipt_store, point_cache = memory_stores
  receipt = load_receipt(file_name)
  receipt_id = f"test-{file_name}"

  points = store_and_calculate(receipt_id, receipt, receipt_store, point_cache)

  # Assertions
  assert receipt_id in receipt_store
  assert receipt_id in point_cache
  assert isinstance(points, int)
  assert point_cache[receipt_id] == points
  assert points >= 0