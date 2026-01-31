"""
Resume Suggestions Engine
Provides AI-powered suggestions to improve resume content based on best practices.
"""

import re
from typing import List, Tuple
from core.data import ACTION_VERBS, WEAK_WORDS, INDUSTRY_KEYWORDS


class SuggestionEngine:
    """Analyzes resume content and provides actionable improvement suggestions."""

    @staticmethod
    def analyze_personal_info(data: dict) -> str:
        """Generate suggestions for the Personal Info section."""
        suggestions = []

        # Summary Analysis
        summary = data.get("summary", "")
        if summary:
            summary_suggestions = SuggestionEngine._analyze_summary(summary)
            if summary_suggestions:
                suggestions.append("### 📝 Professional Summary")
                suggestions.extend([f"- {s}" for s in summary_suggestions])

        # Professional Title
        title = data.get("title", "")
        if title and len(title.split()) < 2:
            suggestions.append("### 💼 Professional Title")
            suggestions.append(
                "- Consider making your title more specific (e.g., 'Senior Software Engineer' instead of 'Engineer')"
            )

        if not suggestions:
            return """
### ✅ Personal Info looks great!

Your personal information section is well-structured. Here are some general tips:
- Keep your summary concise (2-3 sentences)
- Highlight your unique value proposition
- Include relevant keywords for your industry
"""

        return "\n\n".join(suggestions)

    @staticmethod
    def _analyze_summary(summary: str) -> List[str]:
        """Analyze professional summary and return suggestions."""
        suggestions = []

        words = summary.split()
        word_count = len(words)

        # Length check
        if word_count < 20:
            suggestions.append(
                "Your summary is quite brief. Aim for 30-60 words to showcase your value."
            )
        elif word_count > 80:
            suggestions.append(
                "Your summary is a bit long. Try to condense it to 30-60 words for better impact."
            )

        # Weak language detection
        weak_found = [w for w in WEAK_WORDS if w.lower() in summary.lower()]
        if weak_found:
            suggestions.append(
                f"Avoid passive phrases like: {', '.join(weak_found[:2])}. Use action-oriented language instead."
            )

        # Check for quantification
        if not re.search(r"\d+", summary):
            suggestions.append(
                "Add numbers or metrics to quantify your experience (e.g., '5+ years', '20% improvement')."
            )

        # First-person check
        first_person = ["I ", "my ", "me "]
        if any(fp in summary for fp in first_person):
            suggestions.append(
                "Write in third person or without pronouns (remove 'I', 'my', 'me')."
            )

        return suggestions

    @staticmethod
    def analyze_education(entries: List[dict]) -> str:
        """Generate suggestions for Education section."""
        if not entries:
            return "Add at least one education entry to strengthen your resume."

        suggestions = []

        for i, edu in enumerate(entries):
            highlights = edu.get("highlights", "").strip()
            gpa = edu.get("gpa", "").strip()

            entry_suggestions = []

            # GPA suggestion
            if not gpa:
                try:
                    # Check if it's a strong GPA worth mentioning
                    entry_suggestions.append("Consider adding GPA if it's 3.5 or above")
                except:
                    pass

            # Achievements suggestion
            if not highlights:
                entry_suggestions.append(
                    "Add relevant achievements, honors, or coursework"
                )
            elif len(highlights.split("\n")) < 2:
                entry_suggestions.append(
                    "Add more specific achievements (awards, projects, relevant coursework)"
                )

            if entry_suggestions:
                suggestions.append(
                    f"### 🎓 Education #{i+1}: {edu.get('degree', 'Entry')}"
                )
                suggestions.extend([f"- {s}" for s in entry_suggestions])

        if not suggestions:
            return "### ✅ Education section looks strong!\n\nYour education entries are well-detailed."

        return "\n\n".join(suggestions)

    @staticmethod
    def analyze_experience(entries: List[dict]) -> str:
        """Generate suggestions for Work Experience section."""
        if not entries:
            return "Add work experience to showcase your professional background."

        suggestions = []

        for i, exp in enumerate(entries):
            highlights = exp.get("highlights", "").strip()

            if not highlights:
                suggestions.append(
                    f"### 💼 Experience #{i+1}: {exp.get('position', 'Entry')}"
                )
                suggestions.append("- Add key achievements and responsibilities")
                continue

            entry_suggestions = SuggestionEngine._analyze_highlights(highlights)

            if entry_suggestions:
                suggestions.append(
                    f"### 💼 {exp.get('position', 'Position')} at {exp.get('company', 'Company')}"
                )
                suggestions.extend([f"- {s}" for s in entry_suggestions])

        if not suggestions:
            return "### ✅ Experience section is strong!\n\nYour work experience is well-documented with achievements."

        return "\n\n".join(suggestions)

    @staticmethod
    def _analyze_highlights(highlights: str) -> List[str]:
        """Analyze achievement highlights and return suggestions."""
        suggestions = []

        bullets = [b.strip() for b in highlights.split("\n") if b.strip()]

        # Check number of bullets
        if len(bullets) < 2:
            suggestions.append("Add more bullet points (aim for 3-5 key achievements)")
        elif len(bullets) > 6:
            suggestions.append("Consider condensing to 4-6 most impactful achievements")

        # Analyze each bullet
        bullets_without_action_verbs = 0
        bullets_without_numbers = 0
        bullets_with_weak_language = 0

        all_action_verbs = [v for verbs in ACTION_VERBS.values() for v in verbs]

        for bullet in bullets:
            words = bullet.split()
            if not words:
                continue

            # Check for action verb
            first_word = words[0].rstrip(".,;:")
            if first_word not in all_action_verbs:
                bullets_without_action_verbs += 1

            # Check for quantification
            if not re.search(r"\d+", bullet):
                bullets_without_numbers += 1

            # Check for weak language
            if any(weak in bullet.lower() for weak in WEAK_WORDS):
                bullets_with_weak_language += 1

        # Generate suggestions based on analysis
        if bullets_without_action_verbs > len(bullets) / 2:
            example_verbs = ", ".join(ACTION_VERBS["technical"][:3])
            suggestions.append(
                f"Start more bullets with strong action verbs (e.g., {example_verbs})"
            )

        if bullets_without_numbers > len(bullets) / 2:
            suggestions.append(
                "Add metrics and numbers to quantify your impact (e.g., 'Increased efficiency by 30%')"
            )

        if bullets_with_weak_language > 0:
            suggestions.append(
                "Remove passive phrases like 'responsible for' - be direct and action-oriented"
            )

        return suggestions

    @staticmethod
    def analyze_projects(entries: List[dict]) -> str:
        """Generate suggestions for Projects section."""
        if not entries:
            return "Projects are optional but can strengthen your resume, especially for technical roles."

        suggestions = []

        for i, proj in enumerate(entries):
            desc = proj.get("description", "").strip()
            url = proj.get("url", "").strip()

            entry_suggestions = []

            if not desc:
                entry_suggestions.append(
                    "Add a description of the project and your contributions"
                )
            elif len(desc.split()) < 10:
                entry_suggestions.append(
                    "Expand description to include technologies used and impact"
                )

            if not url:
                entry_suggestions.append(
                    "Add a URL if the project is publicly available (GitHub, live demo, etc.)"
                )

            # Check for technologies/skills
            if desc and not any(
                keyword in desc.lower()
                for keywords in INDUSTRY_KEYWORDS.values()
                for keyword in keywords
            ):
                entry_suggestions.append("Mention specific technologies or skills used")

            if entry_suggestions:
                suggestions.append(
                    f"### 🚀 Project #{i+1}: {proj.get('name', 'Entry')}"
                )
                suggestions.extend([f"- {s}" for s in entry_suggestions])

        if not suggestions:
            return "### ✅ Projects section looks great!\n\nYour projects are well-documented."

        return "\n\n".join(suggestions)

    @staticmethod
    def analyze_overall_resume(form_data: dict) -> Tuple[int, str]:
        """
        Analyze the complete resume and return a score (0-100) and detailed feedback.

        Returns:
            Tuple[int, str]: (score, formatted_feedback_markdown)
        """
        score = 0
        feedback_sections = []

        # Completeness Score (40 points)
        feedback_sections.append("## 📊 Resume Completeness")
        completeness_items = []

        if form_data.get("name") and form_data.get("email"):
            score += 10
            completeness_items.append("✅ Contact information present")
        else:
            completeness_items.append("❌ Missing contact information")

        if form_data.get("summary"):
            score += 10
            completeness_items.append("✅ Professional summary included")
        else:
            score += 0
            completeness_items.append("❌ Add a professional summary")

        if form_data.get("education"):
            score += 10
            completeness_items.append("✅ Education section filled")
        else:
            completeness_items.append("❌ Add education details")

        if form_data.get("experience"):
            score += 10
            completeness_items.append("✅ Work experience included")
        else:
            completeness_items.append("❌ Add work experience")

        feedback_sections.append("\n".join(completeness_items))

        # Content Quality Score (35 points)
        feedback_sections.append("\n## 💎 Content Quality")
        quality_items = []

        # Count achievement bullets
        total_bullets = 0
        if form_data.get("experience"):
            for exp in form_data["experience"]:
                highlights = exp.get("highlights", "")
                total_bullets += len([b for b in highlights.split("\n") if b.strip()])

        if total_bullets >= 6:
            score += 15
            quality_items.append(
                f"✅ Strong detail level ({total_bullets} achievement bullets)"
            )
        elif total_bullets >= 3:
            score += 10
            quality_items.append(
                f"⚠️ Good detail, consider adding more achievements ({total_bullets} bullets)"
            )
        else:
            quality_items.append(
                "❌ Add more specific achievements and responsibilities"
            )

        # Check for quantification
        all_text = str(form_data)
        numbers_count = len(re.findall(r"\d+%|\d+x|\$\d+|\d+\+", all_text))

        if numbers_count >= 5:
            score += 20
            quality_items.append(
                f"✅ Excellent use of metrics ({numbers_count} quantified achievements)"
            )
        elif numbers_count >= 2:
            score += 12
            quality_items.append(
                f"⚠️ Good metrics usage, add more numbers ({numbers_count} found)"
            )
        else:
            quality_items.append("❌ Add metrics and numbers to quantify your impact")

        feedback_sections.append("\n".join(quality_items))

        # Action Verbs & Language (25 points)
        feedback_sections.append("\n## 🎯 Language & Impact")
        language_items = []

        all_action_verbs = [v for verbs in ACTION_VERBS.values() for v in verbs]
        action_verb_count = sum(
            1 for verb in all_action_verbs if verb.lower() in all_text.lower()
        )

        if action_verb_count >= 5:
            score += 15
            language_items.append("✅ Strong use of action verbs")
        elif action_verb_count >= 2:
            score += 8
            language_items.append("⚠️ Add more action verbs to strengthen impact")
        else:
            language_items.append(
                "❌ Start bullets with action verbs (Led, Developed, Achieved, etc.)"
            )

        # Check for weak language
        weak_count = sum(1 for weak in WEAK_WORDS if weak.lower() in all_text.lower())
        if weak_count == 0:
            score += 10
            language_items.append("✅ No passive language detected")
        else:
            score += 5
            language_items.append(f"⚠️ Remove {weak_count} instances of passive phrases")

        feedback_sections.append("\n".join(language_items))

        # Overall Rating
        if score >= 85:
            rating = "🌟 **Excellent** - Your resume is strong and ready!"
        elif score >= 70:
            rating = "👍 **Good** - Minor improvements will make it great"
        elif score >= 50:
            rating = "⚠️ **Fair** - Needs some work to stand out"
        else:
            rating = "🔧 **Needs Improvement** - Focus on the suggestions below"

        header = (
            f"# Resume Strength Analysis\n\n## Overall Score: {score}/100\n{rating}\n\n"
        )

        return score, header + "\n".join(feedback_sections)

    @staticmethod
    def suggest_action_verbs(category: str = "technical") -> List[str]:
        """Return a list of action verbs for a specific category."""
        return ACTION_VERBS.get(category, ACTION_VERBS["technical"])

    @staticmethod
    def detect_industry(form_data: dict) -> str:
        """
        Detect the likely industry based on resume content.

        Returns:
            str: Industry name (software, data, product, marketing, or general)
        """
        all_text = str(form_data).lower()

        industry_scores = {}
        for industry, keywords in INDUSTRY_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword.lower() in all_text)
            industry_scores[industry] = score

        if not industry_scores or max(industry_scores.values()) == 0:
            return "general"

        return max(industry_scores.values())

    @staticmethod
    def get_industry_specific_tips(industry: str) -> str:
        """Return industry-specific resume tips."""
        tips = {
            "software": """
### 💻 Software Engineering Tips
- Highlight specific technologies and frameworks
- Include GitHub/portfolio links
- Mention agile/scrum experience
- Quantify code improvements (performance, efficiency)
- Showcase side projects and open source contributions
""",
            "data": """
### 📊 Data Science/Analytics Tips
- Emphasize statistical methods and ML algorithms
- Mention tools: Python, R, SQL, Tableau, etc.
- Quantify insights and business impact
- Include relevant publications or research
- Showcase data visualization skills
""",
            "product": """
### 🎯 Product Management Tips
- Focus on user impact and business metrics
- Highlight cross-functional collaboration
- Mention product launches and roadmap planning
- Include A/B testing and data-driven decisions
- Showcase stakeholder management skills
""",
            "marketing": """
### 📢 Marketing Tips
- Quantify campaign performance (ROI, conversion rates)
- Highlight multi-channel experience
- Mention analytics tools and metrics
- Showcase content creation and strategy
- Include growth and engagement metrics
""",
            "general": """
### 💡 General Resume Tips
- Use action verbs to start each bullet
- Quantify achievements with numbers
- Keep format clean and consistent
- Tailor content to job descriptions
- Proofread for errors
""",
        }

        return tips.get(industry, tips["general"])
