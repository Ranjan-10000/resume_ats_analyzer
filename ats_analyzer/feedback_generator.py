# class FeedbackGenerator:
#     """
#     Generates a comprehensive feedback report based on the analysis details.
#     """

#     @classmethod
#     def _generate_skill_feedback(cls, details):
#         """Generates feedback for the skill matching section."""
#         score = details['score']
#         matched_skills = details['matched_skills']
#         missing_skills = details['missing_skills']

#         good = []
#         improve = []

#         if score >= 80:
#             good.append(f"Excellent skill alignment! You have matched with {len(matched_skills)} key skills required for the role.")
#         elif score >= 50:
#             good.append(f"Good skill alignment. You matched with several key skills: {', '.join(sorted(list(matched_skills))[:3])}...")
        
#         if missing_skills:
#             improve.append(f"Consider adding or highlighting these skills from the job description: {', '.join(sorted(list(missing_skills)))}.")
        
#         if not good and not improve:
#             improve.append("No skills were matched. Review the job description and tailor your resume's skill section accordingly.")

#         return good, improve

#     @classmethod
#     def _generate_experience_feedback(cls, details):
#         """Generates feedback for the experience section."""
#         score = (details.get('role_match_score', 0) * 0.60) + (details.get('experience_duration_score', 0) * 0.40)
#         role_match_score = details.get('role_match_score', 0)
#         total_years = details.get('total_years', 0)
#         jd_title = details.get('jd_title', 'the target role')

#         good = []
#         improve = []

#         if role_match_score > 80:
#             good.append(f"Your previous roles align very well with the target role of '{jd_title}'.")
        
#         if total_years > 0:
#             good.append(f"You have demonstrated {total_years} years of professional experience.")
        
#         if role_match_score < 70:
#             improve.append(f"Tailor your job titles or descriptions to better align with the target role of '{jd_title}'.")
        
#         if total_years < 1 and score < 100:
#              improve.append("If you have more experience (including internships or volunteer work), make sure it's clearly listed with dates.")

#         if not good and not improve:
#             improve.append("Could not parse work experience. Ensure your roles are clearly listed with start and end dates.")

#         return good, improve

#     @classmethod
#     def _generate_project_feedback(cls, details):
#         """Generates feedback for the project skill usage section."""
#         skills_found = details.get('skills_found', [])
#         skills_missing = details.get('skills_missing', [])

#         good = []
#         improve = []

#         if skills_found:
#             good.append(f"Great job showcasing your skills! Your projects demonstrate the use of: {', '.join(sorted(skills_found))}.")
        
#         if skills_missing:
#             improve.append(f"To strengthen your profile, consider starting a small project that uses these skills: {', '.join(sorted(skills_missing))}.")
        
#         if not good and not improve:
#             improve.append("No matched skills were found in your project descriptions. Ensure your projects clearly state the technologies used.")

#         return good, improve

#     @classmethod
#     def _generate_achievement_feedback(cls, details):
#         """Generates feedback for quantifiable achievements."""
#         if isinstance(details, dict):
#             achievements = details.get('achievements', [])
#         else:
#             achievements = details

#         num_achievements = len(achievements)

#         good = []
#         improve = []

#         if num_achievements > 0:
#             good.append(f"Excellent work including {num_achievements} quantifiable results. This shows your impact.")
#             if achievements:
#                 good.append(f"Highlighting metrics like '{achievements[0]}' is very effective.")
        
#         if num_achievements < 3:
#             improve.append("Strengthen your resume by adding more metrics. For each bullet point, ask yourself: 'How much?', 'How many?', or 'What was the result?'")
        
#         return good, improve

#     @classmethod
#     def _generate_education_feedback(cls, details):
#         """Generates feedback for the education section."""
#         # --- THE FIX: Use .get() with default values to prevent KeyErrors ---
#         resume_details = details.get('resume_details', {})
#         jd_details = details.get('jd_details', {})
#         field_score = details.get('field_score', 0)

#         level_score = 50.0 if resume_details.get('level', 0) >= jd_details.get('level', 0) else 0.0
#         gpa_score = 20.0 if resume_details.get('gpa', 0) >= 7.5 else 0.0
#         score = level_score + gpa_score + field_score

#         good = []
#         improve = []

#         if score == 100:
#             good.append("Your educational background is a perfect match for the requirements.")
        
#         if resume_details.get('level', 0) >= jd_details.get('level', 0):
#             good.append(f"Your degree level meets the job requirements.")
#         else:
#             improve.append("The job requires a different degree level than what is listed on your resume.")

#         if field_score > 0:
#              good.append(f"Your field of study, '{resume_details.get('field', 'N/A')}', aligns with the job's preferred majors.")
#         else:
#             improve.append(f"Your field of study does not appear to match the required fields: {', '.join(jd_details.get('fields', []))}. If your coursework is relevant, consider highlighting that.")

#         return good, improve

#     @classmethod
#     def _generate_keyword_feedback(cls, details):
#         """Generates feedback for keyword optimization."""
#         score = details.get('score', 0)
#         density = details.get('density', 0)
#         found_keywords = details.get('found_keywords', {})

#         good = []
#         improve = []

#         if score >= 75:
#             good.append("Your resume is well-optimized with relevant keywords from the job description.")
#             if found_keywords:
#                 top_keyword = max(found_keywords, key=found_keywords.get)
#                 good.append(f"Effectively used terms like '{top_keyword}'.")

#         if score < 75:
#             improve.append("Integrate more keywords from the job description naturally into your summary and experience bullet points.")
#             improve.append(f"Your current keyword density is {density:.2f} per 100 words; aiming for 2 or more is ideal.")

#         return good, improve

#     @classmethod
#     def _generate_formatting_feedback(cls, details):
#         """Generates feedback for formatting compliance."""
#         score = details.get('score', 0)
        
#         good = []
#         improve = []

#         if score == 100:
#             good.append("Your resume format is professional, clear, and ATS-friendly.")
        
#         if details.get('structure_score', 0) > 80:
#             good.append("Includes all standard sections (Summary, Experience, Education, Skills).")
#         else:
#             improve.append("Your resume may be missing standard sections like 'Summary' or 'Skills'. Ensure all key sections are clearly titled.")

#         if details.get('correctness_score', 0) < 100:
#             if details.get('pronoun_count', 0) > 0:
#                 improve.append("Avoid using first-person pronouns (I, my, me). Start bullet points with strong action verbs instead.")
#             if details.get('spelling_score', 0) < 100:
#                  improve.append("Proofread carefully for spelling errors to maintain professionalism.")

#         return good, improve

#     @classmethod
#     def generate_feedback(cls, all_details):
#         """
#         The main method to generate a complete feedback report.
#         """
#         feedback_sections = {
#             "Skill Matching": cls._generate_skill_feedback(all_details['skills']),
#             "Experience Relevance": cls._generate_experience_feedback(all_details['experience']),
#             "Skill Usage in Projects": cls._generate_project_feedback(all_details['projects']),
#             "Quantifiable Achievements": cls._generate_achievement_feedback(all_details['achievements']),
#             "Education Alignment": cls._generate_education_feedback(all_details['education']),
#             "Keyword Optimization": cls._generate_keyword_feedback(all_details['keywords']),
#             "Formatting Compliance": cls._generate_formatting_feedback(all_details['formatting']),
#         }

#         report = "\n" + "="*50
#         report += "\n" + " " * 15 + "DETAILED FEEDBACK REPORT"
#         report += "\n" + "="*50

#         for section_name, (good_points, improve_points) in feedback_sections.items():
#             report += f"\n\n--- {section_name.upper()} ---\n"
            
#             if good_points:
#                 report += "\n✅ What you did well:\n"
#                 for point in good_points:
#                     report += f"   - {point}\n"
            
#             if improve_points:
#                 report += "\n💡 What you can improve:\n"
#                 for point in improve_points:
#                     report += f"   - {point}\n"
        
#         report += "\n" + "="*50
#         return report


# # feedback_generator.py
# class FeedbackGenerator:
#     """
#     Generates a comprehensive feedback report based on the analysis details.
#     """

#     @classmethod
#     def _generate_skill_feedback(cls, details):
#         """Generates feedback for the skill matching section."""
#         score = details['score']
#         matched_skills = details['matched_skills']
#         missing_skills = details['missing_skills']

#         good = []
#         improve = []

#         if score >= 80:
#             good.append(f"Excellent skill alignment! You have matched with {len(matched_skills)} key skills required for the role.")
#         elif score >= 50:
#             good.append(f"Good skill alignment. You matched with several key skills: {', '.join(sorted(list(matched_skills))[:3])}...")
        
#         if missing_skills:
#             improve.append(f"Consider adding or highlighting these skills from the job description: {', '.join(sorted(list(missing_skills)))}.")
        
#         if not good and not improve:
#             improve.append("No skills were matched. Review the job description and tailor your resume's skill section accordingly.")

#         return good, improve

#     @classmethod
#     def _generate_experience_feedback(cls, details):
#         """Generates feedback for the experience section."""
#         score = details.get('final_score', 0)
#         role_match_score = details.get('role_match_score', 0)
#         total_years = details.get('total_years', 0)
#         jd_title = details.get('jd_title', 'the target role')

#         good = []
#         improve = []

#         if role_match_score > 80:
#             good.append(f"Your previous roles align very well with the target role of '{jd_title}'.")
        
#         if total_years > 0:
#             good.append(f"You have demonstrated {total_years} years of professional experience.")
        
#         if role_match_score < 70:
#             improve.append(f"Tailor your job titles or descriptions to better align with the target role of '{jd_title}'.")
        
#         if total_years < 1 and score < 100:
#              improve.append("If you have more experience (including internships or volunteer work), make sure it's clearly listed with dates.")

#         if not good and not improve:
#             improve.append("Could not parse work experience. Ensure your roles are clearly listed with start and end dates.")

#         return good, improve

#     @classmethod
#     def _generate_project_feedback(cls, details):
#         """Generates feedback for the project skill usage section."""
#         skills_found = details.get('skills_found', [])
#         skills_missing = details.get('skills_missing', [])

#         good = []
#         improve = []

#         if skills_found:
#             good.append(f"Great job showcasing your skills! Your projects demonstrate the use of: {', '.join(sorted(skills_found))}.")
        
#         if skills_missing:
#             improve.append(f"To strengthen your profile, consider starting a small project that uses these skills: {', '.join(sorted(skills_missing))}.")
        
#         if not good and not improve:
#             improve.append("No matched skills were found in your project descriptions. Ensure your projects clearly state the technologies used.")

#         return good, improve

#     @classmethod
#     def _generate_achievement_feedback(cls, details):
#         """Generates feedback for quantifiable achievements."""
#         if isinstance(details, dict):
#             achievements = details.get('achievements', [])
#         else:
#             achievements = details

#         num_achievements = len(achievements)

#         good = []
#         improve = []

#         if num_achievements > 0:
#             good.append(f"Excellent work including {num_achievements} quantifiable results. This shows your impact.")
#             if achievements:
#                 good.append(f"Highlighting metrics like '{achievements[0]}' is very effective.")
        
#         if num_achievements < 3:
#             improve.append("Strengthen your resume by adding more metrics. For each bullet point, ask yourself: 'How much?', 'How many?', or 'What was the result?'")
        
#         return good, improve

#     @classmethod
#     def _generate_education_feedback(cls, details):
#         """Generates feedback for the education section."""
#         # Use .get() with default values to prevent KeyErrors
#         resume_details = details.get('resume_details', {})
#         jd_details = details.get('jd_details', {})
#         field_score = details.get('field_score', 0)

#         level_score = 50.0 if resume_details.get('level', 0) >= jd_details.get('level', 0) else 0.0
#         gpa_score = 20.0 if resume_details.get('gpa', 0) >= 7.5 else 0.0
#         score = level_score + gpa_score + field_score

#         good = []
#         improve = []

#         if score == 100:
#             good.append("Your educational background is a perfect match for the requirements.")
        
#         if resume_details.get('level', 0) >= jd_details.get('level', 0):
#             good.append(f"Your degree level meets the job requirements.")
#         else:
#             improve.append("The job requires a different degree level than what is listed on your resume.")

#         if field_score > 0:
#              good.append(f"Your field of study, '{resume_details.get('field', 'N/A')}', aligns with the job's preferred majors.")
#         else:
#             improve.append(f"Your field of study does not appear to match the required fields: {', '.join(jd_details.get('fields', []))}. If your coursework is relevant, consider highlighting that.")

#         return good, improve

#     @classmethod
#     def _generate_keyword_feedback(cls, details):
#         """Generates feedback for keyword optimization."""
#         score = details.get('score', 0)
#         density = details.get('density', 0)
#         found_keywords = details.get('resume_keywords_found_counts', {})

#         good = []
#         improve = []

#         if score >= 75:
#             good.append("Your resume is well-optimized with relevant keywords from the job description.")
#             if found_keywords:
#                 top_keyword = max(found_keywords, key=found_keywords.get, default="N/A")
#                 good.append(f"Effectively used terms like '{top_keyword}'.")

#         if score < 75:
#             improve.append("Integrate more keywords from the job description naturally into your summary and experience bullet points.")
#             improve.append(f"Your current keyword density is {density:.2f} per 100 words; aiming for 2 or more is ideal.")

#         return good, improve

#     @classmethod
#     def _generate_formatting_feedback(cls, details):
#         """Generates feedback for formatting compliance."""
#         score = details.get('score', 0)
        
#         good = []
#         improve = []

#         if score == 100:
#             good.append("Your resume format is professional, clear, and ATS-friendly.")
        
#         if details.get('structure_score', 0) > 80:
#             good.append("Includes all standard sections (Summary, Experience, Education, Skills).")
#         else:
#             improve.append("Your resume may be missing standard sections like 'Summary' or 'Skills'. Ensure all key sections are clearly titled.")

#         if details.get('correctness_score', 0) < 100:
#             if details.get('pronoun_count', 0) > 0:
#                 improve.append("Avoid using first-person pronouns (I, my, me). Start bullet points with strong action verbs instead.")
#             if details.get('spelling_score', 0) < 100:
#                  improve.append("Proofread carefully for spelling errors to maintain professionalism.")

#         return good, improve

#     @classmethod
#     def generate_feedback(cls, all_details):
#         """
#         The main method to generate a complete feedback report.
#         """
#         feedback_sections = {
#             "Skill Matching": cls._generate_skill_feedback(all_details['skills']),
#             "Experience Relevance": cls._generate_experience_feedback(all_details['experience']),
#             "Skill Usage in Projects": cls._generate_project_feedback(all_details['projects']),
#             "Quantifiable Achievements": cls._generate_achievement_feedback(all_details['achievements']),
#             "Education Alignment": cls._generate_education_feedback(all_details['education']),
#             "Keyword Optimization": cls._generate_keyword_feedback(all_details['keywords']),
#             "Formatting Compliance": cls._generate_formatting_feedback(all_details['formatting']),
#         }

#         report = "\n" + "="*50
#         report += "\n" + " " * 15 + "DETAILED FEEDBACK REPORT"
#         report += "\n" + "="*50

#         for section_name, (good_points, improve_points) in feedback_sections.items():
#             report += f"\n\n--- {section_name.upper()} ---\n"
            
#             if good_points:
#                 report += "\n✅ What you did well:\n"
#                 for point in good_points:
#                     report += f"   - {point}\n"
            
#             if improve_points:
#                 report += "\n💡 What you can improve:\n"
#                 for point in improve_points:
#                     report += f"   - {point}\n"
        
#         report += "\n" + "="*50
#         return report




# from ats_analyzer.semantic_matcher import SemanticMatcher

# class FeedbackGenerator:
#     semantic = SemanticMatcher()

#     @staticmethod
#     def generate_feedback(all_details, job_text):
#         feedback = "\n\n==================================================\n"
#         feedback += "               PERSONALIZED FEEDBACK REPORT\n"
#         feedback += "==================================================\n"

#         for section, details in all_details.items():
#             section_name = section.upper()
#             rule_score = details.get("score", 0)
#             resume_text = details.get("details", "")

#             # Call SemanticMatcher
#             result = FeedbackGenerator.semantic.get_feedback(
#                 section_name, resume_text, job_text, rule_score
#             )

#             feedback += f"\n--- {section_name} ---\n"
#             if result["strengths"]:
#                 feedback += "✅ Strengths:\n"
#                 for s in result["strengths"]:
#                     feedback += f"   - {s}\n"

#             if result["improvements"]:
#                 feedback += "\n💡 Improvements:\n"
#                 for i in result["improvements"]:
#                     feedback += f"   - {i}\n"

#             feedback += f"\n📊 Rule-based Score: {result['rule_score']:.2f}%"
#             feedback += f"\n🤖 BERT Semantic Score: {result['bert_score']:.2f}%"
#             feedback += f"\n🎯 Final Weighted Score: {result['final_score']:.2f}%\n"

#         return feedback





# from ats_analyzer.semantic_matcher import SemanticMatcher

# class FeedbackGenerator:
#     """Generates personalized feedback reports with BERT-enhanced suggestions."""

#     def __init__(self):
#         self.semantic_matcher = SemanticMatcher()

#     @classmethod
#     def generate_feedback(cls, all_details, job_text):
#         """Generate feedback report for all categories with semantic enhancements."""
#         semantic_matcher = SemanticMatcher()
#         report = []
        
#         for category, details in all_details.items():
#             if isinstance(details, dict) and "score" in details:
#                 # Get semantic-enhanced feedback
#                 semantic_feedback = semantic_matcher.generate_personalized_feedback(
#                     category.lower(), details['score'], details, job_text
#                 )
                
#                 report.append({
#                     "category": category,
#                     "score": details['score'],
#                     "semantic_feedback": semantic_feedback,
#                     "details": details
#                 })
        
#         return report

#     @staticmethod
#     def print_report(report):
#         """Nicely formatted feedback for console output."""
#         print("\n" + "="*50)
#         print("         🎯 PERSONALIZED FEEDBACK REPORT")
#         print("="*50)

#         for entry in report:
#             print(f"\n--- {entry['category'].upper()} ---")
#             print(f"📊 Score: {entry['score']:.2f}%")
#             print(f"💡 AI Suggestions: {entry['semantic_feedback']}")
#             print("-" * 30)



from ats_analyzer.semantic_matcher import SemanticMatcher

class FeedbackGenerator:
    """Generates personalized feedback reports with BERT-enhanced suggestions."""

    @staticmethod
    def generate_feedback(all_details, job_text):
        """Generate feedback report for all categories with semantic enhancements."""
        semantic_matcher = SemanticMatcher()
        report = []
        
        # Map category names to match the semantic matcher templates
        category_mapping = {
            "Skill Matching": "skills",
            "Experience Relevance": "experience", 
            "Skill Usage in Projects": "projects",
            "Quantifiable Achievements": "Quantifiable Achievements",
            "Education Alignment": "education",
            "Keyword Optimization": "keywords",
            "Formatting Compliance": "formatting"
        }
        
        for category, details in all_details.items():
            if isinstance(details, dict) and "score" in details:
                # Map the category name to the semantic matcher format
                mapped_category = category_mapping.get(category, category.lower())
                
                # Get semantic-enhanced feedback based on score
                if details['score'] == 100:
                    # Perfect score - show what they did right
                    feedback_type = "success"
                    semantic_feedback = semantic_matcher._generate_success_feedback(mapped_category, details)
                else:
                    # Less than perfect - show improvements
                    feedback_type = "improvement"
                    semantic_feedback = semantic_matcher._generate_improvement_feedback(
                        mapped_category, details['score'], details, job_text
                    )
                
                # Prepare additional details for display
                display_details = FeedbackGenerator._prepare_display_details(category, details)
                
                report.append({
                    "category": category,
                    "score": details['score'],
                    "feedback_type": feedback_type,  # Add this to distinguish in template
                    "semantic_feedback": semantic_feedback,
                    "details": display_details
                })
        
        return report

    @staticmethod
    def _prepare_display_details(category, details):
        """Prepare details for proper display in the template."""
        display_details = details.copy()
        
        # Ensure all required fields exist with default values
        if category == "Skill Matching":
            display_details.setdefault('matched_skills', [])
            display_details.setdefault('missing_skills', [])
            
        elif category == "Experience Relevance":
            display_details.setdefault('total_years', 0)
            display_details.setdefault('role_match_score', 0)
            display_details.setdefault('jd_title', 'the target role')
            # Ensure experience details are properly formatted
            if 'resume_text' not in display_details and 'details' in display_details:
                display_details['resume_text'] = display_details['details']
                
        elif category == "Skill Usage in Projects":
            display_details.setdefault('skills_found', [])
            display_details.setdefault('skills_missing', [])
            display_details.setdefault('project_technologies', [])
            
        elif category == "Quantifiable Achievements":
            # Ensure achievements is always a list
            if isinstance(details.get('achievements'), list):
                display_details['achievements'] = details['achievements']
            else:
                display_details['achievements'] = []
                
        elif category == "Education Alignment":
            display_details.setdefault('resume_details', {})
            display_details.setdefault('jd_details', {})
            display_details.setdefault('field_score', 0)
            
        elif category == "Keyword Optimization":
            display_details.setdefault('found_keywords', {})
            display_details.setdefault('resume_keywords_found_counts', {})
            display_details.setdefault('density', 0)
            
        elif category == "Formatting Compliance":
            display_details.setdefault('structure_score', 0)
            display_details.setdefault('correctness_score', 0)
            display_details.setdefault('pronoun_count', 0)
            display_details.setdefault('spelling_score', 0)
        
        return display_details

    @staticmethod
    def print_report(report):
        """Nicely formatted feedback for console output."""
        print("\n" + "="*50)
        print("         🎯 PERSONALIZED FEEDBACK REPORT")
        print("="*50)

        for entry in report:
            print(f"\n--- {entry['category'].upper()} ---")
            print(f"📊 Score: {entry['score']:.2f}%")
            
            if entry['feedback_type'] == 'success':
                print(f"✅ What You Did Right: {entry['semantic_feedback']}")
            else:
                print(f"💡 AI Suggestions: {entry['semantic_feedback']}")
            print("-" * 30)