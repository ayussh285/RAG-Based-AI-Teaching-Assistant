import os
import json
import re
import whisper
import yt_dlp
 
AUDIO_FOLDER = "audios"
JSON_FOLDER = "jsons"

os.makedirs(AUDIO_FOLDER, exist_ok=True)
os.makedirs(JSON_FOLDER, exist_ok=True)
 
def clean_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    return filename.strip()

def get_playlist_info(playlist_url):
    print("\nGetting playlist information...\n")
    ydl_opts = {
        "quiet": True,
        "extract_flat": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(
            playlist_url,
            download=False
        )
    return playlist_info

def download_audio(video_url, number):
    print(f"\nDownloading audio for Video {number}...")

    ydl_opts = {
        "outtmpl": os.path.join(
            AUDIO_FOLDER,
            f"{number}. %(title)s.%(ext)s"
        ),

        "format": "bestaudio/best",

        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }
        ],

        "quiet": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            video_url,
            download=True
        )

        downloaded_path = ydl.prepare_filename(info)
 
    audio_path = os.path.splitext(downloaded_path)[0] + ".mp3"

    return info, audio_path

def create_json_from_audio(audio_path,info,number,model):
    print(
        f"Transcribing Video {number}: "
        f"{info['title']}"
    )

    result = model.transcribe(
        audio=audio_path,
        language="hi",
        task="translate",
        word_timestamps=False
    )
 
    chunks = []
    for segment in result["segments"]:
        chunk = {
            "number": number,
            "title": info["title"],
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"],
            
            "video_url": info.get(
                "webpage_url",
                ""
            ),

            "video_id": info.get(
                "id",
                ""
            )
        }
        chunks.append(chunk)
 
    json_data = {
        "video_number": number,
        "title": info["title"],
        "video_url": info.get(
            "webpage_url",
            ""
        ),

        "video_id": info.get(
            "id",
            ""
        ),

        "duration": info.get(
            "duration",
            None
        ),

        "chunks": chunks,
        "text": result["text"]
    }

    safe_title = clean_filename( info["title"])
    json_filename = ( f"{number}. {safe_title}.json")

    json_path = os.path.join(
        JSON_FOLDER,
        json_filename
    )

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4 )

    print(
        f"JSON created successfully: "
        f"{json_filename}"
    )
 
def main():
    print("=" * 60)
    print("VidMentor - YouTube Playlist Processor")
    print("=" * 60)

    playlist_url = input(
        "\nEnter YouTube Playlist URL:\n"
    ).strip()

    if not playlist_url:
        print("\nPlaylist URL cannot be empty.")
        return
 
    try:
        playlist_info = get_playlist_info(
            playlist_url
        )

    except Exception as e:
        print(
            "\nUnable to access playlist."
        )
        print("Error:", e)
        return


    playlist_title = playlist_info.get("title", "Unknown Playlist")

    entries = playlist_info.get(
        "entries",
        []
    )

    print(f"\nPlaylist: {playlist_title}")
    print(f"Videos found: {len(entries)}")

    if not entries:
        print( "\nNo videos found in this playlist.")
        return

    print( "\nLoading Whisper large-v2 model..." )

    model = whisper.load_model("large-v2")

    print("Whisper model loaded successfully.")

    for index, entry in enumerate( entries, start=1):
        try:
            video_url = entry.get(
                "url"
            )

            if not video_url:
                video_url = (
                    "https://www.youtube.com/watch?v="
                    + entry["id"]
                )

            print("\n" + "=" * 60)
            print( f"Processing Video {index}")
            print(f"Title: {entry.get('title', 'Unknown')}")

            print("=" * 60)
            info, audio_path = download_audio(
                video_url,
                index
            )

            if not os.path.exists(audio_path):
                print(
                    f"Audio file not found: "
                    f"{audio_path}"
                )
                continue
 
            create_json_from_audio(
                audio_path=audio_path,
                info=info,
                number=index,
                model=model
            )
 
            print(f"\nVideo {index} completed successfully.")

        except Exception as e: 
            print(
                f"\nError processing Video "
                f"{index}:"
            ) 
            print(e) 
            print(
                "\nSkipping this video and "
                "continuing with the next one."
            )

    print("\n" + "=" * 60) 
    print("Playlist processing completed!")
    print("Audio files saved in: audios/")
    print("JSON files saved in: jsons/")
    print("=" * 60)
 
if __name__ == "__main__":
    main()