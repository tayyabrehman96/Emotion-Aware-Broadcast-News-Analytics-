import nltk
from nltk.corpus import stopwords
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.utils import simple_preprocess
import numpy as np
from scipy.spatial.distance import cosine
from collections import defaultdict
import spacy

# # Download NLTK stopwords
# nltk.download('stopwords')

# Load spaCy model for lemmatization
nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])


##########################################################################################################

# Load GloVe model
def load_glove_model(file_path):
    glove_model = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            split_line = line.split()
            word = split_line[0]
            embedding = np.array([float(val) for val in split_line[1:]])
            glove_model[word] = embedding
    return glove_model

##########################################################################################################

# Preprocess the text
def preprocess(text):
    # Tokenization and removing stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in simple_preprocess(text, deacc=True) if word not in stop_words]
    
    # Lemmatization
    doc = nlp(" ".join(words))
    lemmatized_words = [token.lemma_ for token in doc if token.lemma_ not in stop_words]
    
    return lemmatized_words

##########################################################################################################

def processing(text):
    # Preprocess your transcription
    processed_text = preprocess(text)

    # Create a dictionary and corpus
    dictionary = corpora.Dictionary([processed_text])
    corpus = [dictionary.doc2bow(processed_text)]

    # Train LDA model
    lda_model = LdaModel(corpus, num_topics=3, id2word=dictionary, passes=15)

    return lda_model


##########################################################################################################

# Calculate cosine similarity
def cosine_similarity(vec1, vec2):
    if np.any(vec1) and np.any(vec2):  
        return 1 - cosine(vec1, vec2)
    else:
        return 0.0

# Function to get word vector
def get_word_vector(word, model):
    return model.get(word, np.zeros(100))

##########################################################################################################


# Function to label topics based on top words
def label_topics(text):
    categories = [
    'Politics', 'Business', 'Technology', 'Health', 'Science', 'Sports',
    'Entertainment', 'Environment', 'International Affairs', 'Local News', 
    'Disaster', 'Humanitarian Aid', 'Education', 'Finance', 'Law and Justice', 
    'Travel and Tourism', 'Lifestyle', 'Food and Drink', 'Culture and Arts', 
    'Religion and Spirituality', 'Social Issues', 'History', 'Fashion and Beauty', 
    'Automotive', 'Real Estate', 'Agriculture', 'Aviation', 'Energy and Utilities', 
    'Weather', 'Wildlife and Conservation', 'War', 'Inflation'
    ]

    lda_model = processing(text)
    glove_file_path = 'D:\\Work\\Paper\\Project\\models\\glove.6B.100d.txt'  # Update with the correct path
    glove_model = load_glove_model(glove_file_path)
    
    topics = lda_model.print_topics(num_words=10)
    labels = []
    
    for idx, topic in topics:
        words = topic.split('+')
        words_processed = [word.split('*')[1].strip().strip('"') for word in words]
        # print(f"Topic {idx} top words: {words}")
        
        # Calculate similarity scores for each category
        category_scores = defaultdict(float)
        for word in words_processed:
            word_vector = get_word_vector(word, glove_model)
            for category in categories:
                category_vector = get_word_vector(category.lower(), glove_model)
                similarity_score = cosine_similarity(word_vector, category_vector)
                category_scores[category] += similarity_score
        
        # Average the scores by the number of words
        for category in category_scores:
            category_scores[category] /= len(words_processed)
        
        # Assign the category with the highest score
        if category_scores:
            best_category = max(category_scores, key=category_scores.get)
            labels.append(best_category)
        else:
            labels.append('Uncategorized')

        for idx, label in enumerate(labels):
            # print(f"Topic {idx}: {label}")
            if idx==0:
                return label