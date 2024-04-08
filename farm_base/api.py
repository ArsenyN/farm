from django.http import JsonResponse
from functools import wraps
from farm_base.farm_logic import FarmLogic


# wrapper
def handle_logic_operation(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            status, message = view_func(request, *args, **kwargs)
            if status:
                return JsonResponse({"status": "ok", "message": message})
            else:
                return JsonResponse({"status": "error", "message": message})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return wrapper


# requests handlers
farm_logic = FarmLogic()


@handle_logic_operation
def add_account(request):
    # TODO validate request

    return farm_logic.add_account(request.GET["name"])


@handle_logic_operation
def remove_account(request):
    # TODO validate request

    return farm_logic.remove_account(request.GET["name"])


@handle_logic_operation
def status(request):
    # TODO validate request

    return farm_logic.workers_status()


@handle_logic_operation
def test_task(request):
    return farm_logic.test_task()


"""
def add_account(request):
    # validate request

    # call farm_logic
    # try:
    # farm_logic.add_account(request.GET["name"])
    # except Exception as e:
    #     return JsonResponse({"status": "error", "message": str(e)})

    # return JsonResponse({"status": "ok"})

    try:
        status, message = farm_logic.add_account(request.GET["name"])
        if status:
            return JsonResponse({"status": "ok", "message": message})
        else:
            return JsonResponse({"status": "error", "message": message})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})



def remove_account(request):
    # validate request

    # call farm_logic
    # try:
    farm_logic.remove_account(request.GET["name"])
    # except Exception as e:
    #     return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "ok"})


def status(request):
    # validate request

    # call farm_logic
    farm_logic.workers_status()

    return JsonResponse({"status": "ok"})


def test_task(request):
    # validate request

    # call farm_logic
    farm_logic.test_task(request.GET["name"])
    # farm_logic.workers_status()

    return JsonResponse({"status": "ok"})
"""
