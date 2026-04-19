from abc import ABC, abstractmethod
from typing import Any, Protocol

from app.application.dto.dto import BaseJobMessage


# JobQueuePort는 작업 메시지를 큐에 넣는 공통 인터페이스입니다.
# enqueue만 필수 구현이며, dequeue/size는 pull 방식 큐(Redis 등)에서만 의미가 있습니다.
class JobQueuePort(ABC):
    @abstractmethod
    def enqueue(self, message: BaseJobMessage) -> None:
        ...


# PullJobQueuePort는 pull 방식 큐(Redis 등)에서 메시지를 꺼낼 때 사용하는 확장 인터페이스입니다.
class PullJobQueuePort(JobQueuePort, ABC):
    @abstractmethod
    def dequeue(self) -> BaseJobMessage | None:
        ...

    @abstractmethod
    def size(self) -> int:
        ...


class ExtractedExperienceRepositoryPort(Protocol):
    def get_extracted_experiences(self, extracted_experience_id: int) -> list[dict[str, Any]]:
        ...
