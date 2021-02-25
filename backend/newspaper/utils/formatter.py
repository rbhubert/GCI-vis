from newspaper.enums.newsItem import NewsItem


# Structures a new item, with its url, title, creation date and comments and emotions associated to it.
def format_newsItem(news_url, news_title, news_content, news_text, news_creation_time, comments, last_id_comment):
    newItem = {
        NewsItem.URL: news_url,
        NewsItem.TITLE: news_title,
        NewsItem.CONTENT_STRUCTURED: news_content,
        NewsItem.CONTENT_TEXT: news_text,
        NewsItem.CREATION_TIME: news_creation_time,
        NewsItem.COMMENTS: comments,
        NewsItem.LAST_COMMENT: last_id_comment
    }

    return newItem


def format_comment(comment_id, username, text, time_comment, likes, dislikes, replies=None):
    if replies is None:
        replies = []

    comment_struc = {
        NewsItem.Comments.ID: comment_id,
        NewsItem.Comments.TEXT: text,
        NewsItem.Comments.USERNAME: username,
        NewsItem.Comments.CREATION_TIME: time_comment,
        NewsItem.Comments.LIKES: likes,
        NewsItem.Comments.DISLIKES: dislikes,
        NewsItem.Comments.REPLIES: replies
    }

    return comment_struc
