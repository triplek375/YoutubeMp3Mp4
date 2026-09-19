import yt_dlp
import os

def download_youtube_video(url, resolution):
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    ydl_opts = {
        'format': f'bestvideo[height<={resolution}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(downloads_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'quiet': False, 
    }

    try:
        print(f"Destination: {downloads_path}")
        print(f"Downloading: {url} at up to {resolution}p...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\nDownload completed successfully!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    quality = input("Enter maximum resolution (e.g., 1080, 720, 480): ")
        
    download_youtube_video(video_url, resolution=quality)