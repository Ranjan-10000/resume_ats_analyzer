# import re
# import string
# from nltk import word_tokenize, ngrams
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# from rapidfuzz import process, fuzz

# # Assuming skills_list.py is in the same 'ats_analyzer' directory
# from .skills_list import SKILLS

# class SkillMatcher:
#     """Handles skill extraction and scoring based on a skill database."""

#     stop_words = set(stopwords.words('english'))
#     lemmatizer = WordNetLemmatizer()

#     @classmethod
#     def extract_skills(cls, text):
#         """
#         Extracts skills from text by matching n-grams against a predefined skill database.
#         """
#         # Ensure SKILLS is a flat list
#         processed_skills = SKILLS
#         if isinstance(processed_skills, dict) and 'skills' in processed_skills:
#             processed_skills = processed_skills['skills']
#         if processed_skills and isinstance(processed_skills[0], list):
#             processed_skills = [skill for sublist in processed_skills for skill in sublist]

#         text = re.sub(r'[^\w\s.+#-]', '', text)
#         tokens = word_tokenize(text)
        
#         punctuation = string.punctuation
#         clean_tokens = []
#         for token in tokens:
#             if token.lower() not in cls.stop_words and token not in punctuation:
#                 if len(token) > 4:
#                     clean_tokens.append(cls.lemmatizer.lemmatize(token))
#                 else:
#                     clean_tokens.append(token)

#         unigrams = clean_tokens
#         bigrams = [' '.join(gram) for gram in ngrams(clean_tokens, 2)]
#         trigrams = [' '.join(gram) for gram in ngrams(clean_tokens, 3)]
        
#         all_ngrams = unigrams + bigrams + trigrams
        
#         found_skills = set()
        
#         skills_lower = [skill.lower() for skill in processed_skills]

#         for ngram in all_ngrams:
#             best_match = process.extractOne(ngram.lower(), skills_lower, scorer=fuzz.ratio)
#             if best_match and best_match[1] > 80:
#                 original_skill_index = skills_lower.index(best_match[0])
#                 found_skills.add(processed_skills[original_skill_index])
                
#         return list(found_skills)

#     @staticmethod
#     def fuzzy_match_skills(resume_skills, job_skills, threshold=80):
#         """Finds which job skills are present in the resume skills."""
#         matched = set()
#         for job_skill in job_skills:
#             best_match = process.extractOne(job_skill, resume_skills, scorer=fuzz.ratio)
#             if best_match and best_match[1] >= threshold:
#                 matched.add(job_skill)
#         return matched

#     @staticmethod
#     def calculate_score(resume_text, job_text):
#         """
#         Calculates the skill match score and returns a details dictionary for feedback.
#         """
#         resume_skills = SkillMatcher.extract_skills(resume_text)
#         job_skills = set(SkillMatcher.extract_skills(job_text))

#         if not job_skills:
#             details = {
#                 "score": 0,
#                 "matched_skills": set(),
#                 "missing_skills": set()
#             }
#             return 0, details

#         matched_skills = SkillMatcher.fuzzy_match_skills(resume_skills, list(job_skills))
#         missing_skills = job_skills - matched_skills
#         score = (len(matched_skills) / len(job_skills) * 100) if job_skills else 0

#         # --- THE KEY CHANGE: Bundle results into a single dictionary ---
#         details = {
#             "score": score,
#             "matched_skills": matched_skills,
#             "missing_skills": missing_skills
#         }
        
#         print("\n--- SKILL MATCHING ANALYSIS ---")
#         print(f"Found {len(matched_skills)} out of {len(job_skills)} required skills.")
#         print(f"Skill Match Score: {score:.2f}%")
#         print("-" * 30)

#         # --- THE FIX: Consistently return only two values ---
#         return round(score, 2), details


# # skill_matcher.py
# import re
# import string
# import nltk
# from nltk import word_tokenize, ngrams
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# from rapidfuzz import process, fuzz

# # Download required NLTK data
# try:
#     nltk.data.find('tokenizers/punkt')
# except LookupError:
#     nltk.download('punkt')

# try:
#     nltk.data.find('corpora/stopwords')
# except LookupError:
#     nltk.download('stopwords')

# try:
#     nltk.data.find('corpora/wordnet')
# except LookupError:
#     nltk.download('wordnet')

# # Assuming skills_list.py is in the same 'ats_analyzer' directory
# from .skills_list import SKILLS

# class SkillMatcher:
#     """Handles skill extraction and scoring based on a skill database."""

#     stop_words = set(stopwords.words('english'))
#     lemmatizer = WordNetLemmatizer()

#     @classmethod
#     def extract_skills(cls, text):
#         """
#         Extracts skills from text by matching n-grams against a predefined skill database.
#         """
#         # Ensure SKILLS is a flat list
#         processed_skills = SKILLS
#         if isinstance(processed_skills, dict) and 'skills' in processed_skills:
#             processed_skills = processed_skills['skills']
#         if processed_skills and isinstance(processed_skills[0], list):
#             processed_skills = [skill for sublist in processed_skills for skill in sublist]

#         text = re.sub(r'[^\w\s.+#-]', '', text)
#         tokens = word_tokenize(text)
        
#         punctuation = string.punctuation
#         clean_tokens = []
#         for token in tokens:
#             if token.lower() not in cls.stop_words and token not in punctuation:
#                 if len(token) > 4:
#                     clean_tokens.append(cls.lemmatizer.lemmatize(token))
#                 else:
#                     clean_tokens.append(token)

#         unigrams = clean_tokens
#         bigrams = [' '.join(gram) for gram in ngrams(clean_tokens, 2)]
#         trigrams = [' '.join(gram) for gram in ngrams(clean_tokens, 3)]
        
#         all_ngrams = unigrams + bigrams + trigrams
        
#         found_skills = set()
        
#         skills_lower = [skill.lower() for skill in processed_skills]

#         for ngram in all_ngrams:
#             best_match = process.extractOne(ngram.lower(), skills_lower, scorer=fuzz.ratio)
#             if best_match and best_match[1] > 80:
#                 original_skill_index = skills_lower.index(best_match[0])
#                 found_skills.add(processed_skills[original_skill_index])
                
#         return list(found_skills)

#     @staticmethod
#     def fuzzy_match_skills(resume_skills, job_skills, threshold=80):
#         """Finds which job skills are present in the resume skills."""
#         matched = set()
#         for job_skill in job_skills:
#             best_match = process.extractOne(job_skill, resume_skills, scorer=fuzz.ratio)
#             if best_match and best_match[1] >= threshold:
#                 matched.add(job_skill)
#         return matched

#     @staticmethod
#     def calculate_score(resume_text, job_text):
#         """
#         Calculates the skill match score and returns a details dictionary for feedback.
#         """
#         resume_skills = SkillMatcher.extract_skills(resume_text)
#         job_skills = set(SkillMatcher.extract_skills(job_text))

#         if not job_skills:
#             details = {
#                 "score": 0,
#                 "matched_skills": set(),
#                 "missing_skills": set()
#             }
#             return 0, details

#         matched_skills = SkillMatcher.fuzzy_match_skills(resume_skills, list(job_skills))
#         missing_skills = job_skills - matched_skills
#         score = (len(matched_skills) / len(job_skills) * 100) if job_skills else 0

#         # Bundle results into a single dictionary
#         details = {
#             "score": score,
#             "matched_skills": matched_skills,
#             "missing_skills": missing_skills
#         }
        
#         print("\n--- SKILL MATCHING ANALYSIS ---")
#         print(f"Found {len(matched_skills)} out of {len(job_skills)} required skills.")
#         print(f"Skill Match Score: {score:.2f}%")
#         print("-" * 30)

#         return round(score, 2), details



# import re
# import string
# import nltk
# from nltk import word_tokenize, ngrams
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# from rapidfuzz import process, fuzz

# # Download required NLTK data if missing
# try:
#     nltk.data.find('tokenizers/punkt')
# except LookupError:
#     nltk.download('punkt', quiet=True)
# try:
#     nltk.data.find('corpora/stopwords')
# except LookupError:
#     nltk.download('stopwords', quiet=True)
# try:
#     nltk.data.find('corpora/wordnet')
# except LookupError:
#     nltk.download('wordnet', quiet=True)

# # Assuming skills_list.py is in the same 'ats_analyzer' directory
# from .skills_list import SKILLS

# # Lazy import for sentence-transformers (semantic fallback)
# _SBERt_MODEL = None
# try:
#     from sentence_transformers import SentenceTransformer, util
# except Exception:
#     SentenceTransformer = None
#     util = None

# def _get_sbert(model_name="all-MiniLM-L6-v2"):
#     global _SBERt_MODEL
#     if _SBERt_MODEL is None:
#         if SentenceTransformer is None:
#             return None
#         _SBERt_MODEL = SentenceTransformer(model_name)
#     return _SBERt_MODEL


# class SkillMatcher:
#     """Handles skill extraction and scoring based on a skill database."""

#     stop_words = set(stopwords.words('english'))
#     lemmatizer = WordNetLemmatizer()

#     # Semantic threshold used when comparing embeddings (0-1)
#     SEMANTIC_THRESHOLD = 0.75

#     @classmethod
#     def extract_skills(cls, text):
#         """
#         Extracts skills from text by matching n-grams against a predefined skill database.
#         First tries fuzzy matching, then falls back to semantic matching (BERT) for variants.
#         """
#         # Ensure SKILLS is a flat list
#         processed_skills = SKILLS
#         if isinstance(processed_skills, dict) and 'skills' in processed_skills:
#             processed_skills = processed_skills['skills']
#         if processed_skills and isinstance(processed_skills[0], list):
#             processed_skills = [skill for sublist in processed_skills for skill in sublist]

#         # Clean text but preserve dots and plus/hash/minus commonly in tech names (react.js, c++ etc.)
#         text = re.sub(r'[^\w\s.+#-]', '', text)
#         tokens = word_tokenize(text)

#         punctuation = string.punctuation
#         clean_tokens = []
#         for token in tokens:
#             if token.lower() not in cls.stop_words and token not in punctuation:
#                 if len(token) > 4:
#                     clean_tokens.append(cls.lemmatizer.lemmatize(token))
#                 else:
#                     clean_tokens.append(token)

#         unigrams = clean_tokens
#         bigrams = [' '.join(gram) for gram in ngrams(clean_tokens, 2)]
#         trigrams = [' '.join(gram) for gram in ngrams(clean_tokens, 3)]

#         all_ngrams = unigrams + bigrams + trigrams

#         found_skills = set()

#         skills_lower = [skill.lower() for skill in processed_skills]

#         # ---- 1) Existing fuzzy matching (fast, deterministic) ----
#         for ngram in all_ngrams:
#             best_match = process.extractOne(ngram.lower(), skills_lower, scorer=fuzz.ratio)
#             if best_match and best_match[1] > 80:
#                 original_skill_index = skills_lower.index(best_match[0])
#                 found_skills.add(processed_skills[original_skill_index])

#         # ---- 2) Semantic fallback with SBERT (handles variants like 'React.js' vs 'React') ----
#         # Use ONLY if sentence-transformers is available
#         model = _get_sbert()
#         if model is not None and all_ngrams:
#             try:
#                 # encode once
#                 ngrams_lower = [ng.lower() for ng in all_ngrams]
#                 emb_ngrams = model.encode(ngrams_lower, convert_to_tensor=True)
#                 emb_skills = model.encode(skills_lower, convert_to_tensor=True)

#                 # compute similarity matrix (ngrams x skills)
#                 sims = util.pytorch_cos_sim(emb_ngrams, emb_skills)  # shape (n_ngrams, n_skills)
#                 # For each ngram, find best skill
#                 for i in range(sims.shape[0]):
#                     row = sims[i]
#                     best_idx = int(row.argmax())
#                     score = float(row[best_idx])
#                     if score >= cls.SEMANTIC_THRESHOLD:
#                         found_skills.add(processed_skills[best_idx])
#             except Exception:
#                 # If anything goes wrong in semantic path, ignore and return fuzzy results
#                 pass

#         return list(found_skills)

#     @staticmethod
#     def fuzzy_match_skills(resume_skills, job_skills, threshold=80):
#         """Finds which job skills are present in the resume skills."""
#         matched = set()
#         for job_skill in job_skills:
#             best_match = process.extractOne(job_skill, resume_skills, scorer=fuzz.ratio)
#             if best_match and best_match[1] >= threshold:
#                 matched.add(job_skill)
#         return matched

#     @staticmethod
#     def calculate_score(resume_text, job_text):
#         """
#         Calculates the skill match score and returns a details dictionary for feedback.
#         """
#         resume_skills = SkillMatcher.extract_skills(resume_text)
#         job_skills = set(SkillMatcher.extract_skills(job_text))

#         if not job_skills:
#             details = {
#                 "score": 0,
#                 "matched_skills": set(),
#                 "missing_skills": set()
#             }
#             return 0, details

#         matched_skills = SkillMatcher.fuzzy_match_skills(resume_skills, list(job_skills))
#         missing_skills = job_skills - matched_skills
#         score = (len(matched_skills) / len(job_skills) * 100) if job_skills else 0

#         details = {
#             "score": score,
#             "matched_skills": matched_skills,
#             "missing_skills": missing_skills
#         }

#         print("\n--- SKILL MATCHING ANALYSIS ---")
#         print(f"Found {len(matched_skills)} out of {len(job_skills)} required skills.")
#         print(f"Skill Match Score: {score:.2f}%")
#         print("-" * 30)

#         return round(score, 2), details


import re
import string
import nltk
from nltk import word_tokenize, ngrams
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from rapidfuzz import process, fuzz

# Download required NLTK data if missing
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

# Assuming skills_list.py is in the same 'ats_analyzer' directory
from .skills_list import SKILLS

# Lazy import for sentence-transformers (semantic fallback)
_SBERT_MODEL = None
try:
    from sentence_transformers import SentenceTransformer, util
except Exception:
    SentenceTransformer = None
    util = None

def _get_sbert(model_name="all-MiniLM-L6-v2"):
    global _SBERT_MODEL
    if _SBERT_MODEL is None:
        if SentenceTransformer is None:
            return None
        _SBERT_MODEL = SentenceTransformer(model_name)
    return _SBERT_MODEL

class SkillMatcher:
    """Handles skill extraction and scoring based on a skill database."""

    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    # Semantic threshold used when comparing embeddings (0-1)
    SEMANTIC_THRESHOLD = 0.75

    @classmethod
    def extract_skills(cls, text):
        """
        Extracts skills from text by matching n-grams against a predefined skill database.
        First tries fuzzy matching, then falls back to semantic matching (BERT) for variants.
        """
        # Ensure SKILLS is a flat list
        processed_skills = SKILLS
        if isinstance(processed_skills, dict) and 'skills' in processed_skills:
            processed_skills = processed_skills['skills']
        if processed_skills and isinstance(processed_skills[0], list):
            processed_skills = [skill for sublist in processed_skills for skill in sublist]

        # Clean text but preserve dots and plus/hash/minus commonly in tech names (react.js, c++ etc.)
        text = re.sub(r'[^\w\s.+#-]', '', text)
        tokens = word_tokenize(text)

        punctuation = string.punctuation
        clean_tokens = []
        for token in tokens:
            if token.lower() not in cls.stop_words and token not in punctuation:
                if len(token) > 4:
                    clean_tokens.append(cls.lemmatizer.lemmatize(token))
                else:
                    clean_tokens.append(token)

        unigrams = clean_tokens
        bigrams = [' '.join(gram) for gram in ngrams(clean_tokens, 2)]
        trigrams = [' '.join(gram) for gram in ngrams(clean_tokens, 3)]

        all_ngrams = unigrams + bigrams + trigrams

        found_skills = set()

        skills_lower = [skill.lower() for skill in processed_skills]

        # ---- 1) Existing fuzzy matching (fast, deterministic) ----
        for ngram in all_ngrams:
            best_match = process.extractOne(ngram.lower(), skills_lower, scorer=fuzz.ratio)
            if best_match and best_match[1] > 80:
                original_skill_index = skills_lower.index(best_match[0])
                found_skills.add(processed_skills[original_skill_index])

        # ---- 2) Semantic fallback with SBERT (handles variants like 'React.js' vs 'React') ----
        # Use ONLY if sentence-transformers is available
        model = _get_sbert()
        if model is not None and all_ngrams:
            try:
                # encode once
                ngrams_lower = [ng.lower() for ng in all_ngrams]
                emb_ngrams = model.encode(ngrams_lower, convert_to_tensor=True)
                emb_skills = model.encode(skills_lower, convert_to_tensor=True)

                # compute similarity matrix (ngrams x skills)
                sims = util.pytorch_cos_sim(emb_ngrams, emb_skills)  # shape (n_ngrams, n_skills)
                # For each ngram, find best skill
                for i in range(sims.shape[0]):
                    row = sims[i]
                    best_idx = int(row.argmax())
                    score = float(row[best_idx])
                    if score >= cls.SEMANTIC_THRESHOLD:
                        found_skills.add(processed_skills[best_idx])
            except Exception:
                # If anything goes wrong in semantic path, ignore and return fuzzy results
                pass

        return list(found_skills)

    @classmethod
    def extract_skills_from_sections(cls, text):
        """
        Extract skills from all sections of the resume, including projects.
        """
        # First try to extract skills from the entire text
        all_skills = cls.extract_skills(text)
        
        # Then specifically look for project sections
        project_patterns = [
            r'(?:projects|personal projects|academic projects)[\s\S]*?(?=(?:education|skills|experience|$))',
            r'(?:project experience|technical projects)[\s\S]*?(?=(?:education|skills|experience|$))',
        ]
        
        for pattern in project_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                project_text = match.group(0)
                project_skills = cls.extract_skills(project_text)
                all_skills.extend(project_skills)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in all_skills:
            if skill not in seen:
                seen.add(skill)
                unique_skills.append(skill)
                
        return unique_skills

    @staticmethod
    def fuzzy_match_skills(resume_skills, job_skills, threshold=80):
        """Finds which job skills are present in the resume skills."""
        matched = set()
        for job_skill in job_skills:
            best_match = process.extractOne(job_skill, resume_skills, scorer=fuzz.ratio)
            if best_match and best_match[1] >= threshold:
                matched.add(job_skill)
        return matched

    @staticmethod
    def calculate_score(resume_text, job_text):
        """
        Calculates the skill match score using skills from all sections.
        """
        # Use the improved extraction that includes project sections
        resume_skills = SkillMatcher.extract_skills_from_sections(resume_text)
        job_skills = set(SkillMatcher.extract_skills_from_sections(job_text))

        if not job_skills:
            details = {
                "score": 0,
                "matched_skills": set(),
                "missing_skills": set()
            }
            return 0, details

        matched_skills = SkillMatcher.fuzzy_match_skills(resume_skills, list(job_skills))
        missing_skills = job_skills - matched_skills
        score = (len(matched_skills) / len(job_skills) * 100) if job_skills else 0

        details = {
            "score": score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        }
        
        print("\n--- SKILL MATCHING ANALYSIS ---")
        print(f"Found {len(matched_skills)} out of {len(job_skills)} required skills.")
        print(f"Skill Match Score: {score:.2f}%")
        print("-" * 30)

        return round(score, 2), details