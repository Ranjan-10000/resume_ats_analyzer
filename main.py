# from ats_analyzer.pdf_processor import PDFProcessor
# from ats_analyzer.skill_matcher import SkillMatcher
# from ats_analyzer.experience_matcher import ExperienceMatcher
# from ats_analyzer.project_matcher import ProjectMatcher
# from ats_analyzer.quantifiable_checker import QuantifiableChecker
# from ats_analyzer.education_checker import EducationChecker
# from ats_analyzer.keyword_checker import KeywordChecker
# from ats_analyzer.formatting_checker import FormattingChecker
# from ats_analyzer.feedback_generator import FeedbackGenerator

# def main():
#     """
#     Main function to run the complete ATS analysis pipeline.
#     """
#     # --- 1. SETUP ---
#     # resume_file_path = r"C:\Users\ranja\Downloads\Resume_TPBIT-BTECH10041231755238290.pdf"
#     resume_file_path = r"C:\Users\ranja\OneDrive\Desktop\GEET RESUME.pdf"
#     jd_file_path = r"C:\Users\ranja\Downloads\Technical_Role_JD.pdf"

#     # --- 2. TEXT EXTRACTION & NORMALIZATION ---
#     resume_processor = PDFProcessor(resume_file_path)
#     resume_text = resume_processor.extract_text()
#     resume_text_normalized = resume_processor.normalize_text()

#     job_processor = PDFProcessor(jd_file_path)
#     job_text = job_processor.extract_text()
#     job_text_normalized = job_processor.normalize_text()

#     if not resume_text or not job_text:
#         print("Could not read one or both of the PDF files. Exiting.")
#         return

#     # --- 3. RUN ALL ANALYSIS MODULES ---
#     skill_score, skill_details = SkillMatcher.calculate_score(resume_text_normalized, job_text_normalized)
#     experience_score, experience_details = ExperienceMatcher.calculate_experience_score(resume_text, job_text)
#     project_score, project_details = ProjectMatcher.calculate_project_skill_score(resume_text, skill_details["matched_skills"])
#     achievement_score, achievement_details = QuantifiableChecker.calculate_achievement_score(resume_text)
#     education_score, education_details = EducationChecker.calculate_education_score(resume_text, job_text)
#     keyword_score, keyword_details = KeywordChecker.calculate_keyword_score(resume_text, job_text)
#     formatting_score, formatting_details = FormattingChecker.calculate_formatting_score(resume_text)

#     # --- 4. CALCULATE FINAL WEIGHTED ATS SCORE ---
#     weights = {
#         "skills": 0.40,
#         "experience": 0.20,
#         "projects": 0.10,
#         "achievements": 0.10,
#         "education": 0.05,
#         "keywords": 0.05,
#         "formatting": 0.10, # Increased to 10% as per final structure
#     }

#     final_score = (
#         skill_score * weights["skills"] +
#         experience_score * weights["experience"] +
#         project_score * weights["projects"] +
#         achievement_score * weights["achievements"] +
#         education_score * weights["education"] +
#         keyword_score * weights["keywords"] +
#         formatting_score * weights["formatting"]
#     )

#     # --- 5. DISPLAY SCORE SUMMARY ---
#     print("\n" + "="*50)
#     print(" " * 15 + "ATS SCORE SUMMARY")
#     print("="*50)
#     print(f"{'Category':<30} | {'Score':<15}")
#     print("-" * 50)
#     print(f"{'1. Skill Matching':<30} | {skill_score:.2f} / 100.00")
#     print(f"{'2. Experience Relevance':<30} | {experience_score:.2f} / 100.00")
#     print(f"{'3. Skill Usage in Projects':<30} | {project_score:.2f} / 100.00")
#     print(f"{'4. Quantifiable Achievements':<30} | {achievement_score:.2f} / 100.00")
#     print(f"{'5. Education Alignment':<30} | {education_score:.2f} / 100.00")
#     print(f"{'6. Keyword Optimization':<30} | {keyword_score:.2f} / 100.00")
#     print(f"{'7. Formatting Compliance':<30} | {formatting_score:.2f} / 100.00")
#     print("-" * 50)
#     print(f"{'FINAL WEIGHTED ATS SCORE':<30} | {final_score:.2f} / 100.00")
#     print("="*50)

#     # --- 6. GATHER ALL DETAILS FOR FEEDBACK ---
#     all_details = {
#         "skills": skill_details,
#         "experience": experience_details,
#         "projects": project_details,
#         "achievements": achievement_details,
#         "education": education_details,
#         "keywords": keyword_details,
#         "formatting": formatting_details
#     }

#     # --- 7. GENERATE AND DISPLAY FEEDBACK ---
#     feedback_report = FeedbackGenerator.generate_feedback(all_details)
#     print(feedback_report)


# if __name__ == "__main__":
#     main()



# from ats_analyzer.pdf_processor import PDFProcessor
# from ats_analyzer.skill_matcher import SkillMatcher
# from ats_analyzer.experience_matcher import ExperienceMatcher
# from ats_analyzer.project_matcher import ProjectMatcher
# from ats_analyzer.quantifiable_checker import QuantifiableChecker
# from ats_analyzer.education_checker import EducationChecker
# from ats_analyzer.keyword_checker import KeywordChecker
# from ats_analyzer.formatting_checker import FormattingChecker
# from ats_analyzer.feedback_generator import FeedbackGenerator


# def main():
#     """
#     Main function to run the complete ATS analysis pipeline with
#     both rule-based scoring and BERT-powered personalized feedback.
#     """
#     # --- 1. SETUP ---
#     resume_file_path = r"C:\Users\ranja\OneDrive\Desktop\GEET RESUME.pdf"
#     jd_file_path = r"C:\Users\ranja\Downloads\Technical_Role_JD.pdf"

#     # --- 2. TEXT EXTRACTION ---
#     resume_processor = PDFProcessor(resume_file_path)
#     resume_text = resume_processor.extract_text()
#     resume_text_normalized = resume_processor.normalize_text()

#     job_processor = PDFProcessor(jd_file_path)
#     job_text = job_processor.extract_text()
#     job_text_normalized = job_processor.normalize_text()

#     if not resume_text or not job_text:
#         print("Could not read one or both of the PDF files. Exiting.")
#         return

#     # --- 3. RUN ALL ANALYSIS MODULES (Rule-based) ---
#     skill_score, skill_details = SkillMatcher.calculate_score(resume_text_normalized, job_text_normalized)
#     experience_score, experience_details = ExperienceMatcher.calculate_experience_score(resume_text, job_text)
#     project_score, project_details = ProjectMatcher.calculate_project_skill_score(resume_text, skill_details["matched_skills"])
#     achievement_score, achievement_details = QuantifiableChecker.calculate_achievement_score(resume_text)
#     education_score, education_details = EducationChecker.calculate_education_score(resume_text, job_text)
#     keyword_score, keyword_details = KeywordChecker.calculate_keyword_score(resume_text, job_text)
#     formatting_score, formatting_details = FormattingChecker.calculate_formatting_score(resume_text)

#     # --- 4. CALCULATE FINAL RULE-BASED ATS SCORE ---
#     weights = {
#         "skills": 0.40,
#         "experience": 0.20,
#         "projects": 0.10,
#         "achievements": 0.10,
#         "education": 0.05,
#         "keywords": 0.05,
#         "formatting": 0.10,
#     }

#     final_score = (
#         skill_score * weights["skills"] +
#         experience_score * weights["experience"] +
#         project_score * weights["projects"] +
#         achievement_score * weights["achievements"] +
#         education_score * weights["education"] +
#         keyword_score * weights["keywords"] +
#         formatting_score * weights["formatting"]
#     )

#     # --- 5. DISPLAY SCORE SUMMARY ---
#     print("\n" + "="*50)
#     print(" " * 15 + "ATS SCORE SUMMARY")
#     print("="*50)
#     print(f"{'Category':<30} | {'Score':<15}")
#     print("-" * 50)
#     print(f"{'1. Skill Matching':<30} | {skill_score:.2f} / 100.00")
#     print(f"{'2. Experience Relevance':<30} | {experience_score:.2f} / 100.00")
#     print(f"{'3. Skill Usage in Projects':<30} | {project_score:.2f} / 100.00")
#     print(f"{'4. Quantifiable Achievements':<30} | {achievement_score:.2f} / 100.00")
#     print(f"{'5. Education Alignment':<30} | {education_score:.2f} / 100.00")
#     print(f"{'6. Keyword Optimization':<30} | {keyword_score:.2f} / 100.00")
#     print(f"{'7. Formatting Compliance':<30} | {formatting_score:.2f} / 100.00")
#     print("-" * 50)
#     print(f"{'FINAL WEIGHTED ATS SCORE':<30} | {final_score:.2f} / 100.00")
#     print("="*50)

#     # --- 6. GATHER ALL DETAILS FOR FEEDBACK ---
#     all_details = {
#         "skills": {**skill_details, "score": skill_score},
#         "experience": {**experience_details, "score": experience_score},
#         "projects": {**project_details, "score": project_score},
#         "achievements": {"details": achievement_details, "score": achievement_score},  # fixed
#         "education": {**education_details, "score": education_score},
#         "keywords": {**keyword_details, "score": keyword_score},
#         "formatting": {**formatting_details, "score": formatting_score}
#     }

#     # --- 7. GENERATE AND DISPLAY FEEDBACK (with BERT) ---
#     feedback_report = FeedbackGenerator.generate_feedback(all_details, job_text_normalized)
#     print(feedback_report)


# if __name__ == "__main__":
#     main()




# from ats_analyzer.pdf_processor import PDFProcessor
# from ats_analyzer.skill_matcher import SkillMatcher
# from ats_analyzer.experience_matcher import ExperienceMatcher
# from ats_analyzer.project_matcher import ProjectMatcher
# from ats_analyzer.quantifiable_checker import QuantifiableChecker
# from ats_analyzer.education_checker import EducationChecker
# from ats_analyzer.keyword_checker import KeywordChecker
# from ats_analyzer.formatting_checker import FormattingChecker
# from ats_analyzer.feedback_generator import FeedbackGenerator


# def main():
#     """
#     Main function to run the complete ATS analysis pipeline.
#     """
#     # --- 1. SETUP ---
#     # resume_file_path = r"C:\Users\ranja\Downloads\Resume_TPBIT-BTECH10041231755238290.pdf"
#     resume_file_path = r"C:\Users\ranja\OneDrive\Desktop\GEET RESUME.pdf"
#     jd_file_path = r"C:\Users\ranja\Downloads\Technical_Role_JD.pdf"

#     # --- 2. TEXT EXTRACTION & NORMALIZATION ---
#     resume_processor = PDFProcessor(resume_file_path)
#     resume_text = resume_processor.extract_text()
#     resume_text_normalized = resume_processor.normalize_text()

#     job_processor = PDFProcessor(jd_file_path)
#     job_text = job_processor.extract_text()
#     job_text_normalized = job_processor.normalize_text()

#     if not resume_text or not job_text:
#         print("❌ Could not read one or both of the PDF files. Exiting.")
#         return

#     # --- 3. RUN ALL ANALYSIS MODULES ---
#     skill_score, skill_details = SkillMatcher.calculate_score(resume_text_normalized, job_text_normalized)
#     experience_score, experience_details = ExperienceMatcher.calculate_experience_score(resume_text, job_text)
#     project_score, project_details = ProjectMatcher.calculate_project_skill_score(
#         resume_text, job_text
#     )
    
#     achievement_score, achievement_details = QuantifiableChecker.calculate_achievement_score(resume_text)
#     education_score, education_details = EducationChecker.calculate_education_score(resume_text, job_text)
#     keyword_score, keyword_details = KeywordChecker.calculate_keyword_score(resume_text, job_text)
#     formatting_score, formatting_details = FormattingChecker.calculate_formatting_score(resume_text)

#     # --- 4. CALCULATE FINAL WEIGHTED ATS SCORE ---
#     weights = {
#         "skills": 0.40,
#         "experience": 0.20,
#         "projects": 0.10,
#         "achievements": 0.10,
#         "education": 0.05,
#         "keywords": 0.05,
#         "formatting": 0.10,  # Increased to 10% as per final structure
#     }

#     final_score = (
#         skill_score * weights["skills"]
#         + experience_score * weights["experience"]
#         + project_score * weights["projects"]
#         + achievement_score * weights["achievements"]
#         + education_score * weights["education"]
#         + keyword_score * weights["keywords"]
#         + formatting_score * weights["formatting"]
#     )

#     # --- 5. DISPLAY SCORE SUMMARY ---
#     print("\n" + "=" * 50)
#     print(" " * 15 + "📊 ATS SCORE SUMMARY")
#     print("=" * 50)
#     print(f"{'Category':<30} | {'Score':<15}")
#     print("-" * 50)
#     print(f"{'1. Skill Matching':<30} | {skill_score:.2f} / 100.00")
#     print(f"{'2. Experience Relevance':<30} | {experience_score:.2f} / 100.00")
#     print(f"{'3. Skill Usage in Projects':<30} | {project_score:.2f} / 100.00")
#     print(f"{'4. Quantifiable Achievements':<30} | {achievement_score:.2f} / 100.00")
#     print(f"{'5. Education Alignment':<30} | {education_score:.2f} / 100.00")
#     print(f"{'6. Keyword Optimization':<30} | {keyword_score:.2f} / 100.00")
#     print(f"{'7. Formatting Compliance':<30} | {formatting_score:.2f} / 100.00")
#     print("-" * 50)
#     print(f"{'FINAL WEIGHTED ATS SCORE':<30} | {final_score:.2f} / 100.00")
#     print("=" * 50)

#     # --- 6. GATHER ALL DETAILS FOR FEEDBACK ---
#     all_details = {
#         "Skills": skill_details,
#         "Experience": experience_details,
#         "Projects": project_details,
#         "Achievements": achievement_details,
#         "Education": education_details,
#         "Keywords": keyword_details,
#         "Formatting": formatting_details,
#     }

#     # --- 7. GENERATE & DISPLAY FEEDBACK ---
#     feedback_report = FeedbackGenerator.generate_feedback(all_details)
#     FeedbackGenerator.print_report(feedback_report)


# if __name__ == "__main__":
#     main()







from ats_analyzer.pdf_processor import PDFProcessor
from ats_analyzer.skill_matcher import SkillMatcher
from ats_analyzer.experience_matcher import ExperienceMatcher
from ats_analyzer.project_matcher import ProjectMatcher
from ats_analyzer.quantifiable_checker import QuantifiableChecker
from ats_analyzer.education_checker import EducationChecker
from ats_analyzer.keyword_checker import KeywordChecker
from ats_analyzer.formatting_checker import FormattingChecker
from ats_analyzer.feedback_generator import FeedbackGenerator


def main():
    """
    Main function to run the complete ATS analysis pipeline.
    """
    # --- 1. SETUP ---
    # resume_file_path = r"C:\Users\ranja\Downloads\Resume_TPBIT-BTECH10041231755238290.pdf"
    resume_file_path = r"C:\Users\ranja\OneDrive\Desktop\GEET RESUME.pdf"
    jd_file_path = r"C:\Users\ranja\Downloads\Technical_Role_JD.pdf"

    # --- 2. TEXT EXTRACTION & NORMALIZATION ---
    resume_processor = PDFProcessor(resume_file_path)
    resume_text = resume_processor.extract_text()
    resume_text_normalized = resume_processor.normalize_text()

    job_processor = PDFProcessor(jd_file_path)
    job_text = job_processor.extract_text()
    job_text_normalized = job_processor.normalize_text()

    if not resume_text or not job_text:
        print("❌ Could not read one or both of the PDF files. Exiting.")
        return

    # --- 3. RUN ALL ANALYSIS MODULES ---
    skill_score, skill_details = SkillMatcher.calculate_score(resume_text_normalized, job_text_normalized)
    experience_score, experience_details = ExperienceMatcher.calculate_experience_score(resume_text, job_text)
    project_score, project_details = ProjectMatcher.calculate_project_skill_score(
        resume_text, job_text
    )
    
    achievement_score, achievement_details = QuantifiableChecker.calculate_achievement_score(resume_text)
    education_score, education_details = EducationChecker.calculate_education_score(resume_text, job_text)
    keyword_score, keyword_details = KeywordChecker.calculate_keyword_score(resume_text, job_text)
    formatting_score, formatting_details = FormattingChecker.calculate_formatting_score(resume_text)

    # --- 4. CALCULATE FINAL WEIGHTED ATS SCORE ---
    weights = {
        "skills": 0.40,
        "experience": 0.20,
        "projects": 0.10,
        "achievements": 0.10,
        "education": 0.05,
        "keywords": 0.05,
        "formatting": 0.10,  # Increased to 10% as per final structure
    }

    final_score = (
        skill_score * weights["skills"]
        + experience_score * weights["experience"]
        + project_score * weights["projects"]
        + achievement_score * weights["achievements"]
        + education_score * weights["education"]
        + keyword_score * weights["keywords"]
        + formatting_score * weights["formatting"]
    )

    # --- 5. DISPLAY SCORE SUMMARY ---
    print("\n" + "=" * 50)
    print(" " * 15 + "📊 ATS SCORE SUMMARY")
    print("=" * 50)
    print(f"{'Category':<30} | {'Score':<15}")
    print("-" * 50)
    print(f"{'1. Skill Matching':<30} | {skill_score:.2f} / 100.00")
    print(f"{'2. Experience Relevance':<30} | {experience_score:.2f} / 100.00")
    print(f"{'3. Skill Usage in Projects':<30} | {project_score:.2f} / 100.00")
    print(f"{'4. Quantifiable Achievements':<30} | {achievement_score:.2f} / 100.00")
    print(f"{'5. Education Alignment':<30} | {education_score:.2f} / 100.00")
    print(f"{'6. Keyword Optimization':<30} | {keyword_score:.2f} / 100.00")
    print(f"{'7. Formatting Compliance':<30} | {formatting_score:.2f} / 100.00")
    print("-" * 50)
    print(f"{'FINAL WEIGHTED ATS SCORE':<30} | {final_score:.2f} / 100.00")
    print("=" * 50)

    # --- 6. GATHER ALL DETAILS FOR FEEDBACK ---
    all_details = {
        "Skills": skill_details,
        "Experience": experience_details,
        "Projects": project_details,
        "Achievements": achievement_details,
        "Education": education_details,
        "Keywords": keyword_details,
        "Formatting": formatting_details,
    }

    # --- 7. GENERATE & DISPLAY FEEDBACK ---
    feedback_report = FeedbackGenerator.generate_feedback(all_details, job_text_normalized)
    FeedbackGenerator.print_report(feedback_report)


if __name__ == "__main__":
    main()