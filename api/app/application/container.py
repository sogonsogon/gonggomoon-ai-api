from app.core.config import get_settings
from app.infrastructure.queue.redis_queue import RedisJobQueue
from app.infrastructure.db.session import create_session_factory
from app.infrastructure.db.extracted_experience_repository import SqlAlchemyExtractedExperienceRepository
from app.application.services.experiece_extraction_service import ExperienceExtractionService
from app.application.services.portfolio_strategy_generation_service import PortfolioStrategyGenerationService
from app.application.services.interview_strategy_generation_service import InterviewStrategyGenerationService
from app.application.services.post_analysis_service import PostAnalysisService

settings = get_settings()
session_factory = create_session_factory(settings.database_url)

##### API 서버 관련 의존성 주입 ######
queue = RedisJobQueue(
    redis_url=settings.redis_url,
    queue_key=settings.redis_queue_key,
)

extracted_experience_repository = SqlAlchemyExtractedExperienceRepository(session_factory=session_factory)

experience_extraction_service = ExperienceExtractionService(
    queue=queue,
    repository=extracted_experience_repository,
    callback_url=settings.call_back_url + "/experience-extraction"
)

portfolio_strategy_generation_service = PortfolioStrategyGenerationService(
    queue=queue,
    callback_url=settings.call_back_url + "/portfolio-strategy-generation"
)

interview_strategy_generation_service = InterviewStrategyGenerationService(
    queue=queue,
    callback_url=settings.call_back_url + "/interview-strategy-generation"
)

# NOTE : Post Analysis Service는 백오피스에서 사용할 예정이므로, 콜백 URL이 다릅니다.
post_analysis_service = PostAnalysisService(
    queue=queue,
    callback_url=settings.backoffice_callback_url + "/post-analysis"
)
