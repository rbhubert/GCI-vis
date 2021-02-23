import time

import tweepy
from twarc import Twarc

from apis.socialMedia import SocialMedia
from database.database import Collection, DBCollections
from enums.apiStructure import TwitterAPIAccess, TwitterAPIStructure
from enums.dbStructure import TwitterStructure, User, Post
from utils.getEmotions import get_emotions
from utils.singleton import Singleton
from utils.textPreprocessing import split_text
from utils.utilsDate import twitter_format


# Class Twitter is a Singleton. It maintains a connection with the Twitter API (Rest and Streaming).
# Gets the information of the new user to follow (REST) and its last tweets published.
# Then, it listen for every other tweet publish by the user or comment made to one of its tweets (Streaming).
# This class structure the tweets and save them in the database.
class Twitter(SocialMedia, metaclass=Singleton):
    # StreamListerer listens for any tweet published by any of the users in the STREAM_FILTER list, or for any
    # comments made in one of the tweets of any of the users in the STREAM_FILTER list.
    # class StreamListener(tweepy.StreamListener):
    #     def __init__(self, outerclass):
    #         super().__init__()
    #         self.outerclass = outerclass
    #
    #     def on_status(self, status):
    #         tweet = status._json
    #
    #         if tweet[TwitterAPIStructure.IN_RESPONSE_TO] is not None:
    #             self.outerclass._add_comment(tweet)
    #
    #             # TODO identify new post made by user...

    # This method initializes Twitter class. Sets the connections with the REST and Streaming API's and with the API
    # used to retrieve comments. Also sets the connection with the database (setting the db collection related).
    def __init__(self):
        super().__init__()

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

        # api streaming
        # self.streamListener = self.StreamListener(self)
        # self.twitterStream = tweepy.Stream(auth=auth, listener=self.streamListener)
        # self.STREAM_FILTER = []

        # enums for the database structure and database collection related
        self.dbStructure = TwitterStructure()
        self.dbCollection = Collection(DBCollections.TWITTER)

    def get_accountInformation(self, username):
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
    # the user information and the tweets in the database. It adds the user to the STREAM_FILTER list (streaming).
    def add_account(self, accountID):
        super().add_account(accountID)

        latest_post = self.dbCollection.get_latest_post(accountID)
        if latest_post is None:
            for status in tweepy.Cursor(self.twitterAPI.user_timeline, id=int(accountID),
                                        tweet_mode=TwitterAPIStructure.TWEET_MODE).items(300):
                post = self.__get_post_information(status._json)
                self.dbCollection.save_post(post[self.dbStructure.ID], status._json, post)
                time.sleep(5) # todo change to sleep random between 2 y 5
        else:
            since_tweetID = latest_post[self.dbStructure.ID]
            for status in tweepy.Cursor(self.twitterAPI.user_timeline, id=int(accountID), since_id=since_tweetID,
                                        tweet_mode=TwitterAPIStructure.TWEET_MODE).items():
                post = self.__get_post_information(status._json)
                self.dbCollection.save_post(post[self.dbStructure.ID], status._json, post)
                time.sleep(5)

        # add the user to the streaming
        # self.STREAM_FILTER.append(accountID)
        # self.twitterStream.disconnect()
        # self.twitterStream.filter(follow=self.STREAM_FILTER, is_async=True)

        return True

    # This method removes the user from the streaming
    def remove_account(self, accountID):
        super().remove_account(accountID)

        # if accountID in self.STREAM_FILTER:
        #    self.STREAM_FILTER.remove(accountID)
        #    self.twitterStream.disconnect()
        #    self.twitterStream.filter(follow=self.STREAM_FILTER, is_async=True)

        return True

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
                Post.ORIGINAL: post_text,
                Post.SPLITTED: split_text(post_text)
            },
            self.dbStructure.CREATION_TIME: twitter_format(
                original_post[TwitterAPIStructure.CREATION_TIME]),
            self.dbStructure.HASHTAGS: hashtags,
            self.dbStructure.MULTIMEDIA: self.__get_multimedia(original_post, iscomment),
            self.dbStructure.INTERACTIONS: self.__get_interaction(original_post, iscomment),
            self.dbStructure.EMOTIONS: {},
            self.dbStructure.UPDATE: False
        }

        if not iscomment:
            new_post[self.dbStructure.SOCIAL_NETWORK] = self.NAME

        new_post[self.dbStructure.EMOTIONS] = get_emotions(new_post, self.dbStructure, iscomment)

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

    # This private method searchs for the replies made to the original_post using the Twarc API.
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

        # TODO what if new_comment is a reply to a tweet not-saved in DB? We have to retrieve and save it in the DB
        #  before trying to save the reply

        # TODO we also have to update the emotions values of the main post...
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

            # this search for all comments all over again...
            # interaction_updated = self.__get_interaction(post_again, False)

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

    def getInteractionStructure(self):
        return self.dbStructure.TwitterInteractions()

    def getMultimediaStructure(self):
        return self.dbStructure.Multimedia()


class TwitterStreaming(tweepy.StreamListener, metaclass=Singleton):
    twitter = Twitter()

    def __init__(self, ):
        super().__init__()

        # Twitter connection
        auth = tweepy.OAuthHandler(TwitterAPIAccess.AUTH[0], TwitterAPIAccess.AUTH[1])
        auth.set_access_token(TwitterAPIAccess.ACCESS_TOKEN[0], TwitterAPIAccess.ACCESS_TOKEN[1])

        # api streaming
        self.twitterStream = tweepy.Stream(auth=auth, listener=self)
        self.STREAM_FILTER = []

    def on_status(self, status):
        tweet = status._json

        if tweet[TwitterAPIStructure.IN_RESPONSE_TO] is not None:
            self.twitter.add_comment(tweet)

            # TODO identify new post made by user...

    def add_toStream(self, accountID):
        self.STREAM_FILTER.append(accountID)
        self.twitterStream.disconnect()
        self.twitterStream.filter(follow=self.STREAM_FILTER, is_async=True)

    def remove_ofStream(self, accountID):
        if accountID in self.STREAM_FILTER:
            self.STREAM_FILTER.remove(accountID)
            self.twitterStream.disconnect()
            self.twitterStream.filter(follow=self.STREAM_FILTER, is_async=True)
