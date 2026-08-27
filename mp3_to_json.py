import whisper
import json
import os

AUDIO_FOLDER = "audios"
JSON_FOLDER = "jsons"

os.makedirs(AUDIO_FOLDER, exist_ok=True)
os.makedirs(JSON_FOLDER, exist_ok=True)
model = whisper.load_model("large-v2")

AUDIO_EXTENSIONS = (
    ".mp3",
    ".wav",
    ".m4a",
    ".flac",
    ".aac",
    ".ogg"
)

for audio in os.listdir(AUDIO_FOLDER):
    audio_path = os.path.join(
        AUDIO_FOLDER,
        audio
    )
 
    if not os.path.isfile(audio_path):
        continue
 
    if not audio.lower().endswith(AUDIO_EXTENSIONS):
        continue
 
    file_name = os.path.splitext(audio)[0]
 
    if ". " in file_name:
        number, title = file_name.split(". ", 1)

    else:
        number = ""
        title = file_name

    print(f"\nTranscribing: {audio}")

    try:

        result = model.transcribe(
            audio=audio_path,
            language="hi",
            task="translate",
            word_timestamps=False
        )

        chunks = []

        for segment in result["segments"]:

            chunks.append(
                {
                    "number": number,
                    "title": title,
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"]
                }
            )

        chunks_with_metadata = {
            "chunks": chunks,
            "text": result["text"]
        }

        # Create JSON filename
        json_filename = f"{file_name}.json"

        json_path = os.path.join(
            JSON_FOLDER,
            json_filename
        )

        with open(
            json_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                chunks_with_metadata,
                f,
                ensure_ascii=False,
                indent=4
            )

        print(
            f"JSON saved: {json_path}"
        )

    except Exception as e:

        print(
            f"Failed to transcribe {audio}"
        )

        print(e)