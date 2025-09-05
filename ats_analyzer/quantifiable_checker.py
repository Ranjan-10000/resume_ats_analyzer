# import re

# class QuantifiableChecker:
#     """
#     Scans resume text to find and score quantifiable achievements.
#     """

#     @staticmethod
#     def find_quantifiable_achievements(resume_text):
#         """
#         Finds achievements in the resume text and extracts a clean snippet around them.
#         Returns a list of unique, readable achievement phrases.
#         """
#         found_achievements = set() # Use a set to automatically handle duplicates
        
#         # Define regex patterns to find numbers, percentages, and currency
#         patterns = [
#             r'\b\d+(\.\d+)?\s*%',
#             r'[\$€£]\s*\d+[\d,.]*\s*[KMB]?',
#             r'\b\d+[\d,]*\+\b',
#             r'\b(increased|decreased|reduced|improved|automated|optimized|grew|saved|managed)\s*(?:\w+\s*){0,3}\b\d+[\d,.]*\b',
#             r'\b\d+[\d,.]*\s*(?:\w+\s*){0,3}\b(increase|decrease|reduction|improvement|automation|optimization)\b'
#         ]
        
#         # Extract a context window around each match
#         for pattern in patterns:
#             matches = re.finditer(pattern, resume_text, re.IGNORECASE)
#             for match in matches:
#                 start = max(0, match.start() - 70) # Look 70 chars before
#                 end = min(len(resume_text), match.end() + 70) # Look 70 chars after
                
#                 snippet = resume_text[start:end]
#                 snippet = snippet.replace('\n', ' ').strip()
#                 snippet = "... " + snippet + " ..."
                
#                 found_achievements.add(snippet)
        
#         return list(found_achievements)

#     @classmethod
#     def calculate_achievement_score(cls, resume_text):
#         """
#         Calculates a score and returns the list of achievements found for feedback.
#         """
#         achievements = cls.find_quantifiable_achievements(resume_text)
#         num_achievements = len(achievements)
        
#         score = 0
#         if num_achievements >= 3:
#             score = 100
#         elif num_achievements >= 1:
#             score = 50
#         else:
#             score = 0
            
#         print("\n--- QUANTIFIABLE ACHIEVEMENT ANALYSIS ---")
#         print(f"Found {num_achievements} quantifiable achievements.")
#         if achievements:
#             print("Achievements Found:")
#             for achievement in sorted(achievements): # Sorted for consistent output
#                 print(f"  - {achievement}")
#         print(f"Achievement Score: {score:.2f}%")
#         print("-" * 30)

#         # --- THE KEY CHANGE: Return the achievements list for feedback ---
#         return float(score), achievements

# quantifiable_checker.py
import re

class QuantifiableChecker:
    """
    Scans resume text to find and score quantifiable achievements.
    """

    @staticmethod
    def find_quantifiable_achievements(resume_text):
        """
        Finds achievements in the resume text and extracts a clean snippet around them.
        Returns a list of unique, readable achievement phrases.
        """
        found_achievements = set() # Use a set to automatically handle duplicates
        
        # Define regex patterns to find numbers, percentages, and currency
        patterns = [
            r'\b\d+(\.\d+)?\s*%',
            r'[\$€£]\s*\d+[\d,.]*\s*[KMB]?',
            r'\b\d+[\d,]*\+\b',
            r'\b(increased|decreased|reduced|improved|automated|optimized|grew|saved|managed)\s*(?:\w+\s*){0,3}\b\d+[\d,.]*\b',
            r'\b\d+[\d,.]*\s*(?:\w+\s*){0,3}\b(increase|decrease|reduction|improvement|automation|optimization)\b'
        ]
        
        # Extract a context window around each match
        for pattern in patterns:
            matches = re.finditer(pattern, resume_text, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 70) # Look 70 chars before
                end = min(len(resume_text), match.end() + 70) # Look 70 chars after
                
                snippet = resume_text[start:end]
                snippet = snippet.replace('\n', ' ').strip()
                snippet = "... " + snippet + " ..."
                
                found_achievements.add(snippet)
        
        return list(found_achievements)

    @classmethod
    def calculate_achievement_score(cls, resume_text):
        """
        Calculates a score and returns the list of achievements found for feedback.
        """
        achievements = cls.find_quantifiable_achievements(resume_text)
        num_achievements = len(achievements)
        
        score = 0
        if num_achievements >= 3:
            score = 100
        elif num_achievements >= 1:
            score = 50
        else:
            score = 0
            
        print("\n--- QUANTIFIABLE ACHIEVEMENT ANALYSIS ---")
        print(f"Found {num_achievements} quantifiable achievements.")
        if achievements:
            print("Achievements Found:")
            for achievement in sorted(achievements): # Sorted for consistent output
                print(f"  - {achievement}")
        print(f"Achievement Score: {score:.2f}%")
        print("-" * 30)

        # Return the achievements list for feedback
        return float(score), achievements