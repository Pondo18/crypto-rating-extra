import pandas as pd
import praw
from threading import Thread
from sqlalchemy import create_engine
import psycopg2
from data_cleaning import Preprocessing
import datetime
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('stopwords')
nltk.download('vader_lexicon')


def authentication():
    r = praw.Reddit(user_agent='NighthawkF119',
                    client_id='rLCb2zuuI353PvfyFj-MEg',
                    client_secret='9J4k6ideHi40H1I87nwfm-W2beX88A',
                    check_for_async=False)
    return r


def query_reddit(subreddit, key, update):
    # build connection to redditapi
    r = authentication()

    # define subreddit to query
    sub = r.subreddit(subreddit)

    # get original submissions from reddit
    # (depending on if the query is intended for updating the dataset or initial quering all or the 100 most recent)
    # exception in case subreddit does not excist
    try:
        if update:
            submissions = [*sub.new(limit=100)]
        else:
            submissions = [*sub.new(limit=None)]

        # getting the required data from the submissions
        # title  = text of the submission
        title = [submission.title for submission in submissions]
        # unique id given by reddit api
        ids = [submission.id for submission in submissions]
        # score =  amount of upvotes
        score = [submission.score for submission in submissions]
        # subreddit for each submission
        subreddit_list = [key for submission in submissions]
        # date of creation for each submission
        date = [datetime.datetime.utcfromtimestamp(submission.created) for submission in submissions]

        # putting data in pandas dataframe for easier handling
        main_df = pd.DataFrame({"id": ids, "date": date, "text": title, "score": score, "subreddit_id": subreddit_list})

        # getting comments to each submissions, as well as the comments comments
        # any deeper comments (the commments comments comments) are disregarded

        # list to monitor gross amount of disregarded comments (for testing purposes)
        fail_list = []

        for post in submissions:
            comments = post.comments.list()
            for i in range(0, len(comments)):
                try:
                    if type(comments[i]) == praw.models.reddit.comment.Comment:
                        text = comments[i].body
                        ID = comments[i].id
                        score = comments[i].score
                        date = datetime.datetime.utcfromtimestamp(comments[i].created)
                        main_df = main_df.append(
                            {"id": ID, "date": date, "text": text, "score": score, "subreddit_id": key},
                            ignore_index=True)
                    elif type(comments[i]) == praw.models.reddit.more.MoreComments:
                        unter_kommentare = comments[i].comments()
                        for element in unter_kommentare:
                            text = element.body
                            ID = element.id
                            score = element.score
                            date = datetime.datetime.utcfromtimestamp(comments[i].created)
                            main_df = main_df.append(
                                {"id": ID, "date": date, "text": text, "score": score, "subreddit_id": key},
                                ignore_index=True)
                except AttributeError:
                    fail_list.append("fail")
        print(len(fail_list))
        insert_into_db(main_df)
    except Exception as error:
        print(error)


def insert_into_db(df):
    try:
        conn = create_engine('postgresql+psycopg2://root:pass@10.11.12.116/postgres')
        df.to_sql(name="reddit_posts", con=conn, if_exists="append", index=False, chunksize=1000, method="multi")
    except Exception as error:
        print(error)
    clean_df = cleaned_df(df)
    sentiment_analysis(clean_df)


def cleaned_df(df: pd.DataFrame()) -> pd.DataFrame():
    lst_stopwords = nltk.corpus.stopwords.words("english")
    df2 = df.drop(labels=["score", "subreddit_id", "date"], axis=1)
    df2["cleaned_text"] = df2["text"].apply(Preprocessing.clean_column).apply(Preprocessing.string_convert).apply(
        Preprocessing.remove_emojis).apply(
        lambda x: Preprocessing.utils_preprocess_text(x, flg_stemm=True, flg_lemm=False, lst_stopwords=lst_stopwords))
    return df2


def sentiment_analysis(df: pd.DataFrame()):
    sia = SentimentIntensityAnalyzer()
    sentiment_list = []
    for i in range(len(df)):
        sentiment_list.append(sia.polarity_scores(df["cleaned_text"][i])['compound'])
    df["sentiment_score"] = sentiment_list
    sentiment_to_db(df)


def sentiment_to_db(df: pd.DataFrame()):
    try:
        df.drop(labels=["cleaned_text", "text"], inplace=True, axis=1)
        conn = create_engine('postgresql+psycopg2://root:pass@10.11.12.116/postgres')
        df.to_sql(name="reddit_sentimentscores", con=conn, if_exists="append", index=False, chunksize=1000, method="multi")
    except Exception as error:
        print(error)


def query_subreddits(subreddits, keys, update):
    for i in range(len(subreddits)):
        t = Thread(target=query_reddit, args=(subreddits[i], keys[i], update))
        t.start()


def setup_subreddits(update):
    subreddits = []
    keys = []

    conn = psycopg2.connect(
        host="10.11.12.116",
        database="postgres",
        user="root",
        password="pass")

    cur = conn.cursor()
    sql = "SELECT id, slug FROM crypto_currencies WHERE active_top is True"
    cur.execute(sql)
    currencies = cur.fetchall()

    cur.close()
    conn.close()

    for i in range(len(currencies)):
        keys.append(currencies[i][0])
        subreddits.append(currencies[i][1])

    query_subreddits(subreddits=subreddits, update=update, keys=keys)


setup_subreddits(True)
