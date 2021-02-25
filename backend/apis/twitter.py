import random
import time

import tweepy
from twarc import Twarc

from apis.socialMedia import SocialMedia
from database.database import Collection, DBCollections
from enums.apiStructure import TwitterAPIAccess, TwitterAPIStructure
from enums.dbStructure import TwitterStructure, User
from utils.singleton import Singleton
from utils.utils_date import twitter_format
from enums.dbStructure import Structure
from utils.text_preprocessing import split_text_twitter

# Class Twitter is a Singleton. It maintains a connection with the Twitter API (Rest).
# Gets the information of the new user to follow (REST) and its last tweets published.
# Then, it listen for every other tweet publish by the user or comment made to one of its tweets (Streaming).
# This class structure the tweets and save them in the database.
class Twitter(SocialMedia, tweepy.StreamListener, metaclass=Singleton):

    # This method initializes Twitter class. Sets the connections with the REST API and with the API
    # used to retrieve comments. Also sets the connection with the database (setting the related db collection).
    def __init__(self):
        SocialMedia.__init__(self)
        tweepy.StreamListener.__init__(self)

        self.NAME = DBCollections.TWITTER.capitalize()

        # Twitter connection
        auth = tweepy.OAuthHandler(TwitterAPIAccess.AUTH[0], TwitterAPIAccess.AUTH[1])
        auth.set_access_token(TwitterAPIAccess.ACCESS_TOKEN[0], TwitterAPIAccess.ACCESS_TOKEN[1])

        # api rest
        self.twitterAPI = tweepy.API(auth, wait_on_rate_limit=True,
                                     wait_on_rate_limit_notify=True)
        # api for comments
        self.twitterComments = Twarc(TwitterAPIAccess.AUTH[0], TwitterAPIAccess.AUTH[1],
                                     TwitterAPIAccess.ACCESS_TOKEN[0], TwitterAPIAccess.ACCESS_TOKEN[1])

        # enums for the database structure and database collection related
        self.dbStructure = TwitterStructure()
        self.dbCollection = Collection(DBCollections.TWITTER)

        ## api streaming
        self.twitter_stream = tweepy.Stream(auth=auth, listener=self)
        self.STREAM_FILTER = []

    def get_account_information(self, username):
        user_info = self.twitterAPI.get_user(username)._json
        user_id = user_info[TwitterAPIStructure.USER[1]]

        account_information = {
            User.ID: user_id,
            User.NAME: username,
            User.SOCIAL_NETWORK: self.NAME.lower()
        }

        return account_information

    # This method gets the ID and the last 100 posts published by the user (account). If the user already exists in
    # the database, it recovers the posts published by the user since the last post saved in the database. It saves
    # the user information and the tweets in the database.
    def add_account(self, account_id):
        super().add_account(account_id)

        latest_post = self.dbCollection.get_latest_post(account_id)
        if latest_post is None:
            for status in tweepy.Cursor(self.twitterAPI.user_timeline, id=int(account_id),
                                        tweet_mode=TwitterAPIStructure.TWEET_MODE).items(300):
                post = self.__get_post_information(status._json)
                self.dbCollection.save_post(post[self.dbStructure.ID], status._json, post)
                time.sleep(random.randint(2, 5))
        else:
            since_tweetID = latest_post[self.dbStructure.ID]
            for status in tweepy.Cursor(self.twitterAPI.user_timeline, id=int(account_id), since_id=since_tweetID,
                                        tweet_mode=TwitterAPIStructure.TWEET_MODE).items():
                post = self.__get_post_information(status._json)
                self.dbCollection.save_post(post[self.dbStructure.ID], status._json, post)
                time.sleep(random.randint(2, 5))

        self.__add_to_stream(account_id)
        return True

    def remove_account(self, account_id):
        super().remove_account(account_id)
        self.__remove_of_stream(account_id)

    # This private method returns the original_post properly structured, ready to save in the database.
    def __get_post_information(self, original_post):
        print("     -> Structuring post...")
        return self.__structure_post(original_post, False)

    # This private method structures the original post. It takes into account whether the original_post is a comment.
    # If iscomment is True, the structured post will have 0 comments associated to it, and it will not have the
    # socialmedia field that indicates to which socialmedia belongs.
    def __structure_post(self, original_post, iscomment):
        hashtags = [hashtag[
                        TwitterAPIStructure.HASHTAGS[2]] for hashtag in
                    original_post[TwitterAPIStructure.HASHTAGS[0]][TwitterAPIStructure.HASHTAGS[1]]]

        account_id = original_post[TwitterAPIStructure.USER[0]][TwitterAPIStructure.USER[1]]

        post_text = original_post[TwitterAPIStructure.POST[0]] if TwitterAPIStructure.POST[
                                                                      0] in original_post else original_post[
            TwitterAPIStructure.POST[1]]

        new_post = {
            self.dbStructure.ID: original_post[TwitterAPIStructure.ID],
            self.dbStructure.USER: {
                User.ID: account_id,
                User.NAME: original_post[TwitterAPIStructure.USER[0]][
                    TwitterAPIStructure.USER[2]]
            },
            self.dbStructure.POST: {
                Structure.Post.ORIGINAL: post_text,
                Structure.Post.SPLITTED: split_text_twitter(post_text)
            },
            self.dbStructure.CREATION_TIME: twitter_format(
                original_post[TwitterAPIStructure.CREATION_TIME]),
            self.dbStructure.HASHTAGS: hashtags,
            self.dbStructure.MULTIMEDIA: self.__get_multimedia(original_post, iscomment),
            self.dbStructure.INTERACTIONS: self.__get_interaction(original_post, iscomment),
            self.dbStructure.UPDATE: False
        }

        if not iscomment:
            new_post[self.dbStructure.SOCIAL_NETWORK] = self.NAME

        return new_post

    # This private method returns the multimedia (links, images and videos) associated to the post.
    def __get_multimedia(self, original_post, iscomment):
        print("               -> Getting multimedia...") if iscomment else print("          -> Getting multimedia...")

        links = [link[
                     TwitterAPIStructure.LINK[2]] for link in
                 original_post[TwitterAPIStructure.LINK[0]][TwitterAPIStructure.LINK[1]]]

        if TwitterAPIStructure.IMAGE[0] in original_post:
            images = [
                image[TwitterAPIStructure.IMAGE[4]] for image in
                original_post[TwitterAPIStructure.IMAGE[0]][TwitterAPIStructure.IMAGE[1]] if
                image[TwitterAPIStructure.IMAGE[2]] == TwitterAPIStructure.IMAGE[3]
            ]
            videos = [
                video[TwitterAPIStructure.VIDEO[4]] for video in
                original_post[TwitterAPIStructure.VIDEO[0]][TwitterAPIStructure.VIDEO[1]] if
                video[TwitterAPIStructure.VIDEO[2]] == TwitterAPIStructure.VIDEO[3]
            ]
        else:
            images = []
            videos = []

        multimedia = {
            self.dbStructure.Multimedia.IMAGE: images,
            self.dbStructure.Multimedia.VIDEO: videos,
            self.dbStructure.Multimedia.LINK: links
        }

        return multimedia

    # This private method returns the interaction (comments, retweets and favorites) associated to the post.
    # If the post is a comment (iscomment==True), there will be no search for the replies to the post.
    def __get_interaction(self, original_post, iscomment):
        print("               -> Getting interaction...") if iscomment else print("          -> Getting interaction...")

        interaction = {
            self.dbStructure.TwitterInteractions.COMMENTS: 0,
            self.dbStructure.TwitterInteractions.RETWEETS: original_post[TwitterAPIStructure.RETWEETS],
            self.dbStructure.TwitterInteractions.FAVORITES: original_post[TwitterAPIStructure.FAVORITES]
        }

        if not iscomment:
            interaction[self.dbStructure.TwitterInteractions.COMMENTS] = self.__get_comments(original_post)

        return interaction

    # This private method searches for the replies made to the original_post using the Twarc API.
    # It structures each of the comments and returns a list of comments.
    def __get_comments(self, original_post):
        print("               -> Getting comments...")

        comments_unstructured = self.twitterComments.replies(original_post, False)

        comments = []
        for comment_x in comments_unstructured:
            if comment_x[TwitterAPIStructure.ID] != original_post[TwitterAPIStructure.ID]:
                comment = self.__structure_post(comment_x, True)
                comments.append(comment)

        return comments

    # This method structures the new comment and then it adds it to the comments list of the corresponding post.
    # If the comment is a reply for a post that is not in the database, the method gets this posts, structures it
    # and adds it to the database.
    def add_comment(self, new_comment):
        print("     -> Structuring new comment...")

        in_response_to = new_comment[TwitterAPIStructure.IN_RESPONSE_TO]

        main_post = self.dbCollection.get_post(in_response_to)

        comments = main_post[self.dbStructure.INTERACTIONS][
            self.dbStructure.TwitterInteractions.COMMENTS]

        comment = self.__structure_post(new_comment, iscomment=True)
        comments.append(comment)

        main_post[self.dbStructure.INTERACTIONS][
            self.dbStructure.TwitterInteractions.COMMENTS] = comments
        main_post[self.dbStructure.UPDATE] = True
        self.dbCollection.update_post(in_response_to, main_post)

    # This private method updates the number of retweets and favorites of each of the posts.
    # It gets the information of these posts with an api call (get_status / REST) and access to the retweets
    # and favorites fields.
    # It saves the updated posts in the database.
    def __update_posts(self, posts):
        print("     -> Updating new interactions...")

        for post in posts:
            post_again = self.twitterAPI.get_status(post[self.dbStructure.ID])

            # this only update #retweets and #favorites
            interaction_updated = {
                self.dbStructure.TwitterInteractions.COMMENTS:
                    post[self.dbStructure.INTERACTIONS][
                        self.dbStructure.TwitterInteractions.COMMENTS],
                self.dbStructure.TwitterInteractions.RETWEETS: post_again[
                    TwitterAPIStructure.RETWEETS],
                self.dbStructure.TwitterInteractions.FAVORITES: post_again[
                    TwitterAPIStructure.FAVORITES]
            }

            post[self.dbStructure.INTERACTIONS] = interaction_updated
            post[self.dbStructure.UPDATE] = False

            self.dbCollection.update_post(post[self.dbStructure.ID], post)

    def get_interaction_structure(self):
        return self.dbStructure.TwitterInteractions()

    def get_multimedia_structure(self):
        return self.dbStructure.Multimedia()

    # streaming on_status
    def on_status(self, status):
        tweet = status._json

        if tweet[TwitterAPIStructure.IN_RESPONSE_TO] is not None:
            self.add_comment(tweet)

    def __add_to_stream(self, account_id):
        self.STREAM_FILTER.append(account_id)
        self.twitter_stream.disconnect()
        self.twitter_stream.filter(follow=self.STREAM_FILTER, is_async=True)

    def __remove_of_stream(self, account_id):
        if account_id in self.STREAM_FILTER:
            self.STREAM_FILTER.remove(account_id)
            self.twitter_stream.disconnect()
            self.twitter_stream.filter(follow=self.STREAM_FILTER, is_async=True)
