import requests, string
from stop_words import get_stop_words
from bs4 import BeautifulSoup as BS

stop_words = get_stop_words('english')

def main(url):
        return keywords(url)

def keywords(html):
        ua = 'Mozilla/5.0 (Windows NT 6.1;WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        r = requests.get(url, headers={'User-Agent': ua})
        if r.status_code != 200:
                raise IOError
        parser = BS(r.text, 'lxml')
        kws = []
        if parser.title.string:
                kws.extend(parser.title.string.split(' '))
        for meta in [ x['content'].encode('utf-8') for x in
                        parser.find_all(attrs={'name':'description'})]:
                kws.extend(meta.split(' '))
        text = ''.join([c for c in ' '.join(kws) if c in
                string.ascii_letters+'\'- ']).lower()
        return list(set(w for w in text.split(' ') if w and w not in stop_words and w not in string.punctuation))
 
if __name__ == '__main__':
        import sys, json
        urls = sys.argv[1:]
        fix = lambda url: url if 'http://' in url else 'http://'+url
        kws = {}
        for url in map(fix, urls):
                kws[url] = keywords(url)
        print(json.dumps(kws, sort_keys=True, indent=4, separators=(',',': ')))
