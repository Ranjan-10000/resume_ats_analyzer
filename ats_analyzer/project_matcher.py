# import re
# from rapidfuzz import fuzz
# import nltk
# from nltk.tokenize import sent_tokenize

# # Ensure punkt
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


# class ProjectMatcher:
#     """Analyzes resume projects and matches them against JD responsibilities."""

#     SECTION_KEYWORDS = ["projects", "personal projects", "academic projects", "work experience"]
#     SECTION_END_KEYWORDS = ["skills", "education", "achievements", "certifications", "awards"]

#     @classmethod
#     def extract_section(cls, text, keywords):
#         """Extracts project section using fuzzy matching."""
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
#     def _rule_based_match(resume_projects, jd_text):
#         """Rule-based keyword/fuzzy match."""
#         if not resume_projects.strip() or not jd_text.strip():
#             return 0.0, []

#         project_sentences = sent_tokenize(resume_projects)
#         jd_sentences = sent_tokenize(jd_text)

#         matched_sentences = []
#         match_count = 0
#         for proj in project_sentences:
#             for jd in jd_sentences:
#                 if fuzz.partial_ratio(proj.lower(), jd.lower()) > 75:
#                     matched_sentences.append((proj, jd))
#                     match_count += 1
#                     break
#         if not jd_sentences:
#             return 0.0, []
#         score = (match_count / len(jd_sentences)) * 100
#         return score, matched_sentences

#     @staticmethod
#     def _semantic_match(resume_projects, jd_text, threshold=0.70):
#         """Semantic sentence similarity using SBERT."""
#         model = _get_sbert()
#         if model is None or not resume_projects.strip() or not jd_text.strip():
#             return 0.0, []

#         try:
#             resume_sentences = sent_tokenize(resume_projects)
#             jd_sentences = sent_tokenize(jd_text)

#             if not resume_sentences or not jd_sentences:
#                 return 0.0, []

#             emb_resume = model.encode(resume_sentences, convert_to_tensor=True)
#             emb_jd = model.encode(jd_sentences, convert_to_tensor=True)

#             sims = util.pytorch_cos_sim(emb_resume, emb_jd)  # (n_resume, n_jd)

#             matched = []
#             match_count = 0
#             for i, proj in enumerate(resume_sentences):
#                 best_j = int(sims[i].argmax())
#                 score = float(sims[i][best_j])
#                 if score >= threshold:
#                     matched.append((proj, jd_sentences[best_j], round(score, 2)))
#                     match_count += 1

#             jd_count = len(jd_sentences)
#             final_score = (match_count / jd_count) * 100 if jd_count else 0.0
#             return final_score, matched
#         except Exception:
#             return 0.0, []

#     @classmethod
#     def calculate_project_skill_score(cls, resume_text, jd_text):
#         """Combines rule-based + semantic project matching."""
#         resume_projects = cls.extract_section(resume_text, cls.SECTION_KEYWORDS)
#         jd_responsibilities = cls.extract_section(jd_text, ["responsibilities", "key responsibilities", "duties"])

#         if not resume_projects or not jd_responsibilities:
#             print("\n--- PROJECT MATCHING ---")
#             print("Could not find Projects or Responsibilities section.")
#             print("-" * 30)
#             return 0.0, {}

#         # Rule-based score
#         rb_score, rb_matches = cls._rule_based_match(resume_projects, jd_responsibilities)

#         # Semantic score
#         sem_score, sem_matches = cls._semantic_match(resume_projects, jd_responsibilities)

#         # Weighted combination: 70% rule-based, 30% semantic
#         final_score = 0.7 * rb_score + 0.3 * sem_score

#         print("\n--- PROJECT MATCHING ---")
#         print(f"Rule-based Score: {rb_score:.2f}%")
#         print(f"Semantic Score: {sem_score:.2f}%")
#         print(f"Final Project Score: {final_score:.2f}%")
#         print("-" * 30)

#         details = {
#             "score": final_score,
#             "rule_based": rb_score,
#             "semantic": sem_score,
#             "rule_matches": rb_matches,
#             "semantic_matches": sem_matches
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
        end_keywords = ["skills", "education", "experience", "achievements", "certifications"]
    
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
        if "project" in keyword:
            section_variations.add("proj")
    
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

class ProjectMatcher:
    """Analyzes resume projects and matches them against JD responsibilities."""

    SECTION_KEYWORDS = ["projects", "personal projects", "academic projects", "work experience", "project experience", "technical projects"]
    SECTION_END_KEYWORDS = ["skills", "education", "experience", "achievements", "certifications", "awards"]

    @classmethod
    def extract_section(cls, text, keywords):
        """Extracts project section using advanced matching."""
        return extract_section_advanced(text, keywords, cls.SECTION_END_KEYWORDS)

    @staticmethod
    def _rule_based_match(resume_projects, jd_text):
        """Rule-based keyword/fuzzy match."""
        if not resume_projects.strip() or not jd_text.strip():
            return 0.0, []

        project_sentences = sent_tokenize(resume_projects)
        jd_sentences = sent_tokenize(jd_text)

        matched_sentences = []
        match_count = 0
        for proj in project_sentences:
            for jd in jd_sentences:
                if fuzz.partial_ratio(proj.lower(), jd.lower()) > 75:
                    matched_sentences.append((proj, jd))
                    match_count += 1
                    break
        if not jd_sentences:
            return 0.0, []
        score = (match_count / len(jd_sentences)) * 100
        return score, matched_sentences

    @staticmethod
    def _semantic_match(resume_projects, jd_text, threshold=0.70):
        """Semantic sentence similarity using SBERT."""
        model = _get_sbert()
        if model is None or not resume_projects.strip() or not jd_text.strip():
            return 0.0, []

        try:
            resume_sentences = sent_tokenize(resume_projects)
            jd_sentences = sent_tokenize(jd_text)

            if not resume_sentences or not jd_sentences:
                return 0.0, []

            emb_resume = model.encode(resume_sentences, convert_to_tensor=True)
            emb_jd = model.encode(jd_sentences, convert_to_tensor=True)

            sims = util.pytorch_cos_sim(emb_resume, emb_jd)  # (n_resume, n_jd)

            matched = []
            match_count = 0
            for i, proj in enumerate(resume_sentences):
                best_j = int(sims[i].argmax())
                score = float(sims[i][best_j])
                if score >= threshold:
                    matched.append((proj, jd_sentences[best_j], round(score, 2)))
                    match_count += 1

            jd_count = len(jd_sentences)
            final_score = (match_count / jd_count) * 100 if jd_count else 0.0
            return final_score, matched
        except Exception:
            return 0.0, []

    @classmethod
    def extract_technologies_from_projects(cls, project_text):
        """Extract technologies mentioned in project descriptions."""
        # Common technology patterns
        tech_patterns = [
            r'\b(?:python|java|javascript|c\+\+|c#|go|rust|ruby|php|typescript|swift|kotlin|r|matlab|sql|html|css|react|angular|vue|node\.js|django|flask|spring|tensorflow|pytorch|keras|pandas|numpy|docker|kubernetes|aws|azure|gcp|git|jenkins|ansible|terraform)\b',
            r'\b(?:machine learning|deep learning|data science|natural language processing|computer vision|devops|cloud computing|agile methodology|scrum|kanban|ci/cd|rest api|graphql|microservices|big data|data analytics)\b'
        ]
        
        technologies = set()
        for pattern in tech_patterns:
            matches = re.finditer(pattern, project_text, re.IGNORECASE)
            for match in matches:
                technologies.add(match.group(0).lower())
                
        return list(technologies)


    @classmethod
    def calculate_project_skill_score(cls, resume_text, jd_text):
        """Combines rule-based + semantic project matching."""
        resume_projects = cls.extract_section(resume_text, cls.SECTION_KEYWORDS)
        jd_responsibilities = extract_section_advanced(jd_text, ["responsibilities", "key responsibilities", "duties", "what you'll do", "role", "position", "you will"])

        if not resume_projects:
            print("\n--- PROJECT MATCHING ---")
            print("Could not find Projects section.")
            print("-" * 30)
            return 0.0, {}
            
        if not jd_responsibilities:
            print("\n--- PROJECT MATCHING ---")
            print("Could not find Responsibilities section in JD.")
            print("-" * 30)
            return 0.0, {}

        # Extract technologies from projects
        project_technologies = cls.extract_technologies_from_projects(resume_projects)
        
        # Rule-based score - match project descriptions with JD requirements
        rb_score, rb_matches = cls._rule_based_match(resume_projects, jd_responsibilities)

        # Semantic score
        sem_score, sem_matches = cls._semantic_match(resume_projects, jd_responsibilities)

        # Additional scoring based on technology matching
        jd_technologies = cls.extract_technologies_from_projects(jd_responsibilities)
        tech_match_score = 0
        if jd_technologies and project_technologies:
            matched_tech = set(project_technologies) & set(jd_technologies)
            tech_match_score = (len(matched_tech) / len(jd_technologies)) * 100 if jd_technologies else 0
        elif project_technologies:
            # If no technologies in JD, give partial credit for having technologies in projects
            tech_match_score = 30

        # If technologies match but content doesn't, boost the score
        if tech_match_score > 50 and rb_score < 30:
            rb_score = min(rb_score + 20, 100)

        # Weighted combination: 40% rule-based, 30% semantic, 30% technology match
        final_score = 0.4 * rb_score + 0.3 * sem_score + 0.3 * tech_match_score

        print("\n--- PROJECT MATCHING ---")
        print(f"Rule-based Score: {rb_score:.2f}%")
        print(f"Semantic Score: {sem_score:.2f}%")
        print(f"Technology Match Score: {tech_match_score:.2f}%")
        print(f"Technologies found in projects: {', '.join(project_technologies)}")
        if jd_technologies:
            print(f"Technologies required in JD: {', '.join(jd_technologies)}")
        print(f"Final Project Score: {final_score:.2f}%")
        print("-" * 30)

        details = {
            "score": final_score,
            "rule_based": rb_score,
            "semantic": sem_score,
            "tech_match": tech_match_score,
            "rule_matches": rb_matches,
            "semantic_matches": sem_matches,
            "project_technologies": project_technologies,
            "jd_technologies": jd_technologies
        }
        return round(final_score, 2), details