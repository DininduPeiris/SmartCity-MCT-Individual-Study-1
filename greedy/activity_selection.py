"""Activity Selection for Urban Fleet Driver Scheduling.

This module implements the greedy 'Earliest Finish Time' (EFT) scheduling strategy
to maximize non-overlapping delivery jobs serviced by a single driver/vehicle.
Includes the 3-5 sentence informal exchange argument correctness justification.
"""

from dataclasses import dataclass
from typing import List, Tuple, Dict, Any


@dataclass
class DeliveryJob:
    """Represents a delivery assignment with a time window."""
    job_id: str
    description: str
    start_time: float   # e.g., 8.0 for 08:00
    end_time: float     # e.g., 9.5 for 09:30
    destination: str

    def __post_init__(self):
        if self.start_time > self.end_time:
            raise ValueError(f"Job {self.job_id} start_time ({self.start_time}) cannot exceed end_time ({self.end_time})")

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

    def __repr__(self) -> str:
        return f"Job({self.job_id}: [{self.start_time:.1f}h - {self.end_time:.1f}h] -> {self.destination})"


def activity_selection_earliest_finish(jobs: List[DeliveryJob]) -> Tuple[List[DeliveryJob], Dict[str, Any]]:
    """Selects the maximum number of mutually compatible delivery jobs.

    Greedy Strategy:
    1. Sort all jobs by their end (finish) time ascending.
    2. Pick the first job (finishes earliest).
    3. Greedily pick the next job whose start_time >= end_time of the previously chosen job.

    Time Complexity: O(n log n) due to initial sorting; O(n) greedy linear pass.
    Space Complexity: O(n) to store sorted and selected jobs.
    """
    if not jobs:
        return [], {"total_considered": 0, "total_selected": 0, "driver_utilization_hours": 0.0}

    # Step 1: Sort by earliest finish time; tie-break by start time
    sorted_jobs = sorted(jobs, key=lambda j: (j.end_time, j.start_time))

    selected: List[DeliveryJob] = []
    current_end_time = float("-inf")

    # Step 2: Linear greedy scan
    for job in sorted_jobs:
        if job.start_time >= current_end_time:
            selected.append(job)
            current_end_time = job.end_time

    total_duration = sum(j.duration for j in selected)

    stats = {
        "total_considered": len(jobs),
        "total_selected": len(selected),
        "driver_utilization_hours": round(total_duration, 2),
        "selection_efficiency_pct": round((len(selected) / len(jobs)) * 100.0, 1) if jobs else 0.0
    }

    return selected, stats


def get_activity_selection_justification() -> str:
    """Returns the 3-5 sentence informal exchange argument correctness justification.

    Required by the assessment deliverable checklist.
    """
    return (
        "Correctness Justification (Informal Exchange Argument):\n"
        "Suppose an optimal schedule O exists that differs from our greedy schedule G. "
        "Let the first job in G be g_1 (the job with the earliest finishing time overall), "
        "and let the first job in O be o_1. Since g_1 finishes no later than o_1 by definition "
        "(finish(g_1) <= finish(o_1)), replacing o_1 with g_1 in O cannot create any conflict "
        "with any remaining jobs in O. This exchange produces a valid schedule O' of identical "
        "cardinality that shares the greedy choice g_1. Continuing this inductive replacement "
        "step for all subsequent non-conflicting jobs transforms O into G without reducing the total "
        "number of deliveries, proving that the greedy earliest-finish-time strategy is always optimal."
    )
