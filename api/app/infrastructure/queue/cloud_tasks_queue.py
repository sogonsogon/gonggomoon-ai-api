from google.cloud import tasks_v2

from app.application.dto.dto import BaseJobMessage
from app.application.ports.ports import JobQueuePort


class CloudTasksJobQueue(JobQueuePort):
    """
    Google Cloud Tasks 기반의 push 방식 큐 구현체.
    enqueue 시 Cloud Tasks가 worker_url로 HTTP POST 요청을 보냅니다.
    """

    def __init__(
        self,
        project: str,
        location: str,
        queue_name: str,
        worker_url: str,
        service_account_email: str | None = None,
        internal_api_key: str | None = None,
    ) -> None:
        self.client = tasks_v2.CloudTasksClient()
        self.parent = self.client.queue_path(project, location, queue_name)
        self.worker_url = worker_url
        self.service_account_email = service_account_email
        self.internal_api_key = internal_api_key

    def enqueue(self, message: BaseJobMessage) -> None:
        payload = message.model_dump_json().encode("utf-8")

        headers = {"Content-Type": "application/json"}
        if self.internal_api_key:
            headers["x-internal-api-key"] = self.internal_api_key

        http_request: dict = {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": self.worker_url,
            "headers": headers,
            "body": payload,
        }

        # OIDC 토큰을 통해 worker 엔드포인트 인증 (Cloud Run 등에서 권장)
        if self.service_account_email:
            http_request["oidc_token"] = {
                "service_account_email": self.service_account_email,
                "audience": self.worker_url,
            }

        task = {"http_request": http_request}

        self.client.create_task(parent=self.parent, task=task)
