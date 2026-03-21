#!/bin/sh
set -eu

CRON_SCHEDULE="${JOB_SCRAPER_CRON:-0 * * * *}"
PYTHON_BIN="${PYTHON_BIN:-python}"
SCRIPT_PATH="/app/email-agent-tests/run_scrape_job.py"
LOG_PATH="/var/log/job-scraper.log"

touch "${LOG_PATH}"

cat <<EOF >/etc/cron.d/job-scraper
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
${CRON_SCHEDULE} cd /app/email-agent-tests && ${PYTHON_BIN} ${SCRIPT_PATH} >> ${LOG_PATH} 2>&1
EOF

chmod 0644 /etc/cron.d/job-scraper
crontab /etc/cron.d/job-scraper

cron
tail -f "${LOG_PATH}"
