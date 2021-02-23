# coding=utf-8
import json
import os

import rq
from flask import Flask, Response, request
from flask_cors import CORS

import tasks_requestHandler
from accountManager import accountsManager
from apis.twitter import TwitterStreaming
from enums import RequestType
from newsManager import newsManager
from recovery import requestsHandler
from worker import conn

FLASK_APP = Flask(__name__)
CORS(FLASK_APP)  # allowing request from different urls... (localhost in another port)

# just to avoid a windows error... o.ó
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

tasksQueue = rq.Queue('tasksQueue', connection=conn, default_timeout=3600)
twitterStreaming = TwitterStreaming()


##
# TODO the main application can already create the twitter instance

##
# TODO error message

# Route to the index page
@FLASK_APP.route('/')
def index():
    return 'Index page'


@FLASK_APP.route("/tasks/<taskID>", methods=["GET"])
def get_TaskStatus(taskID):
    task = tasksQueue.fetch_job(taskID)

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


# todo before getting all new tweets, just let the user know that we are searching for tweets, but he can already
#  try to use some visualization. its boring other way... and kind of annoying.
# Add a new user to the list of users/accounts currently followed.
@FLASK_APP.route('/accounts/<socialMedia>/<username>', methods=['DELETE', 'POST'])
def accounts(socialMedia=None, username=None):
    # If is it a POST request -> add new followed account
    # If is it a DELETE request -> remove followed account

    socialMedia = socialMedia.lower()
    if request.method == 'POST':
        job = tasksQueue.enqueue(tasks_requestHandler.add_account, socialMedia, username)
        jobId_js = json.dumps(job.get_id())
        return Response(jobId_js, status=200, mimetype='application/json')

    else:

        response = tasks_requestHandler.remove_account(socialMedia, username)
        respjs = json.dumps(response)
        return Response(respjs, status=200, mimetype='application/json')


@FLASK_APP.route('/stream/<socialMedia>/<username>', methods=['DELETE', 'POST'])
def streamAccount(socialMedia=None, username=None):
    response = tasks_requestHandler.stream_account(socialMedia, username)
    js = json.dumps(response)
    return Response(js, status=200, mimetype='application/json')


# Returns all the accounts that are being currently followed.
@FLASK_APP.route('/accounts')
def get_accounts():
    accounts = accountsManager.get_accounts()
    js = json.dumps(accounts)
    return Response(js, status=200, mimetype='application/json')


# Returns all the accounts that are being currently followed.
@FLASK_APP.route('/newspaper', methods=['GET'])
def get_new():
    newUrl = request.args.get('newUrl')
    newItem = newsManager.get_newItem(newUrl)
    js = json.dumps(newItem, default=str)
    return Response(js, status=200, mimetype='application/json')


# Gets the wordcloud for a socialmedia account.
@FLASK_APP.route('/wordcloud/socialmedia/<socialMedia>/<username>/', defaults={"timeWindow": None})
@FLASK_APP.route('/wordcloud/socialmedia/<socialMedia>/<username>/<timeWindow>')
def wordcloud_socialmedia(socialMedia, username, timeWindow=None):
    userID = tasks_requestHandler.get_userID(socialMedia, username)
    wordCloud = requestsHandler.wordCloud(RequestType.SOCIALMEDIA, socialMedia, userID, timeWindow)
    jsonResponse = json.dumps(wordCloud)

    resp = Response(jsonResponse, status=200, mimetype='application/json')

    return resp


# Gets the wordcloud for a news url.
@FLASK_APP.route('/wordcloud/newspaper')
def wordcloud_newspaper():
    newUrl = request.args.get('newUrl')
    wordCloud = requestsHandler.wordCloud(RequestType.NEWSPAPER, url=newUrl)
    jsonResponse = json.dumps(wordCloud)

    resp = Response(jsonResponse, status=200, mimetype='application/json')

    return resp


# Gets the emotions for a socialmedia account.
@FLASK_APP.route('/emotions/radar/socialmedia/<socialMedia>/<username>/', defaults={"timeWindow": None})
@FLASK_APP.route('/emotions/radar/socialmedia/<socialMedia>/<username>/<timeWindow>')
def emotionsRadar_socialmedia(socialMedia, username, timeWindow=None):
    userID = tasks_requestHandler.get_userID(socialMedia, username)
    emotions = requestsHandler.emotionsCombinations(RequestType.SOCIALMEDIA, socialMedia, userID, timeWindow)
    js = json.dumps(emotions)

    resp = Response(js, status=200, mimetype='application/json')

    return resp


# Gets the emotions for a news url.
@FLASK_APP.route('/emotions/radar/newspaper')
def emotionsRadar_newspaper():
    newUrl = request.args.get('newUrl')
    emotions = requestsHandler.emotionsCombinations(RequestType.NEWSPAPER, url=newUrl)
    js = json.dumps(emotions)

    resp = Response(js, status=200, mimetype='application/json')

    return resp


# Gets the relation between multimedia resources and interactions receive from citizens for a socialmedia account.
@FLASK_APP.route('/multimediaInteraction/socialmedia/<socialMedia>/<username>/', defaults={"timeWindow": None})
@FLASK_APP.route('/multimediaInteraction/socialmedia/<socialMedia>/<username>/<timeWindow>')
def multimediaInteraction_relation_socialmedia(socialMedia, username, timeWindow=None):
    userID = tasks_requestHandler.get_userID(socialMedia, username)
    multInteraction = requestsHandler.multimediaInteraction(socialMedia, userID, timeWindow)
    js = json.dumps(multInteraction)

    resp = Response(js, status=200, mimetype='application/json')

    return resp


# Gets the use of multimedia resources of a socialmedia account.
@FLASK_APP.route('/multimedia/socialmedia/<socialMedia>/<username>/', defaults={"timeWindow": None})
@FLASK_APP.route('/multimedia/socialmedia/<socialMedia>/<username>/<timeWindow>')
def multimedia_socialmedia(socialMedia, username, timeWindow=None):
    userID = tasks_requestHandler.get_userID(socialMedia, username)
    multimedia = requestsHandler.getMultimedia(socialMedia, userID, timeWindow)
    js = json.dumps(multimedia)

    resp = Response(js, status=200, mimetype='application/json')

    return resp


# Gets the interactions made by citizens to a socialmedia account posts.
@FLASK_APP.route('/interaction/socialmedia/<socialMedia>/<username>/', defaults={"timeWindow": None})
@FLASK_APP.route('/interaction/socialmedia/<socialMedia>/<username>/<timeWindow>')
def interaction_socialmedia(socialMedia, username, timeWindow=None):
    userID = tasks_requestHandler.get_userID(socialMedia, username)
    interaction = requestsHandler.getInteraction(socialMedia, userID, timeWindow)
    js = json.dumps(interaction)

    resp = Response(js, status=200, mimetype='application/json')

    return resp


# Gets the emotions for a socialmedia account over time
@FLASK_APP.route('/emotions/socialmedia/<socialMedia>/<username>/', defaults={"timeWindow": None})
@FLASK_APP.route('/emotions/socialmedia/<socialMedia>/<username>/<timeWindow>')
def emotions_socialmedia(socialMedia, username, timeWindow):
    userID = tasks_requestHandler.get_userID(socialMedia, username)
    emotions = requestsHandler.getEmotions(requestType=RequestType.SOCIALMEDIA, socialMedia=socialMedia, userID=userID,
                                           timeWindow=timeWindow)
    js = json.dumps(emotions)

    resp = Response(js, status=200, mimetype='application/json')

    return resp


# Gets the emotions for a news url over time
@FLASK_APP.route('/emotions/newspaper')
def emotions_newspaper():
    newUrl = request.args.get('newUrl')
    emotions = requestsHandler.getEmotions(RequestType.NEWSPAPER, url=newUrl)
    js = json.dumps(emotions)

    resp = Response(js, status=200, mimetype='application/json')

    return resp


# Gets the activity (posts publications), the interactions and the multimedia resource use
# of a socialmedia account over time.
@FLASK_APP.route('/activity/socialmedia/<socialMedia>/<username>/', defaults={"timeWindow": None})
@FLASK_APP.route('/activity/socialmedia/<socialMedia>/<username>/<timeWindow>')
def activity_socialmedia(socialMedia, username, timeWindow=None):
    userID = tasks_requestHandler.get_userID(socialMedia, username)
    activity = requestsHandler.getActivity(socialMedia, userID, timeWindow)
    js = json.dumps(activity)

    resp = Response(js, status=200, mimetype='application/json')

    return resp
