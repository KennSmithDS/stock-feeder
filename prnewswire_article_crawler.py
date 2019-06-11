#THINGS TO DO BEFORE WRITING CSV:
#perform sentiment analysis
#determine if bull or bear
#search for ticker
#gather stock stats
#create filtered list to output

import re
import time
from datetime import datetime
import pandas as pd
import requests
import csv

class NewsArticle:
	def __init__(self, title, pubdate, link, content):
		self.title = title
		self.pubdate = pubdate
		self.link = link
		self.content = content
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
	headers = {'user-agent': 'Chrome/53.0.2785.143'}
	feed_headers = []
	create_log_csv()

	try:
		for url in urls:
			
			headers = get_news_headers(url)
			
			for i in range(len(links)):
				if '.rss' in links[i]:
					pass
				else:
					feed_headers.append([titles[i].encode('utf8'),pubdates[i],links[i]])
					#linksource = requests.get(links[i], headers=headers)
					#linktext = linksource.text
					#newscontent = re.findall('<!-- Content Body START  -->((.|\n)*)<!-- Content Body  END  -->',linktext)
					#cleancontent = re.findall('<p  itemprop="articleBody">(.*?)</p>',str(newscontent))
					#cleantext = clean_html(cleancontent)
					
					#t=0
					#while t<1:
					#	print(cleantext[5])
					#	t+=1
				
	except Exception as e:
		print(e)
	
	news_list = remove_dup_articles(feed_headers)	
	write_log_to_csv(news_list)

def get_news_headers(url):
			pr_news_response = requests.get(url, headers=headers)
			pr_news_text = pr_news_response.text
			
			titles = re.findall('<title>(.*?)</title>',pr_news_text)
			links = re.findall('<link>(.*?)</link>',pr_news_text)
			pubdates = re.findall('<pubDate>(.*?)</pubDate>',pr_news_text)
			#descriptions = re.findall(r'<description>(.*?)</description>',prn_text)	
	
def remove_dup_articles(headers):
	df = pd.DataFrame(headers)
	df = df.drop_duplicates()
	new_list = df.values.tolist()
	return new_list

#def get_article(link):	

def clean_html(source):
	cleaner = re.compile('<.*?>')
	cleantext = re.sub(cleaner, '', source)
	return cleantext
	
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