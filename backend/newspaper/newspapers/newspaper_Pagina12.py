from contextlib import closing
from datetime import datetime

from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait

from newspaper.config import crawler
from newspaper.utils.formatter import format_newsItem, format_comment


# Scraps the webpage _news_url_ and get all the comments associated to this news
def get_newsItem(news_url):
    with closing(Firefox(firefox_options=crawler.firefox_options,
                         executable_path=crawler.GECKODRIVER_PATH)) as browser:
        browser.get(news_url)

        title = browser.find_element_by_class_name("article-title").get_attribute(
            "textContent")
        creation_time_str = browser.find_element_by_class_name("time").find_element_by_tag_name("span").get_attribute(
            "datetime")
        creation_time = datetime.strptime(creation_time_str, "%Y-%m-%d")

    comments_url = "https://talk.pagina12.com.ar/embed/stream?asset_id=" + news_url.split("-")[0].split("/")[
        -1] + "&asset_url=" + news_url
    pairResult = __getComments_Pagina12(comments_url, None)
    comments_Pagina12 = pairResult[0]
    last_id_comment = pairResult[1]

    # TODO new content, new text
    return format_newsItem(news_url=news_url, news_title=title, news_content=[], news_text="",
                           news_creation_time=creation_time, comments=comments_Pagina12,
                           last_id_comment=last_id_comment)


# Gets the latest comments made in the newsItem (since since_id)
def get_latest_comments(url, since_id):
    comments = __getComments_Pagina12(url,
                                      since_id)
    return comments


# Scrap the comments_url to get the comments made in the news
def __getComments_Pagina12(comments_url, since_id=None):
    comments_Pagina12 = []

    with closing(Firefox(firefox_options=crawler.firefox_options,
                         executable_path=crawler.GECKODRIVER_PATH)) as browser:
        wait = WebDriverWait(browser, timeout=10)

        browser.get(comments_url)

        while True:
            try:
                more_button = wait.until(
                    lambda x: browser.find_element_by_xpath(
                        "/html/body/div[1]/div/div[2]/div/div/div/div[3]/div[2]/div/div/div/div/div[3]/button"))
                more_button.click()
            except TimeoutException:
                break
            except ElementNotInteractableException:
                break

        last_id_comment = ""
        comments_section = browser.find_element_by_class_name("embed__stream")
        comments = comments_section.find_elements_by_class_name("talk-stream-comment-wrapper")

        for comment_body in comments:
            comment_id = comment_body.get_attribute("id")
            if last_id_comment == "":
                last_id_comment = comment_id

            if comment_id == since_id:
                break

            text = comment_body.find_element_by_class_name("talk-plugin-rich-text-text").get_attribute(
                "textContent")  # text
            likes = comment_body.find_element_by_class_name("talk-plugin-respect-count").get_attribute(
                "textContent")
            likes = int(likes) if likes != '' else 0  # pos
            time_str = \
                comment_body.find_element_by_class_name("talk-stream-comment-published-date").find_elements_by_tag_name(
                    "span")[0].get_attribute("title")
            time_comment = datetime.strptime(time_str, "%d/%m/%Y %H:%M:%S")

            # TODO username... and improve comments
            comment_struc = format_comment(comment_id=comment_id, username="", text=text, time_comment=time_comment,
                                           likes=likes, dislikes=0)

            if "talk-stream-comment-wrapper-level-0" in comment_body.get_attribute("class"):
                comments_Pagina12.append(comment_struc)
            else:
                comments_Pagina12[-1]["replies"].append(comment_struc)

    return comments_Pagina12, last_id_comment
