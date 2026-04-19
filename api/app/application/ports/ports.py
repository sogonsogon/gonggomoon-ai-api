from typing import Any, Protocol

from app.application.dto.dto import BaseJobMessage


# JobQueuePort는 작업 메시지를 큐에 넣고 빼는 인터페이스를 정의합니다.
class JobQueuePort:
    def enqueue(self, message: BaseJobMessage) -> None:
        raise NotImplementedError

    def dequeue(self) -> BaseJobMessage | None:
        raise NotImplementedError

    def size(self) -> int:
        raise NotImplementedError


class ExtractedExperienceRepositoryPort(Protocol):
    def get_extracted_experiences(self, extracted_experience_id: int) -> list[dict[str, Any]]:
        ...
