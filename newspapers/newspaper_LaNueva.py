from contextlib import closing
from datetime import datetime

from selenium.webdriver import Firefox

from config import crawler
from newspapers import comments_FBPlugin
from utils.formatter import format_newsItem


# Scraps for the title and creationDate of the news for newspaper LaNueva.
def get_newsItem(news_url):
    # todo get content and text

    with closing(Firefox(firefox_options=crawler.firefox_options, executable_path=crawler.GECKODRIVER_PATH)) as browser:
        browser.get(news_url)

        title = browser.find_element_by_css_selector("h2[itemprop='headline']").get_attribute(
            "textContent")
        creation_time_str = browser.find_element_by_class_name("fecha").get_attribute(
            "textContent")
        creation_time = datetime.strptime(creation_time_str, "%d/%m/%Y | %H:%M |")

    comments = comments_FBPlugin.get_comments_FBPlugin(news_url)

    # todo get content and text
    return format_newsItem(news_url=news_url, news_title=title, news_content=[], news_text="",
                           news_creation_time=creation_time, comments=comments[0],
                           last_id_comment=comments[1])
