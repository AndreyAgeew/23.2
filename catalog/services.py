from django.core.cache import cache

from catalog.models import Category


def get_categories():
    # Сначала попробуйте получить данные из кеша
    categories = cache.get('categories')

    # Если данные не найдены в кеше, выполните выборку из базы данных
    if categories is None:
        categories = Category.objects.all()

        # Сохраните результаты выборки в кеше на определенное время (например, на 1 час)
        cache.set('categories', categories, 3600)

    return categories
