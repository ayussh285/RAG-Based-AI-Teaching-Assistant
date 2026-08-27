from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import joblib
import requests

def create_embedding(text_list):
    r= requests.post("http://localhost:11434/api/embed" , json ={
        "model":"bge-m3",
        "input":  text_list
    })

    embedding = r.json()['embeddings']
    return embedding

def inference(prompt):
    r= requests.post("http://localhost:11434/api/generate" , json ={
        "model":"llama3.2",
        "prompt": prompt,
        "stream": False
    })
    response = r.json()
    return response

def format_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

# incoming_query = input("Ask a question: ")
df = joblib.load("embeddings.joblib")
embedding_matrix = np.vstack(df["embedding"])

def process_query(incoming_query):

    question_embedding = create_embedding([incoming_query])[0]
    # print(question_embedding)   

    similarities = cosine_similarity(
        embedding_matrix,
        [question_embedding]
    ).flatten()

    # Get top 5 results
    top_result = 5
    max_indx = similarities.argsort()[::-1][:top_result]

    # Apply similarity threshold
    threshold = 0.45

    relevant_indices = [
        index for index in max_indx
        if similarities[index] >= threshold
    ]

    if not relevant_indices:
        return "I couldn't find this topic in the provided lectures."

    new_df = df.iloc[relevant_indices].copy()
    new_df["start_time"] = new_df["start"].apply(format_timestamp)
    new_df["end_time"] = new_df["end"].apply(format_timestamp)

    # Store similarity score for debugging / evaluation
    new_df["similarity"] = [
        similarities[index] for index in relevant_indices
    ]

    # Best matching chunk
    best_match = new_df.iloc[0]

    best_video = best_match["number"]
    best_title = best_match["title"]
    best_start = best_match["start_time"]
    best_end = best_match["end_time"]
    best_similarity = best_match["similarity"]

    prompt = f"""
    You are VidMentor, an AI Teaching Assistant for a Computer Graphics lecture playlist.

    Your task is to help the user find where a particular topic is taught in the provided lecture videos.

    IMPORTANT RULES:
    1. Use ONLY the provided lecture chunks.
    2. Never invent a video name, video number, timestamp, or information.
    3. Select the most relevant lecture chunk based primarily on the similarity score.
    4. Prefer the chunk with the highest similarity when determining the main answer.
    5. You may use other retrieved chunks as supporting context.
    6. If the topic is not clearly present in the provided chunks, say:
       "I couldn't find this topic in the provided lectures."
    7. If the query is unrelated to Computer Graphics, say:
       "Please ask a question related to the provided Computer Graphics lectures."
    8. Use the provided start_time and end_time directly.
    9. Keep the answer concise.

    BEST MATCH:
    Video: {best_video} - {best_title}
    Timestamp: {best_start} - {best_end}
    Similarity: {best_similarity:.3f}

    LECTURE CHUNKS:
    {new_df[["title", "number", "text", "start_time", "end_time", "similarity"]].to_json(orient="records")}

    USER QUERY:
    "{incoming_query}"

    If the topic is found, respond in this format:

    🎯 Topic Found

    📺 Video: <video number> - <video title>
    ⏱️ Timestamp: <start time> - <end time>

    📝 < Explanation of what is discussed in this section.>

    Do not provide information that is not supported by the lecture chunks.
    """
    
    # with open ("prompt.txt","w") as f:
    #     f.write(prompt)

    response = inference(prompt)["response"]
    # with open ("response.txt", "w") as f:
    #     f.write(response)
    # for index , item in new_df.iterrows():
    #     print(index, item['title'], item['number'], item['text'], item['start'], item['end'])
    return response