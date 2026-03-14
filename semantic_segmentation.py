from langchain_ai21 import AI21SemanticTextSplitter


api_key = "8DePMNiJe1OTg1AxvLmxQmHprBiewnaa"
splitter = AI21SemanticTextSplitter(api_key=api_key)

def get_segments(text):
    try:
        response = splitter.split_text(text)
        return response
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None