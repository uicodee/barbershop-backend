from apscheduler_di import ContextSchedulerDecorator


def get_scheduler() -> ContextSchedulerDecorator:
    raise NotImplementedError
