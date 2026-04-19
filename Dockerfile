FROM python:3.12-slim

# 보안: 非root 사용자로 실행
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# 의존성만 먼저 복사해서 레이어 캐시 활용
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 복사
COPY api/ .

# Cloud Run은 PORT 환경변수를 주입함 (기본 8080)
ENV PORT=8080

USER appuser

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
