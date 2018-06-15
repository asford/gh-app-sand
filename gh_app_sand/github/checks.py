from typing import Optional

import attr
import enum

class Status(enum.Enum):
    queued = "queued"
    in_progress = "in_progress"
    completed = "completed"

class Conclusion(enum.Enum):
    success = "success"
    failure = "failure"
    neutral = "neutral"
    cancelled = "cancelled"
    timed_out = "timed_out"
    action_required = "action_required"

@attr.s(auto_attribs=True)
class Output:
    title: str
    summary: str
    text: Optional[str] = None
    #annotations: List[Annotation]
    #images: List[Image]

@attr.s(auto_attribs=True)
class RunDetails:
    """Check run input parameters from: https://developer.github.com/v3/checks/runs/"""
    name: str
    id: Optional[str] = None
    head_sha: Optional[str] = None
    head_branch: Optional[str] = None
    details_url: Optional[str] = None
    external_id: Optional[str] = None
    status: Optional[Status] = None
    started_at: Optional[str] = None
    conclusion: Optional[Conclusion] = None
    completed_at: Optional[str] = None
    output: Optional[Output] = None
    # actions: typing.List[CheckActions]

@attr.s(auto_attribs=True)
class CreateRun:
    """Check run input parameters from: https://developer.github.com/v3/checks/runs/"""
    owner: str
    repo: str
    run: RunDetails

@attr.s(auto_attribs=True)
class UpdateRun:
    """Check run input parameters from: https://developer.github.com/v3/checks/runs/"""
    owner: str
    repo: str
    id: str
    run: RunDetails
