from datetime import datetime


def start_cron_job_notes_in_minutes():
    start_job_date = datetime(year=datetime.today().year,
                              month=datetime.today().month,
                              day=datetime.today().day + 1,
                              hour=7, minute=0, second=0)
    datetime_now = datetime.now()

    diff = start_job_date - datetime_now
    return diff.seconds / 60


# def cron_job_notes_recall():
#     data = query_user_notes()
#     if data:
#         data_to_send = preapare_data_for_sending(data)
#         result = send_email(data_to_send, nginx_host=app.config.get("NGINX_HOST"))
#         if result:
#             logging.error("mail sent successfully")
#         else:
#             logging.error("sending mail failed")
#     else:
#         logging.info("CRON::: no data to send")