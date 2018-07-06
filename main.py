from bs4 import BeautifulSoup
import requests
import json
import coloredlogs
import logging as logging
from boilerpipe.extract import Extractor
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import unicodedata

FILE_NAME = "result.json"

# Logging ---------------------------------------------------------------------
coloredlogs.install(
    level='INFO',
    datefmt='%Y-%m-%d %I:%M:%S',
    fmt='%(asctime)s %(msecs)03d |%(name)-12s|%(levelname)-8s|%(process)-1d| %(message)s')

logger = logging.getLogger('WC')

# Functions -------------------------------------------------------------------


def extract_tables(html_string):
    soup = BeautifulSoup(requests.get(url).text, "lxml")
    table = soup.find("table")

    result = list()

    if table is not None:

    	# The first tr contains the field names.
    	headings = [th.get_text() for th in table.find("tr").find_all("th")]

    	datasets = []
    	for row in table.find_all("tr")[1:]:
    	    dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
    	    datasets.append(dataset)

    	for i, dataset in enumerate(datasets):
            item = dict()
            for field in dataset:
                item[field[0].replace('\n', '')] = field[1].replace('\n', '')
                # print("{0:<20}: {1}".format(field[0].replace('\n', ''), field[1].replace('\n', '')))
            print('   Save table item ' + str(i))
            result.append(item)

    else:
        logger.info('No Table Found')

    return result


def extract_urls(html_string):
    soup = BeautifulSoup(html_string, "lxml")

    list_of_urls = list()
    must_have_filter = ['http']

    result = dict()
    result['affiliate'] = dict()
    result['normal'] = dict()

    for link in soup.find_all('a'):
        url = link.get('href')

        if url:

            if url[-1] == '/':
                url = url[:-1]

            filtered = False
            for filter in must_have_filter:
                if filter not in url:
                    filtered = True
                    break

            name = link.get_text(' ', strip=True)

            if filtered is False:
                if url not in list_of_urls:
                    list_of_urls.append(url)
                    if url is not None:
                        print('   Added link: ' + str(url))
                        if 'affiliate' in url:
                            result['affiliate'][name] = url
                        else:
                            result['normal'][name] = url
    return result


def extract_text(url, min_length=10):
    extractor = Extractor(extractor='ArticleExtractor', url=url)
    sid = SentimentIntensityAnalyzer()
    strings = extractor.getText().split('\n')

    result = list()

    for string in strings:
        if string and len(string) >= min_length:
            ss = sid.polarity_scores(string)
            ss["Text"] = string
            print('   Added text item')
            result.append(ss)

    return result


if __name__ == "__main__":
    url = 'https://coinmarketcap.com/all/views/all/'
    extractions = dict()

    logger.info('Start crawling: ' + str(url))
    logger.info('Downloading website ...')
    html_string = requests.get(url).text

    logger.info('Start extracting tables ...')
    extractions['Tables'] = extract_tables(html_string)

    logger.info('Start extracting links ...')
    extractions['Links'] = extract_urls(html_string)

    logger.info('Start extracting text ...')
    extractions['Text'] = extract_text(url=url)

    logger.info('Dump to ' + FILE_NAME + ' ...')
    with open(FILE_NAME, 'w') as fp:
        json.dump(extractions, fp, indent=4, sort_keys=True)

    logger.info('Finished')
