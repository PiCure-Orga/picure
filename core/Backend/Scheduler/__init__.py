from flask_apscheduler import APScheduler

_scheduler = None


def get_scheduler():
    global _scheduler
    if _scheduler is None:
        _scheduler = APScheduler()
    return _scheduler


scheduler = get_scheduler()
