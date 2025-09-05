# # experience_matcher.py
# import re
# from datetime import datetime
# from rapidfuzz import fuzz

# class ExperienceMatcher:
#     EXPERIENCE_KEYWORDS = ['experience', 'work history', 'professional experience',
#                            'career summary', 'employment history']
#     SECTION_END_KEYWORDS = ['projects', 'education', 'skills', 'achievements',
#                             'awards', 'publications', 'certifications', 'references']

#     @staticmethod
#     def _normalize_text(text: str) -> str:
#         if not text:
#             return ""
#         text = text.replace('\r\n', '\n').replace('\r', '\n')
#         # Normalize dashes
#         text = text.replace('\u2013', '-').replace('\u2014', '-').replace('–', '-').replace('—', '-')
#         # Normalize spaces
#         text = re.sub(r'\s+', ' ', text, flags=re.UNICODE)
#         return text

#     @classmethod
#     def extract_section_text(cls, text: str) -> str:
#         text = cls._normalize_text(text)
#         lines = text.split('\n')

#         start_idx, end_idx = -1, len(lines)
#         for i, ln in enumerate(lines):
#             stripped_lower = ln.lower().strip()
#             for kw in cls.EXPERIENCE_KEYWORDS:
#                 if kw in stripped_lower:
#                     start_idx = i
#                     break
#             if start_idx != -1:
#                 break

#         if start_idx == -1:
#             return "", False  # not present

#         for j in range(start_idx + 1, len(lines)):
#             stripped_lower = lines[j].lower().strip()
#             for kw in cls.SECTION_END_KEYWORDS:
#                 if kw in stripped_lower:
#                     end_idx = j
#                     break
#             if end_idx != len(lines):
#                 break

#         return "\n".join(lines[start_idx + 1:end_idx]).strip(), True

#     @staticmethod
#     def extract_job_title_from_jd(jd_text: str):
#         if not jd_text:
#             return None
#         jd = jd_text.lower()
#         patterns = [
#             r'role[:\s-]+(.+)',
#             r'job title[:\s-]+(.+)',
#             r'position[:\s-]+(.+)',
#             r'looking for a[:\s-]+(.+)',
#             r'hiring a[:\s-]+(.+)'
#         ]
#         for pat in patterns:
#             m = re.search(pat, jd, flags=re.IGNORECASE)
#             if m:
#                 return m.group(1).split('\n')[0].strip()
#         return None

#     @staticmethod
#     def extract_job_titles_from_resume(exp_text: str):
#         titles = []
#         lines = exp_text.split('\n')
#         for ln in lines:
#             s = ln.strip()
#             if not s or s.startswith(('-', '•', '*')):
#                 continue
#             if re.search(r'\b(19|20)\d{2}\b', s):  # has year
#                 title_part = re.sub(r'\d{4}.*', '', s)
#                 words = title_part.split()
#                 if words:
#                     title = " ".join(words[:6])
#                     titles.append(title)
#         return list(dict.fromkeys(titles))

#     @staticmethod
#     def compare_roles(resume_titles, jd_title, threshold=50):
#         if not jd_title or not resume_titles:
#             return 0
#         best = max((fuzz.token_sort_ratio(rt.lower(), jd_title.lower()) for rt in resume_titles), default=0)
#         return best if best >= threshold else int(best * 0.5)

#     @staticmethod
#     def calculate_total_experience(exp_text: str) -> float:
#         if not exp_text:
#             return 0.0

#         text = ExperienceMatcher._normalize_text(exp_text)

#         # Patterns: Month YYYY - Month YYYY / Present OR bare YYYY-YYYY
#         patterns = [
#             r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{4}\s*-\s*(Present|Current|Now|\d{4})',
#             r'(\d{4})\s*-\s*(Present|Current|Now|\d{4})'
#         ]

#         total_months = 0
#         for pat in patterns:
#             for match in re.finditer(pat, text, flags=re.IGNORECASE):
#                 start, end = match.groups()

#                 # --- Start date ---
#                 sy = re.search(r'\d{4}', start)
#                 if not sy:
#                     continue
#                 start_year = int(sy.group())
#                 sm = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', start, flags=re.I)
#                 start_month = datetime.strptime(sm.group(1)[:3], '%b').month if sm else 1

#                 # --- End date ---
#                 if re.search(r'present|current|now', end, flags=re.I):
#                     end_year, end_month = datetime.now().year, datetime.now().month
#                 else:
#                     ey = re.search(r'\d{4}', end)
#                     if not ey:
#                         continue
#                     end_year = int(ey.group())
#                     em = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', end, flags=re.I)
#                     end_month = datetime.strptime(em.group(1)[:3], '%b').month if em else 12

#                 months = (end_year - start_year) * 12 + (end_month - start_month) + 1
#                 if months > 0:
#                     total_months += months

#         return round(total_months / 12, 1)

#     @classmethod
#     def calculate_experience_score(cls, resume_text: str, job_description_text: str):
#         jd_title = cls.extract_job_title_from_jd(job_description_text)
#         exp_section, present = cls.extract_section_text(resume_text)

#         resume_titles = cls.extract_job_titles_from_resume(exp_section)
#         total_years = cls.calculate_total_experience(exp_section)
#         role_score = cls.compare_roles(resume_titles, jd_title)
#         duration_score = min((total_years / 5.0) * 100, 100)

#         raw_score = (role_score * 0.60) + (duration_score * 0.40)
#         final_score = 0
#         if present:
#             final_score = min(100, 10 + raw_score * 0.9)  # 10% baseline

#         details = {
#             "jd_title": jd_title,
#             "resume_titles": resume_titles,
#             "total_years": total_years,
#             "role_match_score": role_score,
#             "duration_score": round(duration_score, 1),
#             "section_present": present
#         }

#         print("[DEBUG EXPERIENCE] Present:", present, "Raw:", raw_score, "Final:", final_score,
#               "Years:", total_years, "Titles:", resume_titles)

#         return round(final_score, 2), details


# import re
# from rapidfuzz import fuzz
# import nltk
# from nltk.tokenize import sent_tokenize

# # Ensure punkt is available
# try:
#     nltk.data.find('tokenizers/punkt')
# except LookupError:
#     nltk.download('punkt', quiet=True)

# # Lazy load SBERT
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


# class ExperienceMatcher:
#     """Matches resume experience against JD experience requirements."""

#     SECTION_KEYWORDS = ["experience", "work experience", "professional experience", "employment history"]
#     SECTION_END_KEYWORDS = ["skills", "projects", "education", "achievements", "certifications"]

#     @classmethod
#     def extract_section(cls, text, keywords):
#         """Extracts the experience section using fuzzy match."""
#         lines = text.lower().split("\n")
#         section_lines = []
#         in_section = False
#         for line in lines:
#             stripped = line.strip()
#             if not stripped:
#                 continue
#             if not in_section and any(fuzz.ratio(stripped, kw) > 85 for kw in keywords):
#                 in_section = True
#                 continue
#             if in_section:
#                 if any(fuzz.ratio(stripped, end_kw) > 85 for end_kw in cls.SECTION_END_KEYWORDS):
#                     break
#                 section_lines.append(line)
#         return "\n".join(section_lines)

#     @staticmethod
#     def _rule_based_match(resume_exp, jd_text):
#         """Rule-based keyword/fuzzy match."""
#         if not resume_exp.strip() or not jd_text.strip():
#             return 0.0, []

#         resume_sentences = sent_tokenize(resume_exp)
#         jd_sentences = sent_tokenize(jd_text)

#         matched = []
#         match_count = 0
#         for r in resume_sentences:
#             for j in jd_sentences:
#                 if fuzz.partial_ratio(r.lower(), j.lower()) > 75:
#                     matched.append((r, j))
#                     match_count += 1
#                     break
#         if not jd_sentences:
#             return 0.0, []
#         score = (match_count / len(jd_sentences)) * 100
#         return score, matched

#     @staticmethod
#     def _semantic_match(resume_exp, jd_text, threshold=0.70):
#         """Semantic sentence similarity using SBERT."""
#         model = _get_sbert()
#         if model is None or not resume_exp.strip() or not jd_text.strip():
#             return 0.0, []

#         try:
#             resume_sentences = sent_tokenize(resume_exp)
#             jd_sentences = sent_tokenize(jd_text)

#             if not resume_sentences or not jd_sentences:
#                 return 0.0, []

#             emb_resume = model.encode(resume_sentences, convert_to_tensor=True)
#             emb_jd = model.encode(jd_sentences, convert_to_tensor=True)

#             sims = util.pytorch_cos_sim(emb_resume, emb_jd)  # (n_resume, n_jd)

#             matched = []
#             match_count = 0
#             for i, r in enumerate(resume_sentences):
#                 best_j = int(sims[i].argmax())
#                 score = float(sims[i][best_j])
#                 if score >= threshold:
#                     matched.append((r, jd_sentences[best_j], round(score, 2)))
#                     match_count += 1

#             jd_count = len(jd_sentences)
#             final_score = (match_count / jd_count) * 100 if jd_count else 0.0
#             return final_score, matched
#         except Exception:
#             return 0.0, []

#     @classmethod
#     def calculate_experience_score(cls, resume_text, jd_text):
#         """Combines rule-based + semantic experience matching."""
#         resume_exp = cls.extract_section(resume_text, cls.SECTION_KEYWORDS)
#         jd_exp_req = cls.extract_section(jd_text, ["experience", "requirements", "qualifications"])

#         if not resume_exp or not jd_exp_req:
#             print("\n--- EXPERIENCE MATCHING ---")
#             print("Could not find Experience or Requirements section.")
#             print("-" * 30)
#             return 0.0, {}

#         # Rule-based
#         rb_score, rb_matches = cls._rule_based_match(resume_exp, jd_exp_req)

#         # Semantic
#         sem_score, sem_matches = cls._semantic_match(resume_exp, jd_exp_req)

#         # Weighted combination
#         final_score = 0.7 * rb_score + 0.3 * sem_score

#         print("\n--- EXPERIENCE MATCHING ---")
#         print(f"Rule-based Score: {rb_score:.2f}%")
#         print(f"Semantic Score: {sem_score:.2f}%")
#         print(f"Final Experience Score: {final_score:.2f}%")
#         print("-" * 30)

#         details = {
#             "score": final_score,
#             "rule_based": rb_score,
#             "semantic": sem_score,
#             "rule_matches": rb_matches,
#             "semantic_matches": sem_matches,
#         }
#         return round(final_score, 2), details



import re
from rapidfuzz import fuzz
import nltk
from nltk.tokenize import sent_tokenize

# Ensure punkt
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

def extract_section_advanced(text, start_keywords, end_keywords=None):
    """
    Advanced section extraction that handles variations in section headings.
    """
    if end_keywords is None:
        end_keywords = ["skills", "projects", "education", "achievements", "certifications"]
    
    lines = text.lower().split("\n")
    section_lines = []
    in_section = False
    section_variations = set()
    
    # Generate variations of start keywords
    for keyword in start_keywords:
        section_variations.add(keyword)
        section_variations.add(keyword.replace(" ", ""))
        section_variations.add(keyword.replace(" ", "-"))
        section_variations.add(keyword.replace(" ", "_"))
        # Add common abbreviations
        if "experience" in keyword:
            section_variations.add("exp")
            section_variations.add("work exp")
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        # Check if we're entering a section (with fuzzy matching)
        if not in_section:
            for variation in section_variations:
                if fuzz.ratio(stripped, variation) > 75:
                    in_section = True
                    continue

        if in_section:
            # Check if we're exiting the section
            exit_section = False
            for end_kw in end_keywords:
                if fuzz.ratio(stripped, end_kw) > 75:
                    exit_section = True
                    break
                    
            if exit_section:
                break
                
            section_lines.append(line)
    
    return "\n".join(section_lines)

class ExperienceMatcher:
    """Matches resume experience against JD experience requirements."""

    SECTION_KEYWORDS = ["experience", "work experience", "professional experience", "employment history", "work history"]
    SECTION_END_KEYWORDS = ["skills", "projects", "education", "achievements", "certifications"]

    @classmethod
    def extract_section(cls, text, keywords):
        """Extracts the experience section using advanced matching."""
        return extract_section_advanced(text, keywords, cls.SECTION_END_KEYWORDS)

    @staticmethod
    def _rule_based_match(resume_exp, jd_text):
        """Rule-based keyword/fuzzy match."""
        if not resume_exp.strip() or not jd_text.strip():
            return 0.0, []

        resume_sentences = sent_tokenize(resume_exp)
        jd_sentences = sent_tokenize(jd_text)

        matched = []
        match_count = 0
        for r in resume_sentences:
            for j in jd_sentences:
                if fuzz.partial_ratio(r.lower(), j.lower()) > 75:
                    matched.append((r, j))
                    match_count += 1
                    break
        if not jd_sentences:
            return 0.0, []
        score = (match_count / len(jd_sentences)) * 100
        return score, matched

    @staticmethod
    def _semantic_match(resume_exp, jd_text, threshold=0.70):
        """Semantic sentence similarity using SBERT."""
        model = _get_sbert()
        if model is None or not resume_exp.strip() or not jd_text.strip():
            return 0.0, []

        try:
            resume_sentences = sent_tokenize(resume_exp)
            jd_sentences = sent_tokenize(jd_text)

            if not resume_sentences or not jd_sentences:
                return 0.0, []

            emb_resume = model.encode(resume_sentences, convert_to_tensor=True)
            emb_jd = model.encode(jd_sentences, convert_to_tensor=True)

            sims = util.pytorch_cos_sim(emb_resume, emb_jd)  # (n_resume, n_jd)

            matched = []
            match_count = 0
            for i, r in enumerate(resume_sentences):
                best_j = int(sims[i].argmax())
                score = float(sims[i][best_j])
                if score >= threshold:
                    matched.append((r, jd_sentences[best_j], round(score, 2)))
                    match_count += 1

            jd_count = len(jd_sentences)
            final_score = (match_count / jd_count) * 100 if jd_count else 0.0
            return final_score, matched
        except Exception:
            return 0.0, []
        
    # Add to the SECTION_KEYWORDS list
    SECTION_KEYWORDS = [
        "experience", "work experience", "professional experience", 
        "employment history", "work history", "employment", "career",
        "professional background", "work", "employment experience"
    ]

    # Improve the extract_section_advanced function
    def extract_section_advanced(text, start_keywords, end_keywords=None):
        """
        Advanced section extraction that handles variations in section headings.
        """
        if end_keywords is None:
            end_keywords = ["skills", "projects", "education", "achievements", "certifications", "awards"]
        
        lines = text.split("\n")  # Don't convert to lowercase yet
        section_lines = []
        in_section = False
        section_variations = set()
        
        # Generate variations of start keywords
        for keyword in start_keywords:
            section_variations.add(keyword.lower())
            section_variations.add(keyword.replace(" ", "").lower())
            section_variations.add(keyword.replace(" ", "-").lower())
            section_variations.add(keyword.replace(" ", "_").lower())
        
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            if not stripped_line:
                continue
            
            line_lower = stripped_line.lower()
            
            # Check if we're entering a section (with fuzzy matching)
            if not in_section:
                for variation in section_variations:
                    if fuzz.ratio(line_lower, variation) > 75:
                        in_section = True
                        # Also check the next few lines for continuation of section header
                        for j in range(i+1, min(i+3, len(lines))):
                            next_line = lines[j].strip().lower()
                            if next_line and any(fuzz.ratio(next_line, end_kw) > 75 for end_kw in end_keywords):
                                in_section = False
                                break
                        if in_section:
                            continue

            if in_section:
                # Check if we're exiting the section
                exit_section = False
                for end_kw in end_keywords:
                    if fuzz.ratio(line_lower, end_kw) > 75:
                        exit_section = True
                        break
                        
                if exit_section:
                    break
                    
                section_lines.append(line)
        
        return "\n".join(section_lines)

    @classmethod
    def calculate_experience_score(cls, resume_text, jd_text):
        """Combines rule-based + semantic experience matching."""
        resume_exp = cls.extract_section(resume_text, cls.SECTION_KEYWORDS)
        jd_exp_req = extract_section_advanced(jd_text, ["experience", "requirements", "qualifications", "what you'll do"])

        if not resume_exp or not jd_exp_req:
            print("\n--- EXPERIENCE MATCHING ---")
            print("Could not find Experience or Requirements section.")
            print("-" * 30)
            return 0.0, {}

        # Rule-based
        rb_score, rb_matches = cls._rule_based_match(resume_exp, jd_exp_req)

        # Semantic
        sem_score, sem_matches = cls._semantic_match(resume_exp, jd_exp_req)

        # Weighted combination
        final_score = 0.7 * rb_score + 0.3 * sem_score

        print("\n--- EXPERIENCE MATCHING ---")
        print(f"Rule-based Score: {rb_score:.2f}%")
        print(f"Semantic Score: {sem_score:.2f}%")
        print(f"Final Experience Score: {final_score:.2f}%")
        print("-" * 30)

        details = {
            "score": final_score,
            "rule_based": rb_score,
            "semantic": sem_score,
            "rule_matches": rb_matches,
            "semantic_matches": sem_matches,
        }
        return round(final_score, 2), details