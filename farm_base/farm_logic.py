import subprocess
import json
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from farm_instance.tasks import get_balance


class FarmLogic:
    def __init__(self):
        self.workers = {}

    def add_account(self, name):
        # TODO validate input data

        if name in self.workers:
            return False, "Worker already exists"

        worker_name = f"worker_{name}"
        queue_name = f"queue_{name}"

        worker_command = [
            "celery",
            "-A",
            "steamfarm",
            "worker",
            "--loglevel=info",
            f"--hostname={worker_name}",
            f"--queues={queue_name}",
        ]

        self.workers[worker_name] = subprocess.Popen(worker_command)

        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.SECONDS,
        )
        PeriodicTask.objects.create(
            interval=schedule,
            name=f"periodic_balance_check_{name}",
            task="farm_instance.tasks.get_balance",
            args=json.dumps([]),
            queue=queue_name,
        )

        return True, "Worker started"

    def remove_account(self, name):
        worker_name = f"worker_{name}"
        if worker_name not in self.workers:
            return False, "Worker not found"

        if self.workers[worker_name].poll() is not None:
            return False, "Worker is not running"

        self.workers[worker_name].terminate()
        self.workers[worker_name].wait()
        del self.workers[worker_name]

        PeriodicTask.objects.filter(
            name=f"periodic_balance_check_{name}",
        ).delete()

        return True, "Worker stopped"

    def workers_status(self):
        status_list = []
        for worker_name in self.workers:
            status = self.workers[worker_name].poll()
            status_list.append((worker_name, status))
        return True, status_list

    # def workers_status(self):
    #     print("Workers status:")
    #     for worker_name in self.workers:
    #         print(worker_name, self.workers[worker_name].poll())

    def test_task(self):
        get_balance.delay()
        return True, "Task started"
