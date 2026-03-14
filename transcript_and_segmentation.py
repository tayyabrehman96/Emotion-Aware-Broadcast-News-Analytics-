import assemblyai as aai

aai.settings.api_key = "faf583b5e8354055a1e310f4ec0632c0"

# audio_file = "./local_file.mp3"
# audio_file = "C:\\Users\\pc\\Desktop\\Neo4j Intuition\\downloads\\BREAKING Israel may have used US-supplied weapons in breach of international law in Gaza  BBC News.mp4"


def get_segments(video_file):
    config = aai.TranscriptionConfig(iab_categories=True)
    transcript = aai.Transcriber().transcribe(video_file, config)

    # Initialize an empty list for text segments
    text_segments = []

    # Loop through the results to extract text segments
    for result in transcript.iab_categories.results:
        # Append the text segment to the list
        text_segments.append(result.text)

    # Display the resulting list of text segments
    # print("Text Segments:")
    # print(text_segments)
    return text_segments
