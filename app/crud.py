from app.database import get_db
from datetime import datetime
from typing import Optional, Dict, Any
from app.utils import calculate_cost  # 新增导入

def create_ride() -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO rides (start_time) VALUES (?)",
            (datetime.utcnow().isoformat(),)
        )
        conn.commit()
        ride_id = cursor.lastrowid
        row = conn.execute(
            "SELECT id, start_time FROM rides WHERE id = ?",
            (ride_id,)
        ).fetchone()
        return {"id": row["id"], "start_time": datetime.fromisoformat(row["start_time"])}

def end_ride(ride_id: int) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, start_time, end_time, status FROM rides WHERE id = ?",
            (ride_id,)
        ).fetchone()
        if not row:
            return None
        if row["status"] == "completed":
            return None
        now = datetime.utcnow().isoformat()
        conn.execute(
            "UPDATE rides SET end_time = ?, status = 'completed' WHERE id = ?",
            (now, ride_id)
        )
        conn.commit()
        updated_row = conn.execute(
            "SELECT id, start_time, end_time, status FROM rides WHERE id = ?",
            (ride_id,)
        ).fetchone()
        return {
            "id": updated_row["id"],
            "start_time": datetime.fromisoformat(updated_row["start_time"]),
            "end_time": datetime.fromisoformat(updated_row["end_time"]),
            "status": updated_row["status"],
        }

def get_ride(ride_id: int) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, start_time, end_time, status FROM rides WHERE id = ?",
            (ride_id,)
        ).fetchone()
        if not row:
            return None
        result = {
            "id": row["id"],
            "start_time": datetime.fromisoformat(row["start_time"]),
            "status": row["status"],
        }
        if row["end_time"]:
            result["end_time"] = datetime.fromisoformat(row["end_time"])
        else:
            result["end_time"] = None
        return result

def get_ride_with_cost(ride_id: int) -> Optional[Dict[str, Any]]:
    ride = get_ride(ride_id)
    if not ride:
        return None
    if ride["status"] != "completed" or ride["end_time"] is None:
        return None
    cost = calculate_cost(ride["start_time"], ride["end_time"])  # 现在可以正确调用
    return {**ride, "cost": cost}