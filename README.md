# How to Use the RAG AI Teaching Assistant with Your Own Data

## Step 1 — Collect Your Educational Data

You can provide your educational content in two ways.

### Method 1 — Local Video Files

Collect all your lecture or educational video files and store them in the `videos` folder.

Then proceed to **Step 2**.

### Method 2 — YouTube Playlist

Run `new.py` and enter the URL of your YouTube educational playlist when prompted.

The program will automatically download the audio from the playlist videos and generate the required JSON transcript files.

After the process is completed, proceed directly to **Step 4**.

---

## Step 2 — Convert Videos to MP3

Run `video_to_mp3.py` to convert all video files into MP3 audio files.

The generated audio files will be stored in the `audios` folder.

---

## Step 3 — Convert MP3 to JSON

Run `mp3_to_json.py` to transcribe the audio files using Whisper.

This generates JSON files containing:

* Video number
* Video title
* Transcribed text
* Start timestamp
* End timestamp

The JSON files will be stored in the `jsons` folder.

---

## Step 4 — Merge Transcript Chunks

Run `merge_chunks.py` to combine smaller Whisper transcript segments into larger chunks.

Larger and more meaningful chunks provide better context for semantic retrieval and improve the quality of the LLM's response.

The processed chunks will be stored in the `newjsons` folder.

---

## Step 5 — Convert Chunks to Embeddings

Run `preprocess_json.py` to:

1. Read the processed JSON files.
2. Generate embeddings using the `bge-m3` embedding model.
3. Store the embeddings along with the video metadata and timestamps.
4. Save the resulting data as `embeddings.joblib`.

---

## Step 6 — Query Processing and LLM Response

Run the VidMentor application using `app.py`.

When the user enters a question:

1. The query is converted into an embedding.
2. The query embedding is compared with the stored lecture embeddings.
3. The most relevant lecture chunks are retrieved.
4. A context-aware prompt is generated using the retrieved chunks.
5. The prompt is sent to the LLM.
6. The LLM generates the final response containing the relevant lecture and timestamp.

---

## Overall Workflow

```text
Step 1 — Collect Educational Data
        │
        ├── Method 1: Local Videos
        │       ↓
        │   videos/
        │       ↓
        │   video_to_mp3.py
        │       ↓
        │   MP3 Audio
        │       ↓
        │   mp3_to_json.py
        │       ↓
        │   JSON Transcriptions
        │
        └── Method 2: YouTube Playlist
                ↓
              new.py
                ↓
              Audio + JSON Transcriptions

                    ↓
              merge_chunks.py
                    ↓
          Larger Transcript Chunks
                    ↓
          preprocess_json.py
                    ↓
             bge-m3 Embeddings
                    ↓
            embeddings.joblib
                    ↓
                User Query
                    ↓
       Embedding + Similarity Search
                    ↓
       Relevant Lecture Chunks
                    ↓
          Context-Aware Prompt
                    ↓
                Llama 3.2
                    ↓
       Answer with Video & Timestamp
                    ↓
       VidMentor Web Interface