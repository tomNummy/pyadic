from __future__ import annotations

import datetime
import re
from collections import Counter
from typing import List, Optional, Union

from pydantic import BaseModel


class Person(BaseModel):
    name: str


class Message(BaseModel):
    sender: Optional[Person]
    text: str
    recipient: Optional[Person]
    start_time: Union[datetime.datetime, datetime.time]
    end_time: Optional[Union[datetime.datetime, datetime.time]] = None
    predecessor: Optional[Message] = None

    @property
    def duration(self) -> datetime.timedelta:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time

    def get_words(self):
        return re.findall(r"\w+", self.text)

    @property
    def word_count(self) -> int:
        return len(self.get_words())


class Conversation(BaseModel):
    messages: List[Message]

    @property
    def people(self) -> set:
        return (
            set([m.sender for m in self.messages]) &
            set([m.recipient for m in self.messages])
        )

    def get_people_freqs(self, normalized: bool = True) -> dict:
        c = Counter([m.sender.name for m in self.messages if m.sender])
        if normalized:
            total = sum(c.values())
            return {x: y / total for x, y in c.items()}
        return dict(c)


Message.update_forward_refs()
Conversation.update_forward_refs()
