import time
from contextlib import closing
from datetime import datetime

from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException, \
    ElementNotVisibleException, StaleElementReferenceException
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait

from newspaper.config import crawler
from newspaper.enums.newsItem import NewsItem
from newspaper.utils.formatter import format_newsItem, format_comment
from newspaper.utils.utilsDate import get_past_date


# Scraps the webpage _news_url_ and get all the comments associated to this new.
def get_newsItem(news_url):
    with closing(Firefox(firefox_options=crawler.firefox_options,
                         executable_path=crawler.GECKODRIVER_PATH)) as browser:
        browser.get(news_url)

        title = browser.find_element_by_class_name("detailHeadline").get_attribute("textContent")
        creation_time_str = \
            browser.find_element_by_class_name("timeStamp").get_attribute("textContent").split("Posted:")[1].split("|")[
                0].strip()[:-3]

        # Posted: Feb 23, 2020 7:06 PM MT ///// MT or AT... or other...
        creation_time = datetime.strptime(creation_time_str, '%b %d, %Y %H:%M %p')
        bodyContent_raw = browser.find_element_by_class_name("story")
        bodyContent_structured = __get_content_formatted(bodyContent_raw)
        bodyContent_text = __get_content_text(bodyContent_structured)

        pairResult = __getComments_CBC(browser, creation_time, None)

    # pairResult = __getComments_CBC(news_url, creation_time, None)
    comments_CBC = pairResult[0]
    last_id_comment = pairResult[1]

    return format_newsItem(news_url=news_url, news_title=title, news_content=bodyContent_structured,
                           news_text=bodyContent_text,
                           news_creation_time=creation_time,
                           comments=comments_CBC, last_id_comment=last_id_comment)


# Gets the latest comments made in the newItem (since since_id)
def get_latest_comments(newItem, since_id):
    comments = __getComments_CBC(newItem[NewsItem.URL], newItem[NewsItem.CREATION_TIME],
                                 since_id)
    return comments


# Scrap the comments_url to get the comments made in the news
def __getComments_CBC(browser, creation_time, since_id=None):
    comments_CBC = []
    wait = WebDriverWait(browser, timeout=10)

    # scroll to the bottom
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)

    # remove cookie notification to be able to click de load-more-comments button.
    try:
        noticeButton = wait.until(
            lambda x: browser.find_element_by_class_name("noticeButton"))
        noticeButton.click()
    except TimeoutException:
        pass
    except ElementNotInteractableException:
        pass

    try:
        wait.until(
            lambda x: browser.find_element_by_class_name("vf-comments"))
    except TimeoutException:
        pass
    except ElementNotInteractableException:
        pass

    while True:
        try:
            more_button = wait.until(
                lambda x: browser.find_element_by_css_selector(".vf-load-more"))
            # more_button = browser.find_element_by_css_selector(".vf-load-more")
            browser.execute_script("arguments[0].scrollIntoView(true);", more_button)
            time.sleep(2)
            more_button.click()
        except NoSuchElementException:
            break
        except TimeoutException:
            break
        except ElementNotInteractableException:
            break

    last_id_comment = ""
    comments_section = browser.find_elements_by_class_name("vf-comment-thread")

    for comment_body in comments_section:
        comment_id = __get_comment_id(comment_body)
        if last_id_comment == "":
            last_id_comment = comment_id

        if comment_id == since_id:
            break

        username = __get_username(comment_body)
        text_body = __get_text(comment_body)
        likes = __get_likes(comment_body)
        dislikes = __get_dislikes(comment_body)
        time_comment = __get_time(comment_body, creation_time)

        # search for load-more-button in replies section...

        try:
            more_replies_section = comment_body.find_element_by_class_name("vf-comment-replies")
            # if "hidden" not in more_replies_section.get_attribute("class"):
            if more_replies_section.is_displayed():
                while True:
                    more_replies_button = wait.until(
                        lambda x: more_replies_section.find_element_by_class_name("vf-replies-button"))
                    more_replies_button.click()
        except NoSuchElementException:
            pass
        except TimeoutException:
            pass
        except ElementNotVisibleException:
            pass
        except ElementNotInteractableException:
            pass
        except StaleElementReferenceException:
            pass

        replies = []

        try:
            replies_list = comment_body.find_element_by_class_name("vf-child-comments")
            replies_list = replies_list.find_elements_by_class_name("vf-comment-container")
            # comments chain...
            for reply_body in replies_list:
                reply_id = reply_body.get_attribute("data-id")
                reply_username = __get_username(reply_body)
                reply_text = __get_text(reply_body)
                reply_likes = __get_likes(reply_body)
                reply_dislikes = __get_dislikes(reply_body)
                reply_time = __get_time(reply_body, creation_time)

                reply_structured = format_comment(comment_id=reply_id, username=reply_username, text=reply_text,
                                                  time_comment=reply_time, likes=reply_likes, dislikes=reply_dislikes)
                replies.append(reply_structured)
        except NoSuchElementException:
            pass

        comment_struc = format_comment(comment_id=comment_id, username=username, text=text_body,
                                       time_comment=time_comment, likes=likes, dislikes=dislikes, replies=replies)
        comments_CBC.append(comment_struc)

    return comments_CBC, last_id_comment


def __get_comment_id(comment_body):
    return comment_body.find_element_by_class_name("vf-comment-container").get_attribute("data-id")


def __get_username(comment_body):
    return comment_body.find_element_by_class_name("vf-comment-username").get_attribute("textContent")


def __get_text(comment_body):
    return comment_body.find_element_by_class_name("vf-comment-html-content").get_attribute(
        "textContent")  # text


def __get_likes(comment_body):
    return int(comment_body.find_element_by_class_name("vf-count-likes").get_attribute("textContent"))  # pos


def __get_dislikes(comment_body):
    return 0  # CBC do not have dislikes in its comments (for now)


def __get_time(comment_body, creation_time):
    time_str = comment_body.find_element_by_class_name("vf-date").get_attribute(
        "textContent").strip()
    return get_past_date(creation_time, time_str)


def __get_content_formatted(body_content):
    child_elements = body_content.find_element_by_tag_name("span").find_elements_by_xpath("*")

    content_structured = []
    current_section = {
        NewsItem.Content.SECTION_TITLE: "First section",
        NewsItem.Content.TEXT: "",
        NewsItem.Content.IMAGE: [],
        NewsItem.Content.LINKS: []
    }

    for child_element in child_elements:
        if child_element.tag_name == "div":  # images or links...
            child_text = child_element.get_attribute("textContent")
            if "MORE TOP STORIES" in child_text:
                break

            # check if image
            possible_image = child_element.find_elements_by_class_name("imageMedia")
            if possible_image:
                p_image_url = possible_image[0].find_element_by_tag_name("img").get_attribute("src")
                p_image_description = possible_image[0].find_element_by_tag_name("figcaption").get_attribute(
                    "textContent")
                image = {
                    NewsItem.Image.URL: p_image_url,
                    NewsItem.Image.TEXT: p_image_description
                }
                current_section[NewsItem.Content.IMAGE].append(image)
            else:
                possible_links = child_element.find_elements_by_tag_name("a")
                for p_link in possible_links:
                    link = {
                        NewsItem.Link.URL: p_link.get_attribute("href"),
                        NewsItem.Link.TEXT: p_link.get_attribute("textContent")
                    }

                    current_section[NewsItem.Content.LINKS].append(link)

        elif child_element.tag_name == "p":
            current_section[NewsItem.Content.TEXT] += child_element.get_attribute("textContent")

            # checks if there are links in this <p>
            possible_links = child_element.find_elements_by_tag_name("a")
            for p_link in possible_links:
                link = {
                    NewsItem.Link.URL: p_link.get_attribute("href"),
                    NewsItem.Link.TEXT: p_link.get_attribute("textContent")
                }

                current_section[NewsItem.Content.LINKS].append(link)
        elif child_element.tag_name == "h2":  # new section
            child_text = child_element.get_attribute("textContent")
            content_structured.append(current_section)
            current_section = {
                NewsItem.Content.SECTION_TITLE: child_text,
                NewsItem.Content.TEXT: "",
                NewsItem.Content.IMAGE: [],
                NewsItem.Content.LINKS: []
            }

    content_structured.append(current_section)
    return content_structured


# return just content...
def __get_content_text(structured_content):
    # content (formatted) is just a list of sections...

    text = ""
    for section in structured_content:
        text += section[NewsItem.Content.TEXT]

    return text
