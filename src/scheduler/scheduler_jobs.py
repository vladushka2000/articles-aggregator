import datetime

from services import article_service


async def update_popular_articles(
    popular_article_lifetime_in_seconds: int, articles_num: int
) -> None:
    """
    Обновить список самых популярных статей
    :param popular_article_lifetime_in_seconds: время жизни популярных статей в секундах
    :param articles_num: количество статей для обновления
    """

    current_date = datetime.datetime.now()
    date_from = current_date - datetime.timedelta(
        seconds=popular_article_lifetime_in_seconds
    )

    await article_service.ArticleService.update_popular_articles(
        date_from, articles_num
    )
