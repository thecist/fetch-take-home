import pytest
from datetime import date, time
from ...helper_module import *
from ...model import Item

# TODO: Add tests for type checking and error handling

def test_count_alphanumeric():
  assert calculate_retailer_points("M&M Market123") == 11
  with pytest.raises(TypeError):
    calculate_retailer_points(12345)

def test_round_dollar_bonus():
  assert calculate_round_total_points(10.0) == 50
  assert calculate_round_total_points(10.1) == 0
  with pytest.raises((TypeError, ValueError)):
    calculate_round_total_points("10.00")

def test_quarter_multiple_bonus():
  assert calculate_quarter_multiple_points(9.75) == 25
  assert calculate_quarter_multiple_points(9.80) == 0
  with pytest.raises((TypeError, ValueError)):
    calculate_quarter_multiple_points(None)

def test_item_pair_bonus():
  items = [Item(short_description="Milk", price="5.00")]
  assert calculate_item_count_points(items) == 0
  items.append(items[0])
  assert calculate_item_count_points(items) == 5
  with pytest.raises(TypeError):
    calculate_item_count_points(100)

def test_description_length_bonus():
  items = [
    Item(short_description="Milk", price="5.00"),
    Item(short_description="AAA", price="4.00")
  ]
  assert calculate_item_description_points(items) == 1
  with pytest.raises(TypeError):
    calculate_item_description_points(123)

def test_odd_day_bonus():
  assert calculate_odd_day_points(
    date.fromisoformat("2023-07-10")
  ) == 0
  assert calculate_odd_day_points(
    date.fromisoformat("2022-01-01")
  ) == 6
  with pytest.raises(AttributeError):
    calculate_odd_day_points("2022-01-01")

def test_afternoon_bonus():
  assert calculate_afternoon_purchase_points(
    time.fromisoformat("14:30")
  ) == 10
  assert calculate_afternoon_purchase_points(
    time.fromisoformat("13:59")
  ) == 0
  with pytest.raises(AttributeError):
    calculate_afternoon_purchase_points("14:30")
