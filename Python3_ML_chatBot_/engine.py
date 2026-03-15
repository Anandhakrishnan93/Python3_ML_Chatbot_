from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimilarityEngine:
    def __init__(self, questions, answers, threshold=0.3):
        self.questions = questions
        self.answers = answers
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer()
        # Pre-calculate the matrix for all questions in the CSV
        self.tfidf_matrix = self.vectorizer.fit_transform(self.questions)

    def get_best_match(self, user_query):
        query_vec = self.vectorizer.transform([user_query])
        scores = cosine_similarity(query_vec, self.tfidf_matrix)
        
        idx = scores.argmax() 
        best_score = scores[0][idx]
        
        # We now return: (The Answer, The Original Question, The Score)
        return self.answers[idx], self.questions[idx], best_score