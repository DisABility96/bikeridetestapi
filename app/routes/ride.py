from fastapi import APIRouter, HTTPException, status
from app import crud, schemas

router = APIRouter()

@router.post("/start", response_model=schemas.RideStartResponse, status_code=status.HTTP_201_CREATED)
def start_ride():
    ride = crud.create_ride()
    return ride

@router.post("/end", response_model=schemas.RideDetail)
def end_ride(request: schemas.RideEndRequest):
    result = crud.end_ride(request.ride_id)
    if result is None:
        ride = crud.get_ride(request.ride_id)
        if ride is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ride not found")
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ride already ended")
    # 计算费用和时长
    start = result["start_time"]
    end = result["end_time"]
    duration_minutes = (end - start).total_seconds() / 60.0
    from app.utils import calculate_cost  # 确保导入正确
    cost = calculate_cost(start, end)
    return {
        "id": result["id"],
        "start_time": start,
        "end_time": end,
        "status": result["status"],
        "duration_minutes": duration_minutes,
        "cost": cost,
    }

@router.get("/{ride_id}", response_model=schemas.RideDetail)
def get_ride(ride_id: int):
    ride = crud.get_ride(ride_id)
    if not ride:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ride not found")
    if ride["status"] == "completed" and ride["end_time"]:
        duration = (ride["end_time"] - ride["start_time"]).total_seconds() / 60.0
        from app.utils import calculate_cost
        cost = calculate_cost(ride["start_time"], ride["end_time"])
        return {
            "id": ride["id"],
            "start_time": ride["start_time"],
            "end_time": ride["end_time"],
            "status": ride["status"],
            "duration_minutes": duration,
            "cost": cost,
        }
    else:
        return {
            "id": ride["id"],
            "start_time": ride["start_time"],
            "end_time": None,
            "status": ride["status"],
            "duration_minutes": None,
            "cost": None,
        }

@router.get("/{ride_id}/cost", response_model=schemas.RideCostResponse)
def get_ride_cost(ride_id: int):
    ride_with_cost = crud.get_ride_with_cost(ride_id)
    if not ride_with_cost:
        ride = crud.get_ride(ride_id)
        if ride is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ride not found")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot calculate cost for active ride")
    return {"ride_id": ride_id, "cost": ride_with_cost["cost"]}