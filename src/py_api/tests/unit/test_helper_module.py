from datetime import date, time
from ...helper_module import *
from ...model import Item

# TODO: Add tests for type checking and error handling

def test_count_alphanumeric():
  assert calculate_retailer_points("M&M Market123") == 12

def test_round_dollar_bonus():
  assert calculate_round_total_points(10.0) == 50
  assert calculate_round_total_points(10.1) == 50

def test_quarter_multiple_bonus():
  assert calculate_quarter_multiple_points(9.75) == 25
  assert calculate_quarter_multiple_points(9.80) == 0

def test_item_pair_bonus():
  items = [Item(short_description="Milk", price="5.00")]
  assert calculate_item_count_points(items) == 0
  items.append(items[0])
  assert calculate_item_count_points(items) == 5

def test_description_length_bonus():
  items = [
    Item(short_description="Milk", price="5.00"),
    Item(short_description="AAA", price="4.00")
  ]
  assert calculate_item_description_points(items) == 1  # "AAA" gives 1 point

def test_odd_day_bonus():
  assert calculate_odd_day_points(
    date.fromisoformat("2023-07-10")
  ) == 0
  assert calculate_odd_day_points(
    date.fromisoformat("2022-01-01")
  ) == 6

def test_afternoon_bonus():
  assert calculate_afternoon_purchase_points(
    time.fromisoformat("14:30")
  ) == 10
  assert calculate_afternoon_purchase_points(
    time.fromisoformat("13:59")
  ) == 0
