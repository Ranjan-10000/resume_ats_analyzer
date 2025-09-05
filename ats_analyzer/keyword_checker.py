# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# from collections import Counter

# class KeywordChecker:
#     """
#     Analyzes keyword density and alignment between the resume and job description.
#     """
#     stop_words = set(stopwords.words('english'))
#     lemmatizer = WordNetLemmatizer()
    
#     # Custom stop words to remove generic business nouns
#     custom_stop_words = set([
#         'company', 'team', 'work', 'experience', 'role', 'job', 'candidate', 'skills', 
#         'qualifications', 'requirements', 'responsibilities', 'knowledge', 'field',
#         'ability', 'system', 'process', 'tool', 'platform', 'solution', 'technology',
#         'project', 'business', 'insights'
#     ])

#     @classmethod
#     def extract_keywords_from_jd(cls, jd_text):
#         """Extracts key nouns and verbs from the job description."""
#         lemmatized_tokens = []
#         tokens = nltk.word_tokenize(jd_text.lower())
#         tagged_tokens = nltk.pos_tag(tokens)

#         for word, tag in tagged_tokens:
#             if word.isalpha() and len(word) > 2 and word not in cls.stop_words and word not in cls.custom_stop_words:
#                 # We care about nouns (NN, NNP, NNS) and verbs (VB, VBG, VBN, VBP, VBZ)
#                 if tag.startswith('NN') or tag.startswith('VB'):
#                     lemmatized_tokens.append(cls.lemmatizer.lemmatize(word, pos='v' if tag.startswith('VB') else 'n'))
        
#         return set(lemmatized_tokens)

#     @classmethod
#     def calculate_keyword_score(cls, resume_text, job_description_text):
#         """
#         Calculates the keyword density score and returns a details dictionary for feedback.
#         """
#         jd_keywords = cls.extract_keywords_from_jd(job_description_text)
        
#         resume_tokens = nltk.word_tokenize(resume_text.lower())
#         total_resume_words = len(resume_tokens)
        
#         # Lemmatize resume tokens for accurate matching
#         lemmatized_resume_tokens = []
#         tagged_resume_tokens = nltk.pos_tag(resume_tokens)
#         for word, tag in tagged_resume_tokens:
#             if word.isalpha():
#                  lemmatized_resume_tokens.append(cls.lemmatizer.lemmatize(word, pos='v' if tag.startswith('VB') else 'n'))

#         # Find which JD keywords are present in the resume
#         resume_keywords_found = [token for token in lemmatized_resume_tokens if token in jd_keywords]
        
#         total_keyword_count = len(resume_keywords_found)
#         density = (total_keyword_count / total_resume_words) * 100 if total_resume_words > 0 else 0
        
#         # Grade the density
#         score = 0
#         if density >= 2.0:
#             score = 100
#         elif density >= 1.5:
#             score = 75
#         elif density >= 1.0:
#             score = 50
#         elif density > 0:
#             score = 25

#         # Create a count of each keyword found for detailed feedback
#         keywords_found_counts = Counter(resume_keywords_found)

#         # --- THE KEY CHANGE: Create a details dictionary for feedback ---
#         details = {
#             "jd_keywords": jd_keywords,
#             "resume_keywords_found_counts": keywords_found_counts,
#             "density": density,
#             "score": score
#         }

#         print("\n--- KEYWORD OPTIMIZATION ANALYSIS ---")
#         print(f"Resume Keyword Density: {density:.2f} keywords per 100 words.")
#         print(f"Keyword Score: {score:.2f}%")
#         print("-" * 30)
        
#         return float(score), details


# keyword_checker.py
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

class KeywordChecker:
    """
    Analyzes keyword density and alignment between the resume and job description.
    """
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    # Custom stop words to remove generic business nouns
    custom_stop_words = set([
        'company', 'team', 'work', 'experience', 'role', 'job', 'candidate', 'skills', 
        'qualifications', 'requirements', 'responsibilities', 'knowledge', 'field',
        'ability', 'system', 'process', 'tool', 'platform', 'solution', 'technology',
        'project', 'business', 'insights'
    ])

    @classmethod
    def extract_keywords_from_jd(cls, jd_text):
        """Extracts key nouns and verbs from the job description."""
        lemmatized_tokens = []
        tokens = nltk.word_tokenize(jd_text.lower())
        tagged_tokens = nltk.pos_tag(tokens)

        for word, tag in tagged_tokens:
            if word.isalpha() and len(word) > 2 and word not in cls.stop_words and word not in cls.custom_stop_words:
                # We care about nouns (NN, NNP, NNS) and verbs (VB, VBG, VBN, VBP, VBZ)
                if tag.startswith('NN') or tag.startswith('VB'):
                    lemmatized_tokens.append(cls.lemmatizer.lemmatize(word, pos='v' if tag.startswith('VB') else 'n'))
        
        return set(lemmatized_tokens)

    @classmethod
    def calculate_keyword_score(cls, resume_text, job_description_text):
        """
        Calculates the keyword density score and returns a details dictionary for feedback.
        """
        jd_keywords = cls.extract_keywords_from_jd(job_description_text)
        
        resume_tokens = nltk.word_tokenize(resume_text.lower())
        total_resume_words = len(resume_tokens)
        
        # Lemmatize resume tokens for accurate matching
        lemmatized_resume_tokens = []
        tagged_resume_tokens = nltk.pos_tag(resume_tokens)
        for word, tag in tagged_resume_tokens:
            if word.isalpha():
                 lemmatized_resume_tokens.append(cls.lemmatizer.lemmatize(word, pos='v' if tag.startswith('VB') else 'n'))

        # Find which JD keywords are present in the resume
        resume_keywords_found = [token for token in lemmatized_resume_tokens if token in jd_keywords]
        
        total_keyword_count = len(resume_keywords_found)
        density = (total_keyword_count / total_resume_words) * 100 if total_resume_words > 0 else 0
        
        # Grade the density
        score = 0
        if density >= 2.0:
            score = 100
        elif density >= 1.5:
            score = 75
        elif density >= 1.0:
            score = 50
        elif density > 0:
            score = 25

        # Create a count of each keyword found for detailed feedback
        keywords_found_counts = Counter(resume_keywords_found)

        # Create a details dictionary for feedback
        details = {
            "jd_keywords": jd_keywords,
            "resume_keywords_found_counts": keywords_found_counts,
            "density": density,
            "score": score
        }

        print("\n--- KEYWORD OPTIMIZATION ANALYSIS ---")
        print(f"Resume Keyword Density: {density:.2f} keywords per 100 words.")
        print(f"Keyword Score: {score:.2f}%")
        print("-" * 30)
        
        return float(score), details