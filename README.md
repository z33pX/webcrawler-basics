# webcrawler-basics
This script extracts text (+ sentiment analysis), links and tables from a webpage and stores it into a json file.
The script is intended as a start for beginners who want to deal with webcrawling.


Start
-

Follow this steps to run the script:
1) Clone repository: ``git clone https://github.com/z33pX/webcrawler-basics.git``
2) Change dir: ``cd webcrawler-basics``
3) Create vm: ``python3 -m venv venv``
4) Activate vm: ``source venv/bin/activate``
5) Install requirements: ``pip install -r requirements.txt``
6) Execute script: ``python main.py``

Code
-

This script basically consists of 3 functions. The functions are called in the main 
function: `extract_tables()`, `extract_urls()` and `extract_text()`.
The url of the website is defined at the beginning of the main function.


```
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
```

Have fun coding and experimenting! :wink: