import urllib3
import time
import os

from lxml import etree

def acquire_page_content(url):
    # Visits url using urllib and returns its body
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    http = urllib3.PoolManager()
    resp = http.request('GET', url, headers=headers, timeout = urllib3.Timeout(connect = 15.0, read = 15.0))
    if resp.status != 200:
        return None
    return resp.data

def parse_page_content(content):
    # Parses web page content and returns the list of video urls
    video_list = []
    doc = etree.HTML(content)

    for elem in doc.xpath('//div[@class="shm-thumb thumb"]'):
        ext = elem.get('data-ext')
        if 'mp4' == ext or 'webm' == ext:
            video_list.append(elem.xpath('./a[last()]/@href')[0])

    return video_list

def save_urls_to_file(url_list, dst):
    # Saves the video urls to file
    with open(dst, 'w') as f:
        for url in url_list:
            f.write(url)
            f.write('\n')

def download_video_url(category, start_page, end_page):
    # Integrates all the sub processes above
    base_dir = 'F:\\Downloads\\ScrapedUrls\\'
    base_url = 'http://rule34.paheal.net/post/list/'

    for i in range(start_page, end_page):
        full_url = base_url + category + '/' + str(i)
        full_path = base_dir + category + '_' + str(i) + '.txt'
        print('Acquiring content from:' + full_url)
        page_content = acquire_page_content(full_url)
        # Page content acquisition failed
        if page_content is None:
            print('Acquisition encountered an error')
        save_urls_to_file(parse_page_content(page_content), full_path)
        time.sleep(8)
