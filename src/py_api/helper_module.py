from model import Receipt, Item
from typing import List
from math import ceil, floor
from datetime import date, time

receipt_store = {}
point_cache = {}

def calculate_retailer_points(retailer: str) -> int:
  """One point for every alphanumeric character in the retailer name."""
  return sum(c.isalnum() for c in retailer)

def calculate_round_total_points(total: float) -> int:
  """50 points if the total is a round dollar amount (e.g. 10.00)."""
  return 50 if floor(total) == total else 0

def calculate_quarter_multiple_points(total: float) -> int:
  """25 points if the total is a multiple of 0.25."""
  return 25 if total % 0.25 == 0 else 0

def calculate_item_count_points(items: List[Item]) -> int:
  """5 points for every two items (integer division)."""
  return (len(items) // 2) * 5

def calculate_item_description_points(items: List[Item]) -> int:
  """
  If the trimmed length of an item description is a multiple of 3,
  multiply the price by 0.2 and round up.
  """
  points = 0
  for item in items:
    desc_len = len(item.short_description.strip())
    if desc_len % 3 == 0:
      points += ceil(float(item.price) * 0.2)
  return points

def calculate_odd_day_points(purchase_date: date) -> int:
  """6 points if the day is odd."""
  return 6 if purchase_date.day % 2 == 1 else 0

def calculate_afternoon_purchase_points(purchase_time: time) -> int:
  """
  10 points if purchase time is after 2:00 PM and before 4:00 PM.
  Time is 24-hour format.
  """
  time_minutes = purchase_time.hour * 60 + purchase_time.minute
  return 10 if 14 * 60 < time_minutes < 16 * 60 else 0

def store_and_calculate(receipt_id: str, receipt: Receipt, receipt_store: dict, point_cache: dict) -> int:
  """
  Stores the given receipt in memory and calculates reward points based on various criteria.
  Args:
    receipt_id (str): The unique identifier for the receipt.
    receipt (Receipt): The receipt object containing purchase details.
  Returns:
    int: The total calculated reward points for the receipt.
  Side Effects:
    - Stores the receipt in the `receipt_store` dictionary.
    - Stores the calculated points in the `point_cache` dictionary.
  Calculation Criteria:
    - Retailer name characteristics.
    - Whether the total is a round dollar amount.
    - Whether the total is a multiple of 0.25.
    - Number of items on the receipt.
    - Description of items.
    - If the purchase date is an odd day.
    - If the purchase time is in the afternoon.
  """

  # Save receipt and points in memory
  receipt_store[receipt_id] = receipt

  # TODO: Add comments for each step
  # TODO: Complete OpenAPI schema transfer when up(description etc)
  # TODO: Write unit tests and integration tests
  # TODO: Add logging
  # TODO: Make python -m pip install equal pip

  # Convert total to float for calculations
  total = float(receipt.total)

  # Calculate points based on various criteria
  points = (
    calculate_retailer_points(receipt.retailer) +
    calculate_round_total_points(total) +
    calculate_quarter_multiple_points(total) +
    calculate_item_count_points(receipt.items) +
    calculate_item_description_points(receipt.items) +
    calculate_odd_day_points(receipt.purchase_date) +
    calculate_afternoon_purchase_points(receipt.purchase_time)
  )

  # Store the calculated points in the cache
  point_cache[receipt_id] = points

  # Return the calculated points
  return points