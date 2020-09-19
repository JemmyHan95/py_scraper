import urllib3

from lxml import etree

def test():
    url = 'http://rule34.paheal.net/post/list/KisXsfm/1'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    http = urllib3.PoolManager()
    resp = http.request('GET', url, headers=headers, timeout=5)
    print(resp.code)
    doc = etree.HTML(resp.data)
    for elem in doc.xpath('//div[@class="shm-thumb thumb"]'):
        print(elem.get('data-ext'))
        print(elem.xpath('./a[last()]/@href')[0])

if __name__ == '__main__':
    test()