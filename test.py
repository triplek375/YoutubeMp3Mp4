import yt_dlp
import os
import subprocess
import shutil
import tempfile
import sys

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
        print(f"Downloading video at up to {resolution}p...")
        
        # 1. Download the video and get file information
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            prepared_filename = ydl.prepare_filename(info_dict)
            base_filepath = os.path.splitext(prepared_filename)[0]
            
        mp4_file = f"{base_filepath}.mp4"
        instrumental_file = f"{base_filepath}.mp3"

        # Expand the temporary directory to hold the ffmpeg extraction as well
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_mp3_file = os.path.join(temp_dir, 'temp_audio.mp3')
            
            # 2. Extract full audio directly into the temporary folder
            print("\nExtracting audio to MP3...")
            subprocess.run([
                'ffmpeg', '-y', '-i', mp4_file, 
                '-q:a', '0', '-map', 'a', temp_mp3_file
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

            # 3. Remove vocals using Demucs
            print("Removing vocals (This may take a few minutes on your CPU)...")
            subprocess.run([
                sys.executable,
                '-m',
                'demucs',
                '--mp3',               
                '--two-stems=vocals',  
                '-o', temp_dir,        
                temp_mp3_file
            ], stdout=subprocess.DEVNULL, check=True)

            # Demucs creates a nested folder structure, so we search for the instrumental file
            for root, dirs, files in os.walk(temp_dir):
                if 'no_vocals.mp3' in files:
                    source_path = os.path.join(root, 'no_vocals.mp3')
                    # Move the final instrumental to your Downloads folder
                    shutil.move(source_path, instrumental_file)
                    break
        
        print("\nProcess completed successfully!")
        print(f"Video saved as: {os.path.basename(mp4_file)}")
        print(f"Instrumental saved as: {os.path.basename(instrumental_file)}")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    quality = input("Enter maximum resolution (e.g., 1080, 720, 480): ")
        
    download_youtube_video(video_url, resolution=quality)