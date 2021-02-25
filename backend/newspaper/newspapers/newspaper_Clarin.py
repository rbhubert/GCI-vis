from contextlib import closing
from datetime import datetime, timedelta

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

        title = browser.find_element_by_id("title").get_attribute("textContent")
        creation_time_section = browser.find_element_by_class_name("breadcrumb").find_element_by_tag_name("span")
        creation_time_str = creation_time_section.get_attribute("textContent").strip()
        creation_time = datetime.strptime(creation_time_str, "%d/%m/%Y - %H:%M")

    pairResult = __getComments_Clarin(news_url, creation_time=creation_time)
    comments_Clarin = pairResult[0]
    last_id_comment = pairResult[1]

    # todo content and text
    return format_newsItem(news_url=news_url, news_title=title, news_content=[], news_text="",
                           news_creation_time=creation_time,
                           comments=comments_Clarin, last_id_comment=last_id_comment)


# Gets the latest comments made in the newsItem (since since_id)
def get_latest_comments(url, since_id):
    comments = __getComments_Clarin(url,
                                    since_id=since_id)
    return comments


# Scrap the comments_url to get the comments made in the news
def __getComments_Clarin(comments_url, creation_time=None, since_id=None):
    comments_Clarin = []

    with closing(Firefox(firefox_options=crawler.firefox_options,
                         executable_path=crawler.GECKODRIVER_PATH)) as browser:
        wait = WebDriverWait(browser, timeout=10)

        browser.get(comments_url)
        if not creation_time:
            creation_time_section = browser.find_element_by_class_name("breadcrumb").find_element_by_tag_name("span")
            creation_time_str = creation_time_section.get_attribute("textContent").strip()
            creation_time = datetime.strptime(creation_time_str, "%d/%m/%Y - %H:%M")

        try:
            activate_button = wait.until(
                lambda x: browser.find_element_by_id("activateComments"))
            activate_button.click()
        except TimeoutException:
            pass
        except ElementNotInteractableException:
            pass

        while True:
            try:
                more_button = wait.until(
                    lambda x: browser.find_element_by_class_name("gig-comments-more"))
                more_button.click()
            except TimeoutException:
                break
            except ElementNotInteractableException:
                break

        wait.until(lambda comments: browser.find_elements_by_class_name("gig-comment"))

        last_id_comment = ""
        comments = browser.find_elements_by_class_name("gig-comment")

        for comment_body in comments:
            comment_id = comment_body.get_attribute("data-comment-id")
            if last_id_comment == "":
                last_id_comment = comment_id

            if comment_id == since_id:
                break

            text = comment_body.find_element_by_class_name("gig-comment-body").get_attribute("textContent")  # text
            likes = int(
                comment_body.find_element_by_class_name("gig-comment-vote-pos").get_attribute("textContent"))  # pos
            dislikes = int(
                comment_body.find_element_by_class_name("gig-comment-vote-neg").get_attribute("textContent"))  # neg
            time_str = comment_body.find_element_by_class_name("gig-comment-time").get_attribute(
                "textContent").split()  # time

            if len(time_str) > 3:
                time_comment = creation_time
            else:
                time_number = int(time_str[1])
                time_lapse = time_str[2]
                if time_lapse[0] == "m":  # m(inutes)
                    time_comment = creation_time
                else:  # time_lapse[0] == "d" # d(days)
                    time_comment = datetime.today() - timedelta(days=time_number)

            # todo username and improve comments... all thread...
            comment_struc = format_comment(comment_id=comment_id, username="", text=text, time_comment=time_comment,
                                           likes=likes, dislikes=dislikes)

            level = int(comment_body.get_attribute("data-level"))
            if level == 0:
                comments_Clarin.append(comment_struc)
            else:
                comments_Clarin[-1]["replies"].append(comment_struc)

    return comments_Clarin, last_id_comment
