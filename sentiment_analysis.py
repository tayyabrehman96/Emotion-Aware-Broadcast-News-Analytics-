from transformers import pipeline
from rephrase import rephrase_text

# Load the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def get_sentiment(text):
    candidate_labels = ["positive", "negative", "neutral"]

    # Get the initial sentiment classification result
    result = classifier(text, candidate_labels)

    highest_score_idx = result['scores'].index(max(result['scores']))
    highest_score_label = result['labels'][highest_score_idx]
    highest_score = result['scores'][highest_score_idx]
    
    print("Initial Sentiment Analysis:")
    print("Label:", highest_score_label)
    print("Score:", highest_score)

    max_attempts = 5  # Maximum number of rephrasing attempts
    attempt = 0  # Initialize the attempt counter
    new_score = lowest_score = highest_score  # Track the lowest score encountered
    new_score_label = lowest_score_label = highest_score_label
    best_rephrased_text = text  # Track the rephrased text with the lowest score

    while attempt < max_attempts:
        # If the score is below 80%, return the best rephrased text and the label
        if lowest_score < 0.80:
            print("Sentiment score is below 80%. Returning result.")
            return best_rephrased_text, lowest_score_label, highest_score, lowest_score

        print(f"Sentiment is too strong ({new_score_label} with {new_score*100:.2f}%). Rephrasing...")

        rephrased = rephrase_text(text)

        # Get the sentiment classification result for rephrased text
        result = classifier(rephrased, candidate_labels)

        new_score_idx = result['scores'].index(max(result['scores']))
        new_score_label = result['labels'][new_score_idx]
        new_score = result['scores'][new_score_idx]

        print("Rephrased Sentiment Analysis:")
        print("Label:", new_score_label)
        print("Score:", new_score)

        # Update the lowest score and best rephrased text if applicable
        if new_score < lowest_score:
            lowest_score = new_score
            lowest_score_label = new_score_label
            best_rephrased_text = rephrased

        attempt += 1
        print("#########################################################")

    print("Maximum attempts reached! Returning the result with the lowest sentiment score.")

    return best_rephrased_text, lowest_score_label, highest_score, lowest_score
