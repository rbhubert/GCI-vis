# coding=utf-8
import json
import os

import rq
from flask import Flask, Response, request
from flask_cors import CORS

import task_handler
from enums import RequestType
from recovery import news
from recovery import recovery_requests_handler
from worker import conn

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

FLASK_APP = Flask(__name__)
CORS(FLASK_APP)  # allowing request from different urls... (localhost in another port)

TASK_QUEUE = rq.Queue('tasksQueue', connection=conn, default_timeout=3600)


@FLASK_APP.route("/tasks/<task_id>", methods=["GET"])
def get_task_status(task_id):
    task = TASK_QUEUE.fetch_job(task_id)

    if task:
        response_object = {
            "status": "success",
            "data": {
                "task_id": task.get_id(),
                "task_status": task.get_status(),
                "task_result": task.result,
            },
        }
    else:
        response_object = {"status": "error"}

    response = json.dumps(response_object)
    return Response(response, status=200, mimetype='application/json')


# Add a new user to the list of users/accounts currently followed.
@FLASK_APP.route('/accounts/<social_media>/<username>', methods=['DELETE', 'POST'])
def accounts(social_media=None, username=None):
    # If is it a POST request -> follow account
    # If is it a DELETE request -> unfollow account

    social_media = social_media.lower()
    if request.method == 'POST':
        job = TASK_QUEUE.enqueue(task_handler.follow_account, social_media, username)
        job_id_js = json.dumps(job.get_id())
        return Response(job_id_js, status=200, mimetype='application/json')

    else:
        response = task_handler.unfollow_account(social_media, username)
        respjs = json.dumps(response)
        return Response(respjs, status=200, mimetype='application/json')


# Returns all the accounts that are being currently followed.
@FLASK_APP.route('/accounts')
def get_accounts():
    accounts = task_handler.get_accounts()
    js = json.dumps(accounts)
    return Response(js, status=200, mimetype='application/json')


# Get the news item
@FLASK_APP.route('/newspaper', methods=['GET'])
def get_news():
    news_url = request.args.get('newUrl')
    news_item = news.get_news_item(news_url)
    js = json.dumps(news_item, default=str)
    return Response(js, status=200, mimetype='application/json')


# Gets the wordcloud for a socialmedia account.
@FLASK_APP.route('/wordcloud/socialmedia/<social_media>/<username>/', defaults={"time_window": None})
@FLASK_APP.route('/wordcloud/socialmedia/<social_media>/<username>/<time_window>')
def wordcloud_social_media(social_media, username, time_window=None):
    user_id = task_handler.__check_user(social_media, username)
    word_cloud = recovery_requests_handler.get_wordcloud(RequestType.SOCIALMEDIA, social_media, user_id, time_window)
    json_response = json.dumps(word_cloud)

    resp = Response(json_response, status=200, mimetype='application/json')

    return resp


# Gets the wordcloud for a news url.
@FLASK_APP.route('/wordcloud/newspaper')
def wordcloud_newspaper():
    news_url = request.args.get('newUrl')
    word_cloud = recovery_requests_handler.get_wordcloud(RequestType.NEWSPAPER, url=news_url)
    json_response = json.dumps(word_cloud)

    resp = Response(json_response, status=200, mimetype='application/json')

    return resp


# Gets the emotions for a socialmedia account.
@FLASK_APP.route('/emotions/radar/socialmedia/<social_media>/<username>/', defaults={"time_window": None})
@FLASK_APP.route('/emotions/radar/socialmedia/<social_media>/<username>/<time_window>')
def emotions_radar_social_media(social_media, username, time_window=None):
    user_id = task_handler.__check_user(social_media, username)
    emotions = recovery_requests_handler.get_emotions_combinations(RequestType.SOCIALMEDIA, social_media, user_id,
                                                                   time_window)
    js = json.dumps(emotions)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


# Gets the emotions for a news url.
@FLASK_APP.route('/emotions/radar/newspaper')
def emotions_radar_newspaper():
    news_url = request.args.get('newUrl')
    emotions = recovery_requests_handler.get_emotions_combinations(RequestType.NEWSPAPER, url=news_url)
    js = json.dumps(emotions)

    resp = Response(js, status=200, mimetype='application/json')
    return resp


# Gets the relation between multimedia resources and interactions receive from citizens for a socialmedia account.
@FLASK_APP.route('/multimediaInteraction/socialmedia/<social_media>/<username>/', defaults={"time_window": None})
@FLASK_APP.route('/multimediaInteraction/socialmedia/<social_media>/<username>/<time_window>')
def multimedia_interaction_relation_social_media(social_media, username, time_window=None):
    user_id = task_handler.__check_user(social_media, username)
    mult_inter = recovery_requests_handler.get_multimedia_interaction(social_media, user_id, time_window)

    js = json.dumps(mult_inter)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


# Gets the use of multimedia resources of a socialmedia account.
@FLASK_APP.route('/multimedia/socialmedia/<social_media>/<username>/', defaults={"time_window": None})
@FLASK_APP.route('/multimedia/socialmedia/<social_media>/<username>/<time_window>')
def multimedia_social_media(social_media, username, time_window=None):
    user_id = task_handler.__check_user(social_media, username)
    multimedia = recovery_requests_handler.get_multimedia(social_media, user_id, time_window)

    js = json.dumps(multimedia)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


# Gets the interactions made by citizens to a socialmedia account posts.
@FLASK_APP.route('/interaction/socialmedia/<social_media>/<username>/', defaults={"time_window": None})
@FLASK_APP.route('/interaction/socialmedia/<social_media>/<username>/<time_window>')
def interaction_social_media(social_media, username, time_window=None):
    user_id = task_handler.__check_user(social_media, username)
    interaction = recovery_requests_handler.get_interaction(social_media, user_id, time_window)

    js = json.dumps(interaction)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


# Gets the emotions for a socialmedia account over time
@FLASK_APP.route('/emotions/socialmedia/<social_media>/<username>/', defaults={"time_window": None})
@FLASK_APP.route('/emotions/socialmedia/<social_media>/<username>/<time_window>')
def emotions_social_media(social_media, username, time_window):
    user_id = task_handler.__check_user(social_media, username)
    emotions = recovery_requests_handler.get_emotions(request_type=RequestType.SOCIALMEDIA, social_media=social_media,
                                                      user_id=user_id,
                                                      time_window=time_window)

    js = json.dumps(emotions)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


# Gets the emotions for a news url over time
@FLASK_APP.route('/emotions/newspaper')
def emotions_newspaper():
    news_url = request.args.get('newUrl')
    emotions = recovery_requests_handler.get_emotions(RequestType.NEWSPAPER, url=news_url)
    js = json.dumps(emotions)

    resp = Response(js, status=200, mimetype='application/json')

    return resp


# Gets the activity (posts publications), the interactions and the multimedia resource use
# of a socialmedia account over time.
@FLASK_APP.route('/activity/socialmedia/<social_media>/<username>/', defaults={"time_window": None})
@FLASK_APP.route('/activity/socialmedia/<social_media>/<username>/<time_window>')
def activity_social_media(social_media, username, time_window=None):
    user_id = task_handler.__check_user(social_media, username)
    activity = recovery_requests_handler.get_activity(social_media, user_id, time_window)

    js = json.dumps(activity)
    resp = Response(js, status=200, mimetype='application/json')
    return resp
