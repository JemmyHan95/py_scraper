from download_url import download_video_url
from download_file import download_video

def main():
    category = 'Elena_Fisher'
    start = 1
    end = 5
    #download_video_url(category, start, end)
    download_video(category, start, end)


if __name__ == '__main__':
    main()
