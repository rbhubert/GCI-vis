import tldextract
import validators

from database.database import newspaperDB
from enums.dbStructure import NewspaperStructure
from newspaper.config.valid_newspapers import mapping_newspaper


def __check_url(url):
    valid = validators.url(url)
    if valid:
        str_page = tldextract.extract(url).domain
        valid_newspapers = mapping_newspaper.keys()
        if str_page in valid_newspapers:
            return mapping_newspaper[str_page]
    else:
        return None


def get_news_item(news_url):
    newspaper = __check_url(news_url)
    if newspaper is None:
        return False  # todo error message

    news_item = newspaperDB.get_news_item(news_url)

    if news_item is not None:  # news_item exists in db
        since_id = news_item[NewspaperStructure.LAST_COMMENT]
        new_comments = newspaper.get_latest_comments(since_id)

        if new_comments[1] == since_id:
            return news_item

        news_item[NewspaperStructure.COMMENTS].extend(new_comments[0])
        news_item[NewspaperStructure.LAST_COMMENT] = new_comments[1]
        newspaperDB.update_news_item(news_item)

        return news_item

    news_item = newspaper.get_newsItem(news_url)
    newspaperDB.add_news_item(news_item)
    return news_item


def search_news_comments(news_url):
    newspaper = __check_url(news_url)
    if newspaper is None:
        return False  # todo error message

    news_item = newspaperDB.get_news_item(news_url)
    if news_item is not None:  # newItem exists in db
        return False  # TODO error message
    else:
        since_id = news_item[NewspaperStructure.LAST_COMMENT]
        new_comments = newspaper.get_latest_comments(since_id)

        if new_comments[1] == since_id:
            return news_item

        news_item[NewspaperStructure.COMMENTS].extend(new_comments[0])
        news_item[NewspaperStructure.LAST_COMMENT] = new_comments[1]
        newspaperDB.update_news_item(news_item)


def get_comments(news_url):
    news_item = newspaperDB.get_news_item(news_url)
    if news_item is not None:  # newItem exists in db
        return news_item[NewspaperStructure.COMMENTS]

    return False  # TODO error message
