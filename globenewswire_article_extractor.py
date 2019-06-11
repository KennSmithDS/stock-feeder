import pandas as pd
import codecs
import re
import os
import sys
from bs4 import BeautifulSoup
import logging
import datetime as dt

def setup_logger(log_dir=None,
                 log_file=None,
                 log_format=logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
                 log_level=logging.INFO):
    # Get logger
    logger = logging.getLogger('')
    # Clear logger
    logger.handlers = []
    # Set level
    logger.setLevel(log_level)
    # Setup screen logging (standard out)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(log_format)
    logger.addHandler(sh)
    # Setup file logging
    if log_dir and log_file:
        fh = logging.FileHandler(os.path.join(log_dir, log_file))
        fh.setFormatter(log_format)
        logger.addHandler(fh)

    return logger

def openArticleArchive():
    os.chdir('C://Users//kenns//PycharmProjects//StockFeeder//globenewswire_articles')
    files = os.listdir()
    articles = [file for file in files if 'r_' not in file]
    return articles

def getArticleSoup(file):
    try:
        # open file from directory and make soup!
        with codecs.open(file, 'r') as f:
            stuff = f.read()
        soup = BeautifulSoup(stuff, 'html.parser')

        # find article language
        for meta in soup.findAll('meta'):
            if meta.get('itemprop', None) == 'inLanguage':
                article_language = meta.get('content')
            else:
                pass

        # filter for english articles only
        if article_language == 'en':

            # find article title
            headers = soup.findAll('h1', class_='article-headline')
            article_title = headers[0].text
            print(article_title)

            # find article timestamp
            times = soup.findAll('time')
            article_timestamp = times[0].text
            print(article_timestamp)

            # find article url link
            for meta in soup.findAll('meta'):
                if meta.get('name', None) == 'original-source':
                    article_url = meta.get('content')
                else:
                    pass

            # find article body
            body = soup.findAll('span', class_='article-body')
            body_text = body[0].text
            print(len(body_text))

        else:

            body_text = None
            article_timestamp = None
            article_title = None
            article_url = None

        return body_text, article_timestamp, article_title, article_url

    except Exception as e:
        log.error('Error on line {}, error type {}, error code {}'.format((sys.exc_info()[-1].tb_lineno), type(e).__name__, e))
        pass

if __name__ == "__main__":

    # Setup directories
    data_dir = 'data'
    logging_dir = 'logs'
    time_date = dt.datetime.now()
    string_date = time_date.strftime("%Y%m%d_%H%M%S")

    # Setup Logging
    logging_level = logging.INFO
    if not os.path.exists(logging_dir):
        os.makedirs(logging_dir)
    logging_file = 'globe_news_wire_article_fetcher_{}.log'.format(string_date)
    log = setup_logger(logging_dir, logging_file, log_level=logging_level)

    try:

        article_filenames = openArticleArchive()
        for file in article_filenames:
            article_body, article_timestamp, article_title, article_url = getArticleSoup(file)
            if article_body:
                print('I think Ill keep this article!!!')
            else:
                print('Dropped non-english language article.')

    except Exception as e:
        log.error('Error on line {}, error type {}, error code {}'.format((sys.exc_info()[-1].tb_lineno), type(e).__name__, e))
        pass