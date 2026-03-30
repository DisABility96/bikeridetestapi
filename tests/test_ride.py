import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
import os
import gc
import time

client = TestClient(app)

# 使用临时数据库进行测试
@pytest.fixture(autouse=True)
def setup_test_db(tmp_path):
    import app.database
    app.database.DATABASE_PATH = str(tmp_path / "test_rides.db")
    init_db()
    yield
    # 强制垃圾回收，可能释放残留连接
    gc.collect()
    time.sleep(0.1)  # 等待操作系统释放文件锁
    # 删除数据库及其附属文件，忽略权限错误
    try:
        if os.path.exists(app.database.DATABASE_PATH):
            os.remove(app.database.DATABASE_PATH)
        for ext in ['-wal', '-shm']:
            f = app.database.DATABASE_PATH + ext
            if os.path.exists(f):
                os.remove(f)
    except PermissionError:
        pass

def test_start_ride():
    response = client.post("/ride/start")
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "start_time" in data

def test_end_ride():
    # 先开始
    start_resp = client.post("/ride/start")
    ride_id = start_resp.json()["id"]
    # 结束
    end_resp = client.post("/ride/end", json={"ride_id": ride_id})
    assert end_resp.status_code == 200
    data = end_resp.json()
    assert data["status"] == "completed"
    assert data["cost"] is not None

def test_end_ride_twice():
    start_resp = client.post("/ride/start")
    ride_id = start_resp.json()["id"]
    client.post("/ride/end", json={"ride_id": ride_id})
    second_end = client.post("/ride/end", json={"ride_id": ride_id})
    assert second_end.status_code == 409
    assert second_end.json()["detail"] == "Ride already ended"

def test_get_ride_active():
    start_resp = client.post("/ride/start")
    ride_id = start_resp.json()["id"]
    resp = client.get(f"/ride/{ride_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "active"
    assert data["duration_minutes"] is None
    assert data["cost"] is None

def test_get_ride_cost_active():
    start_resp = client.post("/ride/start")
    ride_id = start_resp.json()["id"]
    resp = client.get(f"/ride/{ride_id}/cost")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Cannot calculate cost for active ride"