import requests
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def cron_job_notes_recall():
    try:
        r = requests.get(f'http://172.28.1.3/notes/test_start_cron_job')
        logging.info(f":::__job__.py::: request status {r.text}")
    except Exception as e:
        logging.error(f":::__job__.py::: error msg: {e}")

    return r.text