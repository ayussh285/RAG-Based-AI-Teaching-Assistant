import os
import subprocess

VIDEO_FOLDER = "videos"
AUDIO_FOLDER = "audios"

os.makedirs(VIDEO_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)
 
def clean_filename(filename):
    invalid_characters = '<>:"/\\|?*'

    for char in invalid_characters:
        filename = filename.replace(char, "")

    return filename.strip()
 
VIDEO_EXTENSIONS = (
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".wmv",
    ".flv",
    ".webm"
)
 
for file in os.listdir(VIDEO_FOLDER):
    video_path = os.path.join(VIDEO_FOLDER, file)
 
    if not os.path.isfile(video_path):
        continue
 
    if not file.lower().endswith(VIDEO_EXTENSIONS):
        continue
 
    file_name = os.path.splitext(file)[0]
    file_name = clean_filename(file_name)
 
    audio_path = os.path.join(
        AUDIO_FOLDER,
        f"{file_name}.mp3"
    )
    print(f"Converting: {file}")
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                video_path,
                audio_path
            ],
            check=True
        )

        print(f"Saved: {audio_path}\n")

    except subprocess.CalledProcessError:
        print(f"Failed to convert: {file}\n")