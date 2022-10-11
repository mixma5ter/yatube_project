import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    dt_now = datetime.date.today()
    return {
        'year': dt_now.year
    }
