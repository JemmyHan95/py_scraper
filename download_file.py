import os
import requests

from urllib.request import urlopen
from tqdm import tqdm

def download_from_url(url, dst):
    file_size = int(urlopen(url).info().get('Content-Length', -1))

    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size

    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=url.split('/')[-1])
    req = requests.get(url, headers=header, stream=True)

    with open(dst, 'ab') as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()

    return file_size

def download_video(category, start_page, end_page):
    video_save_path = 'F:\\CG Pornography\\' + category + '\\Videos'
    video_url_path = 'F:\\Downloads\\ScrapedUrls\\'
    downloaded_file_code = []

    if not os.path.exists(video_save_path):
        os.mkdir(video_save_path)

    for elem in os.walk(video_save_path):
        for  filename in elem[2]:
            downloaded_file_code.append(filename[0:7])

    for i in range(start_page, end_page):
        full_url_path = video_url_path + category + '_' + str(i) + '.txt'
        if os.path.exists(full_url_path):
            print('Start downloading ' + category + ' page ' + str(i))
            with open(full_url_path, 'r') as f:
                for line in f.readlines():
                    line = line.strip()
                    video_file_name = line[line.rfind('/') + 1 : len(line)].replace('%20', '_')
                    video_code = video_file_name[0:7]
                    if video_code in downloaded_file_code:
                        print(video_file_name + ' already downloaded')
                        continue
                    else:
                        video_full_path = video_save_path + video_file_name
                        download_from_url(line, video_full_path)
        else:
            print(full_url_path + ' does not exists!')
