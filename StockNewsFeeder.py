#Currently this only pulls in designated rss feeds from a single source - PR newswire
#The url links for the rss files are hard coded, but ideally would be dynamically stored in a csv file
#Since each feed file is limited to 20 articles, need to set loop on random time interval
#Eventually I intend to have a header python script that will extract relevant news from all sources
#The following are steps that are intended to be repeated over multiple news source feeds

#0 create blank csv file with column names
#1 open rss feed files from PR newswire website
#2 fetch rss headers (title, publish date, url link, description)
#3 remove duplicate headers/articles from news list that appear in multiple feeds
## should a layer of filtering occur on keywords in title/description???
#4 get article body content for each url link in the filtered list
#5 search for all company stock tickers (nasdaq, nyse, otc, etc.)
#6 ignore articles without tickers present in the articles (represent privately traded, or generic news)
#7 find sector, current price, avg. volume, and moving averages (50/200) day with yahoo finance API / MYQL
#8 filter to only articles within penny stock range and high average volume
#9 perform sentiment analysis from keywords to determine if bull or bear news
#10 write/append output of headers, technical analysis, and market sentiment to csv file

import re
import time
from datetime import datetime
import pandas as pd
from yahoo_finance import Share
import requests
import csv

#class NewsArticle:
	#def __init__(self, title, pubdate, link, content):
		#self.title = title
		#self.pubdate = pubdate
		#self.link = link
		#self.content = content
		#self.sentiment = buy | sell
		#self.ticker = ticker
		#self.stock_of_interest = true | false
		
	#def get_sentiment():
	#def find_tickers():

def main():
	urls = ['http://www.prnewswire.com/rss/automotive-transportation/all-automotive-transportation-news.rss',\
		'http://www.prnewswire.com/rss/business-technology/all-business-technology-news.rss',\
		'http://www.prnewswire.com/rss/consumer-products-retail/all-consumer-products-retail-news.rss',\
		'http://www.prnewswire.com/rss/consumer-technology/all-consumer-technology-news.rss',\
		'http://www.prnewswire.com/rss/energy/all-energy-news.rss',\
		'http://www.prnewswire.com/rss/environment/all-environment-news.rss',\
		'http://www.prnewswire.com/rss/financial-services/all-financial-services-news.rss',\
		'http://www.prnewswire.com/rss/general-business/all-general-business-news.rss',\
		'http://www.prnewswire.com/rss/health/all-health-news.rss',\
		'http://www.prnewswire.com/rss/heavy-industry-manufacturing/all-heavy-industry-manufacturing-news.rss',\
		'http://www.prnewswire.com/rss/policy-public-interest/all-policy-public-interest-news.rss',\
		'http://www.prnewswire.com/rss/telecommunications/all-telecommunications-news.rss']
	
	feed_headers = []
	create_log_csv()

	try:
		for url in urls:
			live_headers = (get_news_headers(url))
			for header in live_headers:
				feed_headers.append(header)
		
		news_list = remove_dup_articles(feed_headers)
		
		# print(news_list[0])
		
		# i=0
		# while i < 1:
			# get_article(news_list[i][2])
			# i+=1

		#for item in news_list:
			#get_article(link)
		
		write_log_to_csv(news_list)
		
	except Exception as e:
		print(e)
		pass

def get_news_headers(url):
	
	response_header = {'user-agent': 'Chrome/53.0.2785.143'}	
	pr_news_response = requests.get(url, headers=response_header)
	pr_news_text = pr_news_response.text
	
	news_headers = []
	titles = re.findall('<title>(.*?)</title>',pr_news_text)
	for title in titles:
		title = title.encode("utf8")
	links = re.findall('<link>(.*?)</link>',pr_news_text)
	pubdates = re.findall('<pubDate>(.*?)</pubDate>',pr_news_text)
	
	#descriptions are commented out because many are blank and mess indexing
	#descriptions = re.findall(r'<description>(.*?)</description>',pr_news_text)	
	
	for i in range(len(links)):
		if '.rss' in links[i]:
			pass
		else:
			news_headers.append([titles[i].encode('utf8'),pubdates[i],links[i]])
	
	return news_headers
	
def remove_dup_articles(headers):
	df = pd.DataFrame(headers)
	df = df.drop_duplicates()
	new_list = df.values.tolist()
	return new_list

def get_article(link):
	print('fetching article')
	response_header = {'user-agent': 'Chrome/53.0.2785.143'}
	linksource = requests.get(link, headers=response_header)
	linktext = linksource.text
	newscontent = re.findall('<!-- Content Body START  -->((.|\n)*)<!-- Content Body  END  -->',linktext)
	cleancontent = re.findall('<p  itemprop="articleBody">(.*?)</p>',str(newscontent))
	cleantext = clean_html(cleancontent)
	
def clean_html(source):
	cleaner = re.compile('<.*?>')
	cleantext = re.sub(cleaner, '', source)
	return cleantext

def find_tickers(body):
	tickers = []
	nasdaq_tickers = re.findall('\(NASDAQ:(.*?)\)',body)
	nyse_tickers = re.findall('\(NYSE:(.*?)\)',body)
	otc_tickers = re.findall('\(OTC:(.*?)\)',body)
	for stock in nasdaq_tickers + nyse_tickers + otc_tickers:
		tickers.append(stock.strip())
	return tickers
	
def stock_analysis(ticker):
	share = Share(ticker)
	price = share.get_price()
	avg_vol = share.get_avg_daily_volume()
	ma_50 = share.get_50day_moving_avg()
	ma_200 = share.get_200day_moving_avg()
	return price, avg_vol, ma_50, ma_200
	
	#can also get historical prices from range
	#share.get_historical(start_date, end_date)
	#need to find way to get the industry too
	#pandas data frames or MYQL might be better method
	
def create_log_csv():
	filename = 'news_log_%s.csv'%datetime.now().strftime('%Y-%m-%d_%H%M')
	with open(filename, 'w', newline='') as out:
		csvwriter = csv.writer(out, delimiter=',')
		csvwriter.writerow(['Title','Publish Date','Link'])
		out.close()
		
def write_log_to_csv(news):
	filename = 'news_log_%s.csv'%datetime.now().strftime('%Y-%m-%d_%H%M')
	with open(filename, 'a', newline='') as out:
		csvwriter = csv.writer(out, delimiter=',')
		for item in news:
			csvwriter.writerow(item)
		out.close()

main()