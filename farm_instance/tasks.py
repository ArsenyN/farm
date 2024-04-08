import time
import random
from celery import shared_task


@shared_task
def get_balance():
    print("get_balance")
    # time.sleep(random.randint(1, 5))
    return 0
