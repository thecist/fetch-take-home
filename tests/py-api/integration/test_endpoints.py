import pytest
import json
from pathlib import Path

@pytest.mark.parametrize("file_name", [
  "receipt1.json", "receipt2.json", "receipt3.json", "receipt4.json"
])
def test_process_and_get_points(client, file_name):
  file_path = Path(__file__).parent.parent.parent / "receipts" / file_name
  with open(file_path) as f:
    receipt_data = json.load(f)

  # POST the receipt
  post_resp = client.post("/receipts/process", json=receipt_data)
  assert post_resp.status_code == 200
  receipt_id = post_resp.json()["id"]
  assert isinstance(receipt_id, str)


  # GET the points
  get_resp = client.get(f"/receipts/{receipt_id}/points")
  assert get_resp.status_code == 200
  json_resp = get_resp.json()
  assert "points" in json_resp
  assert isinstance(json_resp["points"], int)
  assert json_resp["points"] >= 0  # sanity check
