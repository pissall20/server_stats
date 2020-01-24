import psutil


def get_cpu_stats():
    total_cpu_usage_time = dict(psutil.cpu_times()._asdict())
    n_cpu = psutil.cpu_count()
    cpu_ids = [f"cpu_{cpu_id}" for cpu_id in range(1, n_cpu + 1)]
    per_cpu_usage_time = list(
        map(
            lambda x, y: {
                "id": y,
                "user": x.user,
                "system": x.system,
                "idle": x.idle,
            },
            psutil.cpu_times(percpu=True),
            cpu_ids,
        )
    )

    total_cpu_usage_percent = psutil.cpu_percent()
    per_cpu_usage_percent_dict = [
        {"id": cpu_id, "percent": percent}
        for cpu_id, percent in zip(cpu_ids, psutil.cpu_percent(percpu=True))
    ]

    load_avg_dict = {
        k: v
        for k, v in zip(
            ["min_1", "min_5", "min_15"],
            [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()],
        )
    }

    return {
        "total_cpu_usage_time": total_cpu_usage_time,
        "total_cpu_usage_percent": total_cpu_usage_percent,
        "per_cpu_usage_time": per_cpu_usage_time,
        "per_cpu_usage_percent": per_cpu_usage_percent_dict,
        "load_avg": load_avg_dict,
    }