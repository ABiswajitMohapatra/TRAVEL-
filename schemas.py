from pydantic import BaseModel
from typing import List


class DayPlan(BaseModel):
    day: int
    morning: str
    afternoon: str
    evening: str


class TravelPlan(BaseModel):
    destination: str
    total_budget: int
    days: List[DayPlan]
    estimated_cost: int
    notes: str
