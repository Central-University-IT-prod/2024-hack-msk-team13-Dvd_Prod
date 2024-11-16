from typing import Protocol


class Commitable(Protocol):
    async def commit(self) -> None: ...