from django.core.paginator import Paginator

from logging_system.config.models import Settings

# reusable pagination function
# takes objs as array of objects to paginate
# takes page number
# returns objects per page
# example usage:
#
# from logging_system.functions import pagination
# page = pagination({objects array}, request.GET.get("page"))


def pagination(objs, page_number=1):
    items_per_page = Settings.load().items_per_page
    paginator = Paginator(objs, items_per_page)
    return paginator.get_page(page_number)


# reusable log message shortening function
# returns logs with added short_message field
# example usage:
#
# from logging_system.functions import logs_shor_message
# logs = logs_short_message({objects array}, length=50)


def logs_short_message(logs, length=50):
    for log in logs:
        if len(log.message) > 50:
            log.short_message = log.message[:length] + "..."
        else:
            log.short_message = log.message

    return logs
