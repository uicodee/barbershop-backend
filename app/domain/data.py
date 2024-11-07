from apscheduler.jobstores.redis import RedisJobStore

job_stores = {
    "default": RedisJobStore(
        jobs_key="scheduled_haircuts_jobs", run_times_key="scheduled_haircuts_run_times",
        host="localhost", port=6379
    )
}
