# import re
# from spellchecker import SpellChecker
# from nltk.corpus import stopwords
# import string

# class FormattingChecker:
#     """
#     Analyzes the resume for ATS-friendly formatting, structure, and professionalism.
#     """
    
#     # --- THE FIX: Added 'technical skills' and other variations ---
#     STRUCTURE_KEYWORDS = {
#         'summary': ['summary', 'objective', 'profile', 'about'],
#         'experience': ['experience', 'work history', 'professional experience'],
#         'education': ['education', 'academic background', 'qualifications'],
#         'skills': ['skills', 'technical skills', 'core competencies', 'technical expertise']
#     }
    
#     PRONOUNS = {'i', 'me', 'my', 'myself'}
#     ACTION_VERBS_ENDINGS = ('ed', 'ing', 's', 'te', 'ize', 'fy')

#     @classmethod
#     def check_structure(cls, resume_text):
#         """Checks if the resume contains standard sections."""
#         # ... existing code ...
#         text_lower = resume_text.lower()
#         found_sections = 0
#         for section, keywords in cls.STRUCTURE_KEYWORDS.items():
#             if any(keyword in text_lower for keyword in keywords):
#                 found_sections += 1
        
#         # Simple scoring: 25 points per section found
#         return found_sections * 25

#     @classmethod
#     def check_professionalism(cls, resume_text):
#         """Checks for resume length and use of bullet points."""
#         # ... existing code ...
#         lines = resume_text.split('\n')
#         words = resume_text.split()
        
#         # a) Length Score (30 points)
#         word_count = len(words)
#         length_score = 30 if 250 <= word_count <= 800 else 15
        
#         # b) Bullet Point Usage (30 points)
#         bullet_lines = [line for line in lines if line.strip().startswith(('•', '*', '-'))]
#         bullet_score = 30 if len(bullet_lines) > 3 else 0

#         # c) Action Verb Usage (40 points)
#         action_verb_count = 0
#         for line in bullet_lines:
#             first_word = line.strip().lstrip('•*- ').split(' ')[0]
#             if first_word.lower().endswith(cls.ACTION_VERBS_ENDINGS):
#                 action_verb_count += 1
        
#         action_verb_score = 40 if bullet_lines and (action_verb_count / len(bullet_lines)) > 0.5 else 0

#         total_score = length_score + bullet_score + action_verb_score
#         return total_score

#     @classmethod
#     def check_correctness(cls, resume_text):
#         """Checks for spelling errors and first-person pronouns."""
#         # ... existing code ...
#         spell = SpellChecker()
#         stop_words = set(stopwords.words('english'))
        
#         words = re.findall(r'\b\w+\b', resume_text.lower())
        
#         # a) Spelling Score (50 points)
#         misspelled = spell.unknown([word for word in words if word not in stop_words])
#         total_words = len(words)
#         spelling_accuracy = ((total_words - len(misspelled)) / total_words) * 100 if total_words > 0 else 100
#         spelling_score = 50 if spelling_accuracy >= 98 else 25 if spelling_accuracy >= 95 else 0

#         # b) Pronoun Check (50 points)
#         found_pronouns = [word for word in words if word in cls.PRONOUNS]
#         pronoun_count = len(found_pronouns)
#         pronoun_score = 50 if pronoun_count == 0 else 0

#         total_score = spelling_score + pronoun_score
#         return total_score, pronoun_count, spelling_accuracy

#     @classmethod
#     def calculate_formatting_score(cls, resume_text):
#         """Calculates the final weighted formatting score."""
#         # ... existing code ...
#         structure_score = cls.check_structure(resume_text)
#         professionalism_score = cls.check_professionalism(resume_text)
#         correctness_score, pronoun_count, spelling_accuracy = cls.check_correctness(resume_text)

#         # Apply weights: Structure (40%), Professionalism (30%), Correctness (30%)
#         final_score = (structure_score * 0.40) + (professionalism_score * 0.30) + (correctness_score * 0.30)

#         details = {
#             "score": final_score,
#             "structure_score": structure_score,
#             "professionalism_score": professionalism_score,
#             "correctness_score": correctness_score,
#             "pronoun_count": pronoun_count,
#             "spelling_score": (correctness_score - (50 if pronoun_count == 0 else 0)) * 2, # Rescale to 100
#         }
#         return final_score, details


# formatting_checker.py
import re
from spellchecker import SpellChecker
from nltk.corpus import stopwords
import string

class FormattingChecker:
    """
    Analyzes the resume for ATS-friendly formatting, structure, and professionalism.
    """
    
    # Added 'technical skills' and other variations
    STRUCTURE_KEYWORDS = {
        'summary': ['summary', 'objective', 'profile', 'about'],
        'experience': ['experience', 'work history', 'professional experience'],
        'education': ['education', 'academic background', 'qualifications'],
        'skills': ['skills', 'technical skills', 'core competencies', 'technical expertise']
    }
    
    PRONOUNS = {'i', 'me', 'my', 'myself'}
    ACTION_VERBS_ENDINGS = ('ed', 'ing', 's', 'te', 'ize', 'fy')

    @classmethod
    def check_structure(cls, resume_text):
        """Checks if the resume contains standard sections."""
        text_lower = resume_text.lower()
        found_sections = 0
        for section, keywords in cls.STRUCTURE_KEYWORDS.items():
            if any(keyword in text_lower for keyword in keywords):
                found_sections += 1
        
        # Simple scoring: 25 points per section found
        return found_sections * 25

    @classmethod
    def check_professionalism(cls, resume_text):
        """Checks for resume length and use of bullet points."""
        lines = resume_text.split('\n')
        words = resume_text.split()
        
        # a) Length Score (30 points)
        word_count = len(words)
        length_score = 30 if 250 <= word_count <= 800 else 15
        
        # b) Bullet Point Usage (30 points)
        bullet_lines = [line for line in lines if line.strip().startswith(('•', '*', '-'))]
        bullet_score = 30 if len(bullet_lines) > 3 else 0

        # c) Action Verb Usage (40 points)
        action_verb_count = 0
        for line in bullet_lines:
            first_word = line.strip().lstrip('•*- ').split(' ')[0]
            if first_word.lower().endswith(cls.ACTION_VERBS_ENDINGS):
                action_verb_count += 1
        
        action_verb_score = 40 if bullet_lines and (action_verb_count / len(bullet_lines)) > 0.5 else 0

        total_score = length_score + bullet_score + action_verb_score
        return total_score

    @classmethod
    def check_correctness(cls, resume_text):
        """Checks for spelling errors and first-person pronouns."""
        spell = SpellChecker()
        stop_words = set(stopwords.words('english'))
        
        words = re.findall(r'\b\w+\b', resume_text.lower())
        
        # a) Spelling Score (50 points)
        misspelled = spell.unknown([word for word in words if word not in stop_words])
        total_words = len(words)
        spelling_accuracy = ((total_words - len(misspelled)) / total_words) * 100 if total_words > 0 else 100
        spelling_score = 50 if spelling_accuracy >= 98 else 25 if spelling_accuracy >= 95 else 0

        # b) Pronoun Check (50 points)
        found_pronouns = [word for word in words if word in cls.PRONOUNS]
        pronoun_count = len(found_pronouns)
        pronoun_score = 50 if pronoun_count == 0 else 0

        total_score = spelling_score + pronoun_score
        return total_score, pronoun_count, spelling_accuracy

    @classmethod
    def calculate_formatting_score(cls, resume_text):
        """Calculates the final weighted formatting score."""
        structure_score = cls.check_structure(resume_text)
        professionalism_score = cls.check_professionalism(resume_text)
        correctness_score, pronoun_count, spelling_accuracy = cls.check_correctness(resume_text)

        # Apply weights: Structure (40%), Professionalism (30%), Correctness (30%)
        final_score = (structure_score * 0.40) + (professionalism_score * 0.30) + (correctness_score * 0.30)

        details = {
            "score": final_score,
            "structure_score": structure_score,
            "professionalism_score": professionalism_score,
            "correctness_score": correctness_score,
            "pronoun_count": pronoun_count,
            "spelling_score": (correctness_score - (50 if pronoun_count == 0 else 0)) * 2, # Rescale to 100
        }
        return final_score, details