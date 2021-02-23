# coding=utf-8
import json
import os

import rq
from flask import Flask, Response, request
from flask_cors import CORS

from worker import conn

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

FLASK_APP = Flask(__name__)
CORS(FLASK_APP)  # allowing request from different urls... (localhost in another port)

TASK_QUEUE = rq.Queue('tasksQueue', connection=conn, default_timeout=3600)

