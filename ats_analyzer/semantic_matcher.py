from sentence_transformers import SentenceTransformer, util
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import re
from collections import Counter

# make sure punkt is available
nltk.download("punkt", quiet=True)
nltk.download('stopwords', quiet=True)

class SemanticMatcher:
    """
    Enhanced semantic matcher for personalized feedback using BERT.
    """

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.stop_words = set(nltk.corpus.stopwords.words('english'))

    def _semantic_score(self, text1, text2):
        """Compute cosine similarity between two texts."""
        emb1 = self.model.encode(text1, convert_to_tensor=True)
        emb2 = self.model.encode(text2, convert_to_tensor=True)
        return util.pytorch_cos_sim(emb1, emb2).item()

    def _clean_feedback_text(self, text):
        """Clean and format feedback text for better presentation."""
        if not text:
            return ""
        
        # Remove PDF artifacts and unwanted characters
        text = re.sub(r'\(cid:\d+\)', '', text)
        text = re.sub(r'[•▪➢➤]', '•', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Fix punctuation issues
        text = re.sub(r'\.\.+', '.', text)
        text = re.sub(r'\s+([.,!?])', r'\1', text)
        text = re.sub(r'([^.])(\.)([^.]|$)', r'\1\2 \3', text)
        
        # Remove email addresses and URLs
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'http\S+', '', text)
        
        # Split into sentences and clean each one
        sentences = re.split(r'(?<=[.!?])\s+', text)
        cleaned_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 5:
                sentence = sentence[0].upper() + sentence[1:] if sentence else sentence
                if not sentence.endswith(('.', '!', '?')):
                    sentence += '.'
                cleaned_sentences.append(sentence)
        
        cleaned_text = ' '.join(cleaned_sentences)
        return cleaned_text

    def generate_personalized_feedback(self, category, score, details, job_text):
        """
        Generate personalized feedback based on score.
        If score = 100: Focus on "What you did right"
        If score < 100: Focus on "AI-driven suggestions"
        """
        
        if score == 100:
            # Perfect score - focus on what they did right
            return self._generate_success_feedback(category, details)
        else:
            # Less than perfect - focus on improvements
            return self._generate_improvement_feedback(category, score, details, job_text)

    def _generate_success_feedback(self, category, details):
        """Generate 'What you did right' feedback for perfect scores."""
        
        if category == "skills":
            matched_count = len(details.get('matched_skills', []))
            return f"Perfect skills alignment! You successfully matched all {matched_count} key skills required for the role. Your technical expertise directly aligns with what employers are seeking."
            
        elif category == "experience":
            total_years = details.get('total_years', 0)
            return f"Excellent experience relevance! Your {total_years} years of professional experience perfectly match the role requirements. Your career progression demonstrates the exact background needed for this position."
            
        elif category == "projects":
            return "Outstanding project presentation! Your projects perfectly demonstrate the required skills and technologies. You've effectively showcased practical application of your technical abilities through real-world examples."
            
        elif category == "Quantifiable Achievements":
            achievements = details.get('achievements', [])
            return f"Exceptional use of quantifiable metrics! You have {len(achievements)} strong measurable achievements that clearly demonstrate your impact and results-driven approach."
            
        elif category == "education":
            return "Perfect educational alignment! Your degree level and field of study exactly match the job requirements. Your academic background provides the ideal foundation for this role."
            
        elif category == "keywords":
            return "Excellent keyword optimization! Your resume effectively incorporates relevant terminology from the job description, ensuring strong ATS compatibility and recruiter appeal."
            
        elif category == "formatting":
            return "Perfect formatting! Your resume follows all ATS-friendly guidelines with clear sections, professional structure, and proper formatting that ensures optimal parsing by applicant tracking systems."
            
        else:
            return f"Perfect {category} section! You've successfully met all requirements in this area."

    def _generate_improvement_feedback(self, category, score, details, job_text):
        """Generate AI-driven improvement suggestions for non-perfect scores."""
        
        if category == "skills":
            return self._generate_skills_improvements(score, details, job_text)
        elif category == "experience":
            return self._generate_experience_improvements(score, details, job_text)
        elif category == "projects":
            return self._generate_projects_improvements(score, details, job_text)
        elif category == "Quantifiable Achievements":
            return self._generate_achievements_improvements(score, details)
        elif category == "education":
            return self._generate_education_improvements(score, details)
        elif category == "keywords":
            return self._generate_keywords_improvements(score, details, job_text)
        elif category == "formatting":
            return self._generate_formatting_improvements(score, details)
        else:
            return f"Consider improving your {category} section to better match job requirements."

    def _generate_skills_improvements(self, score, details, job_text):
        """Generate skills-specific improvement suggestions."""
        matched_skills = list(details.get('matched_skills', []))
        missing_skills = list(details.get('missing_skills', []))
        
        suggestions = []
        
        if score >= 70:
            suggestions.append(f"Good skills foundation with {len(matched_skills)} matched skills.")
        else:
            suggestions.append("Skills alignment needs improvement.")
            
        if missing_skills:
            top_missing = missing_skills[:3]
            suggestions.append(f"Priority skills to add or highlight: {', '.join(top_missing)}.")
            
        if matched_skills:
            suggestions.append(f"Strengthen your existing skills: {', '.join(matched_skills[:3])}.")
            
        return " ".join(suggestions)

    def _generate_experience_improvements(self, score, details, job_text):
        """Generate experience-specific improvement suggestions."""
        suggestions = []
        
        total_years = details.get('total_years', 0)
        role_match_score = details.get('role_match_score', 0)
        
        if score >= 70:
            suggestions.append("Your experience shows good relevance.")
        else:
            suggestions.append("Experience section needs better alignment with job requirements.")
            
        if role_match_score < 70:
            suggestions.append("Tailor your role descriptions to better match the target position.")
            
        if total_years < 2:
            suggestions.append("Highlight any internships, volunteer work, or relevant coursework to strengthen your experience profile.")
            
        # Add semantic analysis
        resume_content = str(details.get('resume_text', ''))
        if resume_content and job_text:
            similarity = self._semantic_score(resume_content, job_text)
            if similarity < 0.5:
                suggestions.append("Incorporate more industry-specific terminology from the job description into your experience descriptions.")
                
        return " ".join(suggestions)

    def _generate_projects_improvements(self, score, details, job_text):
        """Generate projects-specific improvement suggestions."""
        suggestions = []
        
        if score >= 70:
            suggestions.append("Your projects demonstrate good technical skills.")
        else:
            suggestions.append("Project section needs enhancement to better showcase relevant skills.")
            
        skills_found = details.get('skills_found', [])
        skills_missing = details.get('skills_missing', [])
        
        if skills_missing:
            suggestions.append(f"Consider creating projects that demonstrate: {', '.join(skills_missing[:3])}.")
            
        if not skills_found:
            suggestions.append("Clearly describe the technologies and methodologies used in each project.")
            
        return " ".join(suggestions)

    def _generate_achievements_improvements(self, score, details):
        """Generate achievements-specific improvement suggestions."""
        achievements = details.get('achievements', [])
        num_achievements = len(achievements)
        
        if score >= 70:
            return f"Good progress with {num_achievements} quantifiable achievements. Add 2-3 more metrics to strengthen your impact statements."
        elif score >= 40:
            return f"You have some measurable results ({num_achievements}). Focus on adding percentages, dollar amounts, and timeframes to quantify your impact more clearly."
        else:
            return "Add quantifiable metrics to your resume. For each bullet point, ask: 'How much?', 'How many?', or 'What was the result?' Include specific numbers, percentages, and timeframes."

    def _generate_education_improvements(self, score, details):
        """Generate education-specific improvement suggestions."""
        suggestions = []
        
        resume_details = details.get('resume_details', {})
        jd_details = details.get('jd_details', {})
        
        if score >= 70:
            suggestions.append("Your educational background is well-aligned.")
        else:
            suggestions.append("Education section could better highlight relevant qualifications.")
            
        if resume_details.get('level', 0) < jd_details.get('level', 0):
            suggestions.append("Consider highlighting relevant coursework, certifications, or continuing education that bridges any degree level gaps.")
            
        required_fields = jd_details.get('fields', [])
        if required_fields:
            suggestions.append(f"Emphasize any coursework or projects related to: {', '.join(required_fields[:2])}.")
            
        return " ".join(suggestions)

    def _generate_keywords_improvements(self, score, details, job_text):
        """Generate keywords-specific improvement suggestions."""
        if score >= 70:
            return "Good keyword usage. Consider adding a few more industry-specific terms naturally throughout your resume."
        else:
            density = details.get('density', 0)
            return f"Improve keyword optimization by incorporating more terms from the job description. Current density: {density:.1f} keywords per 100 words. Target: 2-3 keywords per 100 words."

    def _generate_formatting_improvements(self, score, details):
        """Generate formatting-specific improvement suggestions."""
        suggestions = []
        
        if score >= 80:
            suggestions.append("Good formatting overall.")
        else:
            suggestions.append("Formatting needs improvement for better ATS compatibility.")
            
        if details.get('pronoun_count', 0) > 0:
            suggestions.append("Remove first-person pronouns (I, my, me) and start bullet points with action verbs.")
            
        if details.get('spelling_score', 0) < 100:
            suggestions.append("Proofread carefully for spelling and grammar errors.")
            
        if details.get('structure_score', 0) < 80:
            suggestions.append("Ensure all standard sections (Summary, Experience, Education, Skills) are clearly labeled and present.")
            
        return " ".join(suggestions)