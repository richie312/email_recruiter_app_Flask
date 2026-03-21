FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends cron && rm -rf /var/lib/apt/lists/*

COPY email-agent-tests/requirements.txt /tmp/helper-requirements.txt
RUN pip install --no-cache-dir -r /tmp/helper-requirements.txt

COPY email-agent-tests /app/email-agent-tests
COPY email-agent-tests/docker/start_helper_service.sh /app/start_helper_service.sh

RUN chmod +x /app/start_helper_service.sh

CMD ["/app/start_helper_service.sh"]
