import math
from datetime import datetime

def calculate_cost(start: datetime, end: datetime) -> float:
    """
    根据定价规则计算骑行费用：
    - 解锁费 $5
    - 前15分钟免费
    - 之后每5分钟 $1（不足5分钟按5分钟计）
    - 单次骑行封顶 $25
    """
    duration = (end - start).total_seconds() / 60.0
    if duration <= 15:
        time_cost = 0.0
    else:
        paid_minutes = duration - 15
        time_cost = math.ceil(paid_minutes / 5) * 1.0
    total = 5.0 + time_cost
    return min(total, 25.0)