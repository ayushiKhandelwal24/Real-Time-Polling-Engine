from pydantic import BaseModel
from typing import List

class PollCreate(BaseModel):
    title: str
    choices: List[str]

class VoteCreate(BaseModel):
    poll_id: int
    choice_id: int
    voter_fingerprint: str

class ChoiceResponse(BaseModel):
    id: int
    text: str
    votes: int

    class Config:
        from_attributes = True

class PollResponse(BaseModel):
    id: int
    title: str
    choices: List[ChoiceResponse]

    class Config:
        from_attributes = True