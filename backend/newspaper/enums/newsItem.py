# Fields for a newsItem.
class NewsItem:
    class Content:
        SECTION_TITLE = "section_title"
        IMAGE = "images"
        TEXT = "text"
        LINKS = "links"

    class Image:
        URL = "url"
        TEXT = "text"

    class Link:
        URL = "url"
        TEXT = "text"

    class Comments:
        ID = "id"
        USERNAME = "username"
        TEXT = "text"
        CREATION_TIME = "creation_time"
        LIKES = "likes"
        DISLIKES = "dislikes"
        REPLIES = "replies"

    URL = "url"
    TITLE = "title"
    CONTENT_STRUCTURED = "content_structured"
    CONTENT_TEXT = "content_text"
    CREATION_TIME = "creation_time"
    COMMENTS = "comments"
    LAST_COMMENT = "last_comment"
