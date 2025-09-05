# import re
# from rapidfuzz import fuzz

# class EducationChecker:
#     """
#     Analyzes and scores the alignment between a candidate's education and the job requirements.
#     """

#     EDUCATION_KEYWORDS = ['education', 'academic background', 'qualifications']
#     JD_QUALIFICATION_KEYWORDS = ['required skills and qualifications', 'qualifications', 'requirements', 'minimum qualifications']
    
#     SECTION_END_KEYWORDS = [
#         'projects', 'experience', 'skills', 'achievements', 'awards', 
#         'publications', 'certifications', 'references', 'preferred qualifications'
#     ]

#     DEGREE_LEVELS = {
#         "bachelor": 1, "b.tech": 1, "be": 1, "bsc": 1,
#         "master": 2, "m.tech": 2, "me": 2, "msc": 2,
#         "phd": 3, "doctorate": 3
#     }

#     FIELD_ALIASES = {
#         "cse": "computer science",
#         "cs": "computer science",
#         "ece": "electronics and communication engineering",
#         "it": "information technology"
#     }

#     FIELD_SYNONYMS = {
#         "computer science": [
#             "cs", "cse", "ai", "artificial intelligence", "ml",
#             "machine learning", "deep learning", "reinforcement learning",
#             "data science", "data analytics"
#         ],
#         "engineering": [
#             "ece", "eee", "it", "information technology",
#             "mechanical", "civil", "electronics"
#         ]
#     }

#     @classmethod
#     def extract_section(cls, text, start_keywords):
#         """Extracts a section from resume or JD based on keywords."""
#         lines = text.lower().split('\n')
#         section_text = []
#         in_section = False
#         for line in lines:
#             stripped_line = line.strip()
#             if not stripped_line:
#                 continue
            
#             if not in_section and any(fuzz.ratio(stripped_line, keyword) > 85 for keyword in start_keywords):
#                 in_section = True
#                 continue

#             if in_section:
#                 if any(fuzz.ratio(stripped_line, keyword) > 85 for keyword in cls.SECTION_END_KEYWORDS):
#                     break
#                 section_text.append(line)
#         return "\n".join(section_text)

#     @staticmethod
#     def parse_resume_education(education_text):
#         """
#         Improved extraction to handle fields like:
#         'B.Tech - Computer Science and Engineering – CGPA: 8.26'
#         """
#         degree_level = 0
#         field_of_study = ""
#         gpa = 0.0

#         # Find highest degree level
#         for degree, level in EducationChecker.DEGREE_LEVELS.items():
#             if re.search(r'\b' + re.escape(degree) + r'\b', education_text, re.IGNORECASE):
#                 degree_level = max(degree_level, level)

#         # Match field of study after degree
#         match = re.search(
#             r'(?:b\.?tech|bachelor[\w\s]*)[-\s]*(?:in\s+)?([\w\s&\-]+)',
#             education_text,
#             re.IGNORECASE
#         )
#         if match:
#             field_of_study = match.group(1).strip()

#         # Normalize aliases
#         field_of_study_lower = field_of_study.lower()
#         if field_of_study_lower in EducationChecker.FIELD_ALIASES:
#             field_of_study = EducationChecker.FIELD_ALIASES[field_of_study_lower]

#         # Extract GPA
#         gpa_match = re.search(r'(cgpa|gpa):\s*(\d+\.\d+)', education_text, re.IGNORECASE)
#         if gpa_match:
#             gpa = float(gpa_match.group(2))

#         return degree_level, field_of_study, gpa

#     @staticmethod
#     def parse_jd_requirements(jd_text):
#         """Parses JD for degree level & fields."""
#         required_level = 0
#         required_fields = []

#         for degree, level in EducationChecker.DEGREE_LEVELS.items():
#             if re.search(r'\b' + degree + r"'?s?\b", jd_text, re.IGNORECASE):
#                 required_level = max(required_level, level)

#         match = re.search(r'(?:degree in|in)\s+([\w\s,]+(?:or\s+[\w\s,]+)?)', jd_text, re.IGNORECASE)
#         if match:
#             fields_str = match.group(1)
#             required_fields = [field.strip().lower() for field in re.split(r',|\bor\b', fields_str) if field.strip()]

#         return required_level, required_fields

#     @classmethod
#     def calculate_education_score(cls, resume_text, job_description_text):
#         """Calculates final education alignment score."""
#         resume_education_section = cls.extract_section(resume_text, cls.EDUCATION_KEYWORDS)
#         jd_qual_section = cls.extract_section(job_description_text, cls.JD_QUALIFICATION_KEYWORDS)

#         if not resume_education_section or not jd_qual_section:
#             print("\n--- EDUCATION ALIGNMENT ANALYSIS ---")
#             print("Could not find Education or Qualification sections.")
#             print("-" * 30)
#             return 0.0, {}

#         resume_level, resume_field, resume_gpa = cls.parse_resume_education(resume_education_section)
#         jd_level, jd_fields = cls.parse_jd_requirements(jd_qual_section)

#         # --- Scoring ---
#         level_score = 50.0 if resume_level >= jd_level else 0.0

#         field_score = 0.0
#         if resume_field and jd_fields:
#             resume_field_lower = resume_field.lower()
#             match_found = False

#             for jd_field in jd_fields:
#                 jd_field_lower = jd_field.lower()

#                 # Direct containment
#                 if jd_field_lower in resume_field_lower or resume_field_lower in jd_field_lower:
#                     field_score = 30.0
#                     match_found = True
#                     break

#                 # Synonym expansion
#                 if jd_field_lower in cls.FIELD_SYNONYMS:
#                     for synonym in cls.FIELD_SYNONYMS[jd_field_lower]:
#                         if synonym in resume_field_lower:
#                             field_score = 30.0
#                             match_found = True
#                             break

#                 if match_found:
#                     break

#             # Fallback fuzzy similarity
#             if not match_found:
#                 best_match_score = max(
#                     fuzz.partial_ratio(resume_field_lower, jd_field.lower()) for jd_field in jd_fields
#                 )
#                 if best_match_score > 80:
#                     field_score = 30.0

#         gpa_score = 20.0 if resume_gpa >= 7.5 else 0.0
#         total_score = level_score + field_score + gpa_score

#         print("\n--- EDUCATION ALIGNMENT ANALYSIS ---")
#         print(f"JD Requires: Level {jd_level}, Fields {jd_fields}")
#         print(f"Resume Has: Level {resume_level}, Field '{resume_field.title()}', GPA {resume_gpa}")
#         print("-" * 20)
#         print(f"Degree Level Score: {level_score}/50")
#         print(f"Field of Study Score: {field_score}/30")
#         print(f"GPA Score: {gpa_score}/20")
#         print("-" * 20)
#         print(f"Final Education Score: {total_score:.2f}/100")
#         print("-" * 30)

#         details = {
#             "score": total_score,
#             "field_score": field_score,
#             "resume_details": {
#                 "level": resume_level,
#                 "field": resume_field,
#                 "gpa": resume_gpa
#             },
#             "jd_details": {
#                 "level": jd_level,
#                 "fields": jd_fields
#             }
#         }
        
#         return total_score, details


# education_checker.py
# import re
# from rapidfuzz import fuzz

# class EducationChecker:
#     """
#     Analyzes and scores the alignment between a candidate's education and the job requirements.
#     """

#     EDUCATION_KEYWORDS = ['education', 'academic background', 'qualifications']
#     JD_QUALIFICATION_KEYWORDS = ['required skills and qualifications', 'qualifications', 'requirements', 'minimum qualifications']
    
#     SECTION_END_KEYWORDS = [
#         'projects', 'experience', 'skills', 'achievements', 'awards', 
#         'publications', 'certifications', 'references', 'preferred qualifications'
#     ]

#     DEGREE_LEVELS = {
#         "bachelor": 1, "b.tech": 1, "be": 1, "bsc": 1,
#         "master": 2, "m.tech": 2, "me": 2, "msc": 2,
#         "phd": 3, "doctorate": 3
#     }

#     FIELD_ALIASES = {
#         "cse": "computer science",
#         "cs": "computer science",
#         "ece": "electronics and communication engineering",
#         "it": "information technology"
#     }

#     FIELD_SYNONYMS = {
#         "computer science": [
#             "cs", "cse", "ai", "artificial intelligence", "ml",
#             "machine learning", "deep learning", "reinforcement learning",
#             "data science", "data analytics"
#         ],
#         "engineering": [
#             "ece", "eee", "it", "information technology",
#             "mechanical", "civil", "electronics"
#         ]
#     }

#     @classmethod
#     def extract_section(cls, text, start_keywords):
#         """Extracts a section from resume or JD based on keywords."""
#         lines = text.lower().split('\n')
#         section_text = []
#         in_section = False
#         for line in lines:
#             stripped_line = line.strip()
#             if not stripped_line:
#                 continue
            
#             if not in_section and any(fuzz.ratio(stripped_line, keyword) > 85 for keyword in start_keywords):
#                 in_section = True
#                 continue

#             if in_section:
#                 if any(fuzz.ratio(stripped_line, keyword) > 85 for keyword in cls.SECTION_END_KEYWORDS):
#                     break
#                 section_text.append(line)
#         return "\n".join(section_text)

#     @staticmethod
#     def parse_resume_education(education_text):
#         """
#         Improved extraction to handle fields like:
#         'B.Tech - Computer Science and Engineering – CGPA: 8.26'
#         """
#         degree_level = 0
#         field_of_study = ""
#         gpa = 0.0

#         # Find highest degree level
#         for degree, level in EducationChecker.DEGREE_LEVELS.items():
#             if re.search(r'\b' + re.escape(degree) + r'\b', education_text, re.IGNORECASE):
#                 degree_level = max(degree_level, level)

#         # Match field of study after degree
#         match = re.search(
#             r'(?:b\.?tech|bachelor[\w\s]*)[-\s]*(?:in\s+)?([\w\s&\-]+)',
#             education_text,
#             re.IGNORECASE
#         )
#         if match:
#             field_of_study = match.group(1).strip()

#         # Normalize aliases
#         field_of_study_lower = field_of_study.lower()
#         if field_of_study_lower in EducationChecker.FIELD_ALIASES:
#             field_of_study = EducationChecker.FIELD_ALIASES[field_of_study_lower]

#         # Extract GPA
#         gpa_match = re.search(r'(cgpa|gpa):\s*(\d+\.\d+)', education_text, re.IGNORECASE)
#         if gpa_match:
#             gpa = float(gpa_match.group(2))

#         return degree_level, field_of_study, gpa

#     @staticmethod
#     def parse_jd_requirements(jd_text):
#         """Parses JD for degree level & fields."""
#         required_level = 0
#         required_fields = []

#         for degree, level in EducationChecker.DEGREE_LEVELS.items():
#             if re.search(r'\b' + degree + r"'?s?\b", jd_text, re.IGNORECASE):
#                 required_level = max(required_level, level)

#         match = re.search(r'(?:degree in|in)\s+([\w\s,]+(?:or\s+[\w\s,]+)?)', jd_text, re.IGNORECASE)
#         if match:
#             fields_str = match.group(1)
#             required_fields = [field.strip().lower() for field in re.split(r',|\bor\b', fields_str) if field.strip()]

#         return required_level, required_fields

#     @classmethod
#     def calculate_education_score(cls, resume_text, job_description_text):
#         """Calculates final education alignment score."""
#         resume_education_section = cls.extract_section(resume_text, cls.EDUCATION_KEYWORDS)
#         jd_qual_section = cls.extract_section(job_description_text, cls.JD_QUALIFICATION_KEYWORDS)

#         if not resume_education_section or not jd_qual_section:
#             print("\n--- EDUCATION ALIGNMENT ANALYSIS ---")
#             print("Could not find Education or Qualification sections.")
#             print("-" * 30)
#             return 0.0, {}
        
#         resume_level, resume_field, resume_gpa = cls.parse_resume_education(resume_education_section)
#         jd_level, jd_fields = cls.parse_jd_requirements(jd_qual_section)

#         # --- Scoring ---
#         level_score = 50.0 if resume_level >= jd_level else 0.0

#         field_score = 0.0
#         if resume_field and jd_fields:
#             resume_field_lower = resume_field.lower()
#             match_found = False

#             for jd_field in jd_fields:
#                 jd_field_lower = jd_field.lower()

#                 # Direct containment
#                 if jd_field_lower in resume_field_lower or resume_field_lower in jd_field_lower:
#                     field_score = 30.0
#                     match_found = True
#                     break

#                 # Synonym expansion
#                 if jd_field_lower in cls.FIELD_SYNONYMS:
#                     for synonym in cls.FIELD_SYNONYMS[jd_field_lower]:
#                         if synonym in resume_field_lower:
#                             field_score = 30.0
#                             match_found = True
#                             break

#                 if match_found:
#                     break

#             # Fallback fuzzy similarity
#             if not match_found:
#                 best_match_score = max(
#                     fuzz.partial_ratio(resume_field_lower, jd_field.lower()) for jd_field in jd_fields
#                 )
#                 if best_match_score > 80:
#                     field_score = 30.0

#         gpa_score = 20.0 if resume_gpa >= 7.5 else 0.0
#         total_score = level_score + field_score + gpa_score

#         print("\n--- EDUCATION ALIGNMENT ANALYSIS ---")
#         print(f"JD Requires: Level {jd_level}, Fields {jd_fields}")
#         print(f"Resume Has: Level {resume_level}, Field '{resume_field.title()}', GPA {resume_gpa}")
#         print("-" * 20)
#         print(f"Degree Level Score: {level_score}/50")
#         print(f"Field of Study Score: {field_score}/30")
#         print(f"GPA Score: {gpa_score}/20")
#         print("-" * 20)
#         print(f"Final Education Score: {total_score:.2f}/100")
#         print("-" * 30)

#         details = {
#             "score": total_score,
#             "field_score": field_score,
#             "resume_details": {
#                 "level": resume_level,
#                 "field": resume_field,
#                 "gpa": resume_gpa
#             },
#             "jd_details": {
#                 "level": jd_level,
#                 "fields": jd_fields
#             }
#         }
        
#         return total_score, details


# import re
# from rapidfuzz import fuzz
# import nltk
# from nltk.tokenize import sent_tokenize

# # ensure punkt exists
# try:
#     nltk.data.find('tokenizers/punkt')
# except LookupError:
#     nltk.download('punkt', quiet=True)

# # Lazy SBERT import
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


# class EducationChecker:
#     """
#     Analyzes and scores the alignment between a candidate's education and the job requirements.
#     """

#     EDUCATION_KEYWORDS = ['education', 'academic background', 'qualifications']
#     JD_QUALIFICATION_KEYWORDS = ['required skills and qualifications', 'qualifications', 'requirements', 'minimum qualifications']

#     SECTION_END_KEYWORDS = [
#         'projects', 'experience', 'skills', 'achievements', 'awards',
#         'publications', 'certifications', 'references', 'preferred qualifications'
#     ]

#     DEGREE_LEVELS = {
#         "bachelor": 1, "b.tech": 1, "be": 1, "bsc": 1,
#         "master": 2, "m.tech": 2, "me": 2, "msc": 2,
#         "phd": 3, "doctorate": 3
#     }

#     FIELD_ALIASES = {
#         "cse": "computer science",
#         "cs": "computer science",
#         "ece": "electronics and communication engineering",
#         "it": "information technology"
#     }

#     FIELD_SYNONYMS = {
#         "computer science": [
#             "cs", "cse", "ai", "artificial intelligence", "ml",
#             "machine learning", "deep learning", "reinforcement learning",
#             "data science", "data analytics"
#         ],
#         "engineering": [
#             "ece", "eee", "it", "information technology",
#             "mechanical", "civil", "electronics"
#         ]
#     }

#     @classmethod
#     def extract_section(cls, text, start_keywords):
#         """Extracts a section from resume or JD based on keywords using fuzzy matching."""
#         lines = text.lower().split('\n')
#         section_text = []
#         in_section = False
#         for line in lines:
#             stripped_line = line.strip()
#             if not stripped_line:
#                 continue

#             if not in_section and any(fuzz.ratio(stripped_line, keyword) > 85 for keyword in start_keywords):
#                 in_section = True
#                 continue

#             if in_section:
#                 if any(fuzz.ratio(stripped_line, keyword) > 85 for keyword in cls.SECTION_END_KEYWORDS):
#                     break
#                 section_text.append(line)
#         return "\n".join(section_text)

#     @classmethod
#     def _semantic_find_education_section(cls, full_text, top_k=5, threshold=0.55):
#         """
#         Use SBERT to find sentences in resume that look like education lines.
#         Returns a joined string of candidate sentences (or empty string).
#         """
#         model = _get_sbert()
#         if model is None:
#             return ""

#         # templates representative of education lines
#         templates = [
#             "Bachelor of Technology", "B.Tech", "Bachelor of Engineering", "B.E.",
#             "Bachelor's degree", "Master's degree", "M.Tech", "M.Sc", "PhD", "Doctorate",
#             "graduated with", "cgpa", "gpa", "class of", "degree in"
#         ]

#         try:
#             sentences = sent_tokenize(full_text)
#         except Exception:
#             sentences = full_text.split('\n')

#         if not sentences:
#             return ""

#         sent_embs = model.encode(sentences, convert_to_tensor=True)
#         templ_embs = model.encode(templates, convert_to_tensor=True)
#         sims = util.pytorch_cos_sim(sent_embs, templ_embs)  # shape (n_sentences, n_templates)

#         # take max similarity per sentence
#         scores = sims.max(dim=1)[0].cpu().tolist()
#         ranked = sorted(list(zip(sentences, scores)), key=lambda x: x[1], reverse=True)
#         selected = [s for s, sc in ranked if sc >= threshold][:top_k]
#         return "\n".join(selected)

#     @classmethod
#     def _semantic_detect_field(cls, education_text, threshold=0.60):
#         """
#         Use SBERT to detect the canonical field (e.g., 'computer science') from text.
#         """
#         model = _get_sbert()
#         if model is None or not education_text.strip():
#             return ""

#         # Candidate canonical fields
#         candidates = [
#             "computer science", "information technology", "electronics and communication engineering",
#             "mechanical engineering", "civil engineering", "data science", "mathematics", "physics"
#         ]
#         try:
#             ed_emb = model.encode(education_text, convert_to_tensor=True)
#             cand_embs = model.encode(candidates, convert_to_tensor=True)
#             sims = util.pytorch_cos_sim(ed_emb, cand_embs)[0]
#             best_idx = int(sims.argmax())
#             best_score = float(sims[best_idx])
#             if best_score >= threshold:
#                 return candidates[best_idx]
#         except Exception:
#             pass
#         return ""

#     @staticmethod
#     def parse_resume_education(education_text):
#         """
#         Improved extraction to handle fields like:
#         'B.Tech - Computer Science and Engineering – CGPA: 8.26'
#         """
#         degree_level = 0
#         field_of_study = ""
#         gpa = 0.0

#         # Find highest degree level
#         for degree, level in EducationChecker.DEGREE_LEVELS.items():
#             if re.search(r'\b' + re.escape(degree) + r'\b', education_text, re.IGNORECASE):
#                 degree_level = max(degree_level, level)

#         # Improved field of study matching with more patterns
#         patterns = [
#             r'(?:b\.?tech|bachelor[\w\s]*|be|b\.e|bsc|b\.sc)[\s:-]*(?:in\s+)?([\w\s&,.-]+)',
#             r'(?:master[\w\s]*|m\.?tech|ms|m\.sc|me|m\.e)[\s:-]*(?:in\s+)?([\w\s&,.-]+)',
#             r'(?:phd|doctorate)[\s:-]*(?:in\s+)?([\w\s&,.-]+)',
#             r'([\w\s&,.-]+?)\s*(?:\(?\s*(?:b\.?tech|bachelor|be|b\.e|bsc|b\.sc|master|m\.?tech|ms|m\.sc|me|m\.e|phd|doctorate)\s*\)?)',
#         ]
        
#         for pattern in patterns:
#             match = re.search(pattern, education_text, re.IGNORECASE)
#             if match:
#                 field_candidate = match.group(1).strip()
#                 # Filter out common non-field words
#                 if not re.search(r'\b(?:university|college|institute|school|degree|cgpa|gpa|percentage|%|grade)\b', 
#                             field_candidate, re.IGNORECASE):
#                     field_of_study = field_candidate
#                     break

#         # Normalize aliases
#         field_of_study_lower = field_of_study.lower()
#         for alias, canonical in EducationChecker.FIELD_ALIASES.items():
#             if alias in field_of_study_lower:
#                 field_of_study = canonical
#                 break

#         # Extract GPA with more patterns
#         gpa_patterns = [
#             r'(?:cgpa|gpa)[\s:]*(\d+\.\d+)',
#             r'(\d+\.\d+)\s*(?:cgpa|gpa)',
#             r'(\d+\.\d+)\s*\/\s*\d+\.\d+',  # 8.26/10.0 format
#         ]
        
#         for pattern in gpa_patterns:
#             gpa_match = re.search(pattern, education_text, re.IGNORECASE)
#             if gpa_match:
#                 try:
#                     gpa = float(gpa_match.group(1))
#                     break
#                 except ValueError:
#                     continue

#         # If no field found, try semantic detection
#         if not field_of_study:
#             sem_field = EducationChecker._semantic_detect_field(education_text)
#             if sem_field:
#                 field_of_study = sem_field

#         return degree_level, field_of_study, gpa

#     @staticmethod
#     def parse_jd_requirements(jd_text):
#         """Parses JD for degree level & fields."""
#         required_level = 0
#         required_fields = []

#         for degree, level in EducationChecker.DEGREE_LEVELS.items():
#             if re.search(r'\b' + degree + r"'?s?\b", jd_text, re.IGNORECASE):
#                 required_level = max(required_level, level)

#         match = re.search(r'(?:degree in|in)\s+([\w\s,]+(?:or\s+[\w\s,]+)?)', jd_text, re.IGNORECASE)
#         if match:
#             fields_str = match.group(1)
#             required_fields = [field.strip().lower() for field in re.split(r',|\bor\b', fields_str) if field.strip()]

#         return required_level, required_fields

#     @classmethod
#     def calculate_education_score(cls, resume_text, job_description_text):
#         """Calculates final education alignment score."""
#         resume_education_section = cls.extract_section(resume_text, cls.EDUCATION_KEYWORDS)

#         # If no explicit education section found, use semantic search across whole resume
#         if not resume_education_section.strip():
#             resume_education_section = cls._semantic_find_education_section(resume_text)

#         jd_qual_section = cls.extract_section(job_description_text, cls.JD_QUALIFICATION_KEYWORDS)
#         if not resume_education_section or not jd_qual_section:
#             print("\n--- EDUCATION ALIGNMENT ANALYSIS ---")
#             print("Could not find Education or Qualification sections.")
#             print("-" * 30)
#             # Even when JD section is missing, try to parse and return partial info
#             if not resume_education_section:
#                 return 0.0, {}
#             # If JD missing, return resume parsed info with zero JD expectations
#             resume_level, resume_field, resume_gpa = cls.parse_resume_education(resume_education_section)
#             details = {
#                 "score": 0.0,
#                 "field_score": 0.0,
#                 "resume_details": {
#                     "level": resume_level,
#                     "field": resume_field,
#                     "gpa": resume_gpa
#                 },
#                 "jd_details": {
#                     "level": 0,
#                     "fields": []
#                 }
#             }
#             return 0.0, details

#         resume_level, resume_field, resume_gpa = cls.parse_resume_education(resume_education_section)
#         jd_level, jd_fields = cls.parse_jd_requirements(jd_qual_section)

#         # --- Scoring (rule-based, preserved) ---
#         level_score = 50.0 if resume_level >= jd_level else 0.0

#         field_score = 0.0
#         if resume_field and jd_fields:
#             resume_field_lower = resume_field.lower()
#             match_found = False

#             for jd_field in jd_fields:
#                 jd_field_lower = jd_field.lower()

#                 # Direct containment
#                 if jd_field_lower in resume_field_lower or resume_field_lower in jd_field_lower:
#                     field_score = 30.0
#                     match_found = True
#                     break

#                 # Synonym expansion
#                 if jd_field_lower in cls.FIELD_SYNONYMS:
#                     for synonym in cls.FIELD_SYNONYMS[jd_field_lower]:
#                         if synonym in resume_field_lower:
#                             field_score = 30.0
#                             match_found = True
#                             break

#                 if match_found:
#                     break

#             # Fallback fuzzy similarity
#             if not match_found:
#                 best_match_score = max(
#                     fuzz.partial_ratio(resume_field_lower, jd_field.lower()) for jd_field in jd_fields
#                 )
#                 if best_match_score > 80:
#                     field_score = 30.0

#         gpa_score = 20.0 if resume_gpa >= 7.5 else 0.0
#         total_score = level_score + field_score + gpa_score

#         print("\n--- EDUCATION ALIGNMENT ANALYSIS ---")
#         print(f"JD Requires: Level {jd_level}, Fields {jd_fields}")
#         print(f"Resume Has: Level {resume_level}, Field '{resume_field.title() if resume_field else ''}', GPA {resume_gpa}")
#         print("-" * 20)
#         print(f"Degree Level Score: {level_score}/50")
#         print(f"Field of Study Score: {field_score}/30")
#         print(f"GPA Score: {gpa_score}/20")
#         print("-" * 20)
#         print(f"Final Education Score: {total_score:.2f}/100")
#         print("-" * 30)

#         details = {
#             "score": total_score,
#             "field_score": field_score,
#             "resume_details": {
#                 "level": resume_level,
#                 "field": resume_field,
#                 "gpa": resume_gpa
#             },
#             "jd_details": {
#                 "level": jd_level,
#                 "fields": jd_fields
#             }
#         }

#         return total_score, details
















import re
from rapidfuzz import fuzz
import nltk
from nltk.tokenize import sent_tokenize

# ensure punkt exists
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

# Lazy SBERT import
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

class EducationChecker:
    """
    Analyzes and scores the alignment between a candidate's education and the job requirements.
    """

    EDUCATION_KEYWORDS = ['education', 'academic background', 'qualifications', 'academics', 'educational qualifications']
    JD_QUALIFICATION_KEYWORDS = ['required skills and qualifications', 'qualifications', 'requirements', 'minimum qualifications', 'education requirements']
    
    SECTION_END_KEYWORDS = [
        'projects', 'experience', 'skills', 'achievements', 'awards', 
        'publications', 'certifications', 'references', 'preferred qualifications',
        'work experience', 'technical skills', 'professional experience'
    ]

    DEGREE_LEVELS = {
        "bachelor": 1, "b.tech": 1, "be": 1, "bsc": 1, "b.e.": 1, "b.sc.": 1, "btech": 1,
        "master": 2, "m.tech": 2, "me": 2, "msc": 2, "m.e.": 2, "m.sc.": 2, "mtech": 2, "ms": 2,
        "phd": 3, "doctorate": 3, "ph.d.": 3
    }

    FIELD_ALIASES = {
        "cse": "computer science",
        "cs": "computer science",
        "ece": "electronics and communication engineering",
        "it": "information technology",
        "eee": "electrical and electronics engineering",
        "mech": "mechanical engineering",
        "civil": "civil engineering"
    }

    FIELD_SYNONYMS = {
        "computer science": [
            "cs", "cse", "ai", "artificial intelligence", "ml",
            "machine learning", "deep learning", "reinforcement learning",
            "data science", "data analytics", "computer engineering", "software engineering"
        ],
        "engineering": [
            "ece", "eee", "it", "information technology",
            "mechanical", "civil", "electronics", "electrical"
        ]
    }

    @classmethod
    def extract_section(cls, text, start_keywords):
        """Extracts a section from resume or JD based on keywords using fuzzy matching."""
        lines = text.lower().split('\n')
        section_text = []
        in_section = False
        
        # Generate variations of start keywords
        section_variations = set()
        for keyword in start_keywords:
            section_variations.add(keyword)
            section_variations.add(keyword.replace(" ", ""))
            section_variations.add(keyword.replace(" ", "-"))
            section_variations.add(keyword.replace(" ", "_"))
            # Add common abbreviations
            if "education" in keyword:
                section_variations.add("edu")
                section_variations.add("academics")
        
        for line in lines:
            stripped_line = line.strip()
            if not stripped_line:
                continue

            if not in_section:
                for variation in section_variations:
                    if fuzz.ratio(stripped_line, variation) > 75:
                        in_section = True
                        continue

            if in_section:
                if any(fuzz.ratio(stripped_line, end_kw) > 75 for end_kw in cls.SECTION_END_KEYWORDS):
                    break
                section_text.append(line)
        return "\n".join(section_text)

    @classmethod
    def _semantic_find_education_section(cls, full_text, top_k=5, threshold=0.55):
        """
        Use SBERT to find sentences in resume that look like education lines.
        Returns a joined string of candidate sentences (or empty string).
        """
        model = _get_sbert()
        if model is None:
            return ""

        # templates representative of education lines
        templates = [
            "Bachelor of Technology", "B.Tech", "Bachelor of Engineering", "B.E.",
            "Bachelor's degree", "Master's degree", "M.Tech", "M.Sc", "PhD", "Doctorate",
            "graduated with", "cgpa", "gpa", "class of", "degree in", "university", "college",
            "institute of technology", "CGPA", "GPA", "percentage", "aggregate"
        ]

        try:
            sentences = sent_tokenize(full_text)
        except Exception:
            sentences = full_text.split('\n')

        if not sentences:
            return ""

        sent_embs = model.encode(sentences, convert_to_tensor=True)
        templ_embs = model.encode(templates, convert_to_tensor=True)
        sims = util.pytorch_cos_sim(sent_embs, templ_embs)  # shape (n_sentences, n_templates)

        # take max similarity per sentence
        scores = sims.max(dim=1)[0].cpu().tolist()
        ranked = sorted(list(zip(sentences, scores)), key=lambda x: x[1], reverse=True)
        selected = [s for s, sc in ranked if sc >= threshold][:top_k]
        return "\n".join(selected)

    @classmethod
    def _semantic_detect_field(cls, education_text, threshold=0.60):
        """
        Use SBERT to detect the canonical field (e.g., 'computer science') from text.
        """
        model = _get_sbert()
        if model is None or not education_text.strip():
            return ""

        # Candidate canonical fields
        candidates = [
            "computer science", "information technology", "electronics and communication engineering",
            "mechanical engineering", "civil engineering", "data science", "mathematics", "physics",
            "electrical engineering", "software engineering", "computer engineering"
        ]
        try:
            ed_emb = model.encode(education_text, convert_to_tensor=True)
            cand_embs = model.encode(candidates, convert_to_tensor=True)
            sims = util.pytorch_cos_sim(ed_emb, cand_embs)[0]
            best_idx = int(sims.argmax())
            best_score = float(sims[best_idx])
            if best_score >= threshold:
                return candidates[best_idx]
        except Exception:
            pass
        return ""

    @staticmethod
    def parse_resume_education(education_text):
        """
        Improved extraction to handle fields with better pattern matching.
        """
        degree_level = 0
        field_of_study = ""
        gpa = 0.0

        # Find highest degree level
        for degree, level in EducationChecker.DEGREE_LEVELS.items():
            if re.search(r'\b' + re.escape(degree) + r'\b', education_text, re.IGNORECASE):
                degree_level = max(degree_level, level)

        # Improved field of study patterns - look for common degree patterns
        patterns = [
            r'(?:b\.?tech|bachelor[\w\s]*|be|b\.e|bsc|b\.sc)[\s:-]*(?:in\s+)?([\w\s&,.-]+?)(?=\s*(?:university|college|institute|\.|$))',
            r'(?:master[\w\s]*|m\.?tech|ms|m\.sc|me|m\.e)[\s:-]*(?:in\s+)?([\w\s&,.-]+?)(?=\s*(?:university|college|institute|\.|$))',
            r'(?:phd|doctorate)[\s:-]*(?:in\s+)?([\w\s&,.-]+?)(?=\s*(?:university|college|institute|\.|$))',
            r'([\w\s&,.-]+?(?:engineering|science|technology|studies|arts))(?=\s*(?:\(?\s*(?:b\.?tech|bachelor|be|b\.e|bsc|b\.sc|master|m\.?tech|ms|m\.sc|me|m\.e|phd|doctorate)\s*\)?|\.|$))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, education_text, re.IGNORECASE)
            if match:
                field_candidate = match.group(1).strip()
                # Filter out common non-field words and dates
                if (not re.search(r'\b(?:university|college|institute|school|degree|cgpa|gpa|percentage|%|grade|20\d{2}|19\d{2})\b', 
                            field_candidate, re.IGNORECASE) and
                    len(field_candidate.split()) > 1):  # Should have at least 2 words
                    field_of_study = field_candidate
                    break

        # Normalize aliases
        field_of_study_lower = field_of_study.lower()
        for alias, canonical in EducationChecker.FIELD_ALIASES.items():
            if alias in field_of_study_lower:
                field_of_study = canonical
                break

        # Extract GPA with more patterns, focusing on professional GPA, not academic scores
        gpa_patterns = [
            r'(?:cgpa|gpa)[\s:]*(\d+\.\d+)(?=\s*(?:out of|\/|$))',
            r'(\d+\.\d+)\s*(?:cgpa|gpa)(?=\s*(?:out of|\/|$))',
        ]
        
        for pattern in gpa_patterns:
            gpa_match = re.search(pattern, education_text, re.IGNORECASE)
            if gpa_match:
                try:
                    gpa = float(gpa_match.group(1))
                    # Only accept GPA if it's in reasonable range (not academic percentages)
                    if 0 <= gpa <= 10:  # GPA typically 0-10 scale
                        break
                except ValueError:
                    continue

        # If no field found, try semantic detection
        if not field_of_study or len(field_of_study.split()) < 2:
            sem_field = EducationChecker._semantic_detect_field(education_text)
            if sem_field:
                field_of_study = sem_field

        return degree_level, field_of_study, gpa

    @staticmethod
    def parse_jd_requirements(jd_text):
        """Parses JD for degree level & fields."""
        required_level = 0
        required_fields = []

        for degree, level in EducationChecker.DEGREE_LEVELS.items():
            if re.search(r'\b' + degree + r"'?s?\b", jd_text, re.IGNORECASE):
                required_level = max(required_level, level)

        # Improved field extraction from JD
        field_patterns = [
            r'(?:degree|background|studies|major)[\s]*in[\s]*([\w\s,]+(?:or[\s]*[\w\s,]+)?)',
            r'(?:bachelor|master|phd)[\s]*(?:in|of)[\s]*([\w\s,]+(?:or[\s]*[\w\s,]+)?)',
            r'(?:field|discipline)[\s]*of[\s]*([\w\s,]+(?:or[\s]*[\w\s,]+)?)'
        ]
        
        for pattern in field_patterns:
            match = re.search(pattern, jd_text, re.IGNORECASE)
            if match:
                fields_str = match.group(1)
                # Split by commas or "or"
                required_fields = [field.strip().lower() for field in re.split(r',|\bor\b', fields_str) if field.strip()]
                break

        return required_level, required_fields

    @classmethod
    def calculate_education_score(cls, resume_text, job_description_text):
        """Calculates final education alignment score."""
        resume_education_section = cls.extract_section(resume_text, cls.EDUCATION_KEYWORDS)

        # If no explicit education section found, use semantic search across whole resume
        if not resume_education_section.strip():
            resume_education_section = cls._semantic_find_education_section(resume_text)

        jd_qual_section = cls.extract_section(job_description_text, cls.JD_QUALIFICATION_KEYWORDS)
        if not resume_education_section or not jd_qual_section:
            print("\n--- EDUCATION ALIGNMENT ANALYSIS ---")
            print("Could not find Education or Qualification sections.")
            print("-" * 30)
            # Even when JD section is missing, try to parse and return partial info
            if not resume_education_section:
                return 0.0, {}
            # If JD missing, return resume parsed info with zero JD expectations
            resume_level, resume_field, resume_gpa = cls.parse_resume_education(resume_education_section)
            details = {
                "score": 0.0,
                "field_score": 0.0,
                "resume_details": {
                    "level": resume_level,
                    "field": resume_field,
                    "gpa": resume_gpa
                },
                "jd_details": {
                    "level": 0,
                    "fields": []
                }
            }
            return 0.0, details

        resume_level, resume_field, resume_gpa = cls.parse_resume_education(resume_education_section)
        jd_level, jd_fields = cls.parse_jd_requirements(jd_qual_section)

        # --- Scoring (rule-based, preserved) ---
        level_score = 50.0 if resume_level >= jd_level else 0.0

        field_score = 0.0
        if resume_field and jd_fields:
            resume_field_lower = resume_field.lower()
            match_found = False

            for jd_field in jd_fields:
                jd_field_lower = jd_field.lower()

                # Direct containment
                if jd_field_lower in resume_field_lower or resume_field_lower in jd_field_lower:
                    field_score = 30.0
                    match_found = True
                    break

                # Synonym expansion
                if jd_field_lower in cls.FIELD_SYNONYMS:
                    for synonym in cls.FIELD_SYNONYMS[jd_field_lower]:
                        if synonym in resume_field_lower:
                            field_score = 30.0
                            match_found = True
                            break

                if match_found:
                    break

            # Fallback fuzzy similarity
            if not match_found:
                best_match_score = max(
                    fuzz.partial_ratio(resume_field_lower, jd_field.lower()) for jd_field in jd_fields
                )
                if best_match_score > 80:
                    field_score = 30.0

        gpa_score = 20.0 if resume_gpa >= 7.5 else 0.0
        total_score = level_score + field_score + gpa_score

        print("\n--- EDUCATION ALIGNMENT ANALYSIS ---")
        print(f"JD Requires: Level {jd_level}, Fields {jd_fields}")
        print(f"Resume Has: Level {resume_level}, Field '{resume_field.title() if resume_field else ''}', GPA {resume_gpa}")
        print("-" * 20)
        print(f"Degree Level Score: {level_score}/50")
        print(f"Field of Study Score: {field_score}/30")
        print(f"GPA Score: {gpa_score}/20")
        print("-" * 20)
        print(f"Final Education Score: {total_score:.2f}/100")
        print("-" * 30)

        details = {
            "score": total_score,
            "field_score": field_score,
            "resume_details": {
                "level": resume_level,
                "field": resume_field,
                "gpa": resume_gpa
            },
            "jd_details": {
                "level": jd_level,
                "fields": jd_fields
            }
        }

        return total_score, details