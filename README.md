# GCI-vis
GCI-vis is a web tool for the recovery and analysis of **G**overnment-**C**itizen **I**nteraction on Twitter using data mining and **vis**ualizations techniques.

The tool allows the user to retrieve (and keep listening for new) tweets from a Twitter account, in particular an official government Twitter account. The tool also allows you to visualize different aspects of the data: account activity over time, topics covered over a period of time, citizen interactions and emotions identified in the comments, use of multimedia resources by the account, etc.

You can see the research papers that analyze different Latin American countries using this tool, published in a relevant conference and journal in the area of e-Government:
- [Examining government-citizen interactions on Twitter using visual and sentiment analysis](https://dl.acm.org/doi/abs/10.1145/3209281.3209356), publication for the _International Conference on Digital Government Research: Governance in the Data Age_ (2018). 
- [Analyzing and Visualizing Government-Citizen Interactions on Twitter to Support Public Policy-making](https://dl.acm.org/doi/abs/10.1145/3360001), published in  _Digital Government: Research and Practice_ (2020).

# Technologies used
The backend for this project was written with Python 3.8.1. The following libraries were used:
- [flask](https://flask.palletsprojects.com/en/2.0.x/) for the set up of the web server;
- [tweepy](https://www.tweepy.org/) and [twarc](https://github.com/DocNow/twarc) for retrieving tweets and all the comments related;
- [pandas](https://pandas.pydata.org/) and [NLTK](https://www.nltk.org/) for the data analysis and manipulation;
- and [pymongo](https://pymongo.readthedocs.io/en/stable/) for the database (MongoDB) management.

The frontend was generated with [Angular CLI](https://github.com/angular/angular-cli) version 7.3.6. The following packages were used for the different visualizations:
- [angular-plotly](https://github.com/plotly/angular-plotly.js/blob/master/README.md) for the time series, bubble and radar charts;  
- [D3](https://d3js.org/) and [venn.js](https://github.com/benfred/venn.js/) for the Euler diagram visualization;
- and [angular4-word-cloud](https://github.com/alhazmy13/Angular4-word-cloud) for the word cloud visualization.

# How to use

## Preparation
You will need to have Angular, Python, RQ (Redis Queue), and Mongo installed, along with the requeriments for the backend. Once you have the code in your computer, open different console windows to run the following commands. 

### for the frontend
```
cd /path/to/the/GCI-vis/frontend
ng serve --open
```

### for the backend

Installing the requeriments:
```
cd /path/to/the/GCI-vis/backend
source ~/path/to/the/GCI-vis/backend/.venv/bin/activate
pip install -r requirements.txt
```

Server:
```
cd /path/to/the/GCI-vis/backend
source ~/path/to/the/GCI-vis/backend/.venv/bin/activate
export FLASK_APP=main_app.py
flask run
```

Redis Queue:
```
cd /path/to/the/GCI-vis/backend
redis-server
```

Worker
```
cd /path/to/the/GCI-vis/backend
source ~/path/to/the/GCI-vis/backend/.venv/bin/activate
python worker.py
```

Database
```
mongod --dbpath ~/data/db
```

## Usage
When you first open the tool, you can see a section to follow an account. Enter the account name and the tool will retrieve the last 100 tweets posted by that account and will listen for any new tweets. It will also periodically retrieve all citizen interactions, including new comments.

![image](https://user-images.githubusercontent.com/12433425/146689372-2b34efb0-a46a-41b6-a5c7-18878fb3c960.png)

Once you follow at least one account, you can start to see the visualizations. The tool offers seven different types: time series chart, Euler chart, Hasse chart, word cloud, bubble chart, radar chart, and Sankey chart. These graphs help to analyze different aspects of government communication and citizen responses, such as government activity and citizen interactions over time, the communication strategy and multimedia resource used, the emotions identified in the comments, among others.

![image](https://user-images.githubusercontent.com/12433425/146807121-17475135-8652-462d-8711-67b6bc75d064.png)

