from __future__ import annotations

import os

from typing import Optional, Any, List, Union
from dataclasses import dataclass

from requests import get, post, patch


@dataclass
class YouTuberObject:
    id: int
    url: str
    username: str


class YouTuber(YouTuberObject):

    def __init__(self: YouTuber, telegram_user_object: YouTuberObject) -> None:
        for attribute in dir(telegram_user_object):
            if attribute.startswith('__'):
                continue

            self.__setattr__(attribute, telegram_user_object.__getattribute__(attribute), update=False)

    def __repr__(self: YouTuber) -> str:
        return f"{self.__class__.__name__}: {self.id}" if self.id else f"{self.__class__.__name__}: Undefiend"

    def __setattr__(self: YouTuber, __name: str, __value: Any, update: bool = True) -> None:
        if update:
            patch(
                f"http://{os.environ['IP']}:8000/api/v1/youtuber/{self.id}",
                data={__name: __value}
            )

        super().__setattr__(__name, __value)
        
    @staticmethod
    def get(id: int = None) -> Union[YouTuber, List[YouTuber], None]:
        if id is None:
            users = get(f"http://{os.environ['IP']}:8000/api/v1/youtubers").json()
            return [YouTuber(YouTuberObject(**user)) for user in users]

        user = get(
            f"http://{os.environ['IP']}:8000/api/v1/youtuber/{id}"
        ).json()

        if isinstance(user, list) and len(user) == 0:
            return None

        if isinstance(user, dict) and any((user.get('detail'), user.get('details'))):
            return None

        return YouTuber(
            YouTuberObject(
                **(user[0] if isinstance(user, list) else user)
            )
        )

    @staticmethod
    def create(username: str, url: str) -> YouTuber:
        user = get(
            f"http://{os.environ['IP']}:8000/api/v1/youtubers?url={url}"
        ).json()

        if isinstance(user, list) and len(user) != 0:
            return None

        if isinstance(user, dict) and any((user.get('detail'), user.get('details'))):
            return None

        user = post(
            f"http://{os.environ['IP']}:8000/api/v1/youtubers", 
            json={'username': username, 'url': url}
        ).json()

        return YouTuber(
            YouTuberObject(
                **(user[0] if isinstance(user, list) else user)
            )
        )
