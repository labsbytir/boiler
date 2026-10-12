# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 TIR Labs. All rights reserved.

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["service"] == "api-python"
    assert data["error"] is None
