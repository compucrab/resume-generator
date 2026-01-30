import streamlit as st
import yaml
import os
import subprocess
import re


class EnhancedResumeNLP:
    ACTION_VERBS = {
        "leadership": [
            "Led",
            "Directed",
            "Managed",
            "Supervised",
            "Coordinated",
            "Orchestrated",
            "Spearheaded",
            "Mentored",
            "Guided",
            "Facilitated",
        ],
        "technical": [
            "Developed",
            "Engineered",
            "Programmed",
            "Designed",
            "Architected",
            "Built",
            "Implemented",
            "Coded",
            "Debugged",
            "Optimized",
        ],
        "analytical": [
            "Analyzed",
            "Evaluated",
            "Assessed",
            "Investigated",
            "Researched",
            "Examined",
            "Audited",
            "Measured",
            "Calculated",
            "Forecasted",
        ],
        "creative": [
            "Designed",
            "Created",
            "Conceptualized",
            "Innovated",
            "Invented",
            "Crafted",
            "Produced",
            "Authored",
            "Illustrated",
            "Composed",
        ],
        "improvement": [
            "Improved",
            "Enhanced",
            "Optimized",
            "Streamlined",
            "Upgraded",
            "Revamped",
            "Transformed",
            "Modernized",
            "Automated",
            "Refined",
        ],
        "achievement": [
            "Achieved",
            "Accomplished",
            "Delivered",
            "Exceeded",
            "Surpassed",
            "Attained",
            "Completed",
            "Earned",
            "Won",
            "Secured",
        ],
    }

    # Common weak words to avoid
    WEAK_WORDS = [
        "responsible for",
        "duties included",
        "worked on",
        "helped with",
        "assisted with",
        "participated in",
        "involved in",
        "was part of",
    ]

    # Keywords for different industries
    INDUSTRY_KEYWORDS = {
        "software": [
            "agile",
            "scrum",
            "CI/CD",
            "microservices",
            "API",
            "cloud",
            "testing",
            "deployment",
            "DevOps",
            "git",
            "docker",
            "kubernetes",
        ],
        "data": [
            "machine learning",
            "data analysis",
            "SQL",
            "Python",
            "statistics",
            "visualization",
            "ETL",
            "big data",
            "ML models",
            "algorithms",
        ],
        "product": [
            "roadmap",
            "stakeholders",
            "user research",
            "product strategy",
            "metrics",
            "A/B testing",
            "KPIs",
            "market analysis",
            "user stories",
        ],
        "marketing": [
            "campaigns",
            "ROI",
            "analytics",
            "SEO",
            "content strategy",
            "social media",
            "conversion",
            "engagement",
            "branding",
            "growth",
        ],
    }

    @staticmethod
    def suggest_action_verb(text, category="technical"):
        """Suggest an appropriate action verb based on context"""
        if not text:
            return None

        words = text.lower().split()
        first_word = words[0] if words else ""

        # Check if starts with action verb
        all_verbs = [
            v for verbs in EnhancedResumeNLP.ACTION_VERBS.values() for v in verbs
        ]
        if first_word.capitalize() in all_verbs:
            return None

        # Suggest a verb from the category
        return EnhancedResumeNLP.ACTION_VERBS.get(
            category, EnhancedResumeNLP.ACTION_VERBS["technical"]
        )[0]

    @staticmethod
    def detect_weak_language(text):
        """Detect weak language in resume text"""
        if not text:
            return []

        text_lower = text.lower()
        found_weak = []

        for weak in EnhancedResumeNLP.WEAK_WORDS:
            if weak in text_lower:
                found_weak.append(weak)

        return found_weak

    @staticmethod
    def suggest_improvements(text):
        """Suggest improvements for resume text"""
        suggestions = []

        if not text:
            return suggestions

        # Check for weak language
        weak_words = EnhancedResumeNLP.detect_weak_language(text)
        if weak_words:
            suggestions.append(f"Avoid passive phrases: {', '.join(weak_words)}")

        # Check for quantification
        has_numbers = bool(re.search(r"\d+", text))
        if not has_numbers:
            suggestions.append("Add metrics or numbers to quantify your impact")

        # Check length
        if len(text.split()) < 5:
            suggestions.append("Provide more detail about your achievements")
        elif len(text.split()) > 30:
            suggestions.append("Consider making this more concise")

        # Check for action verb
        words = text.split()
        if words:
            first_word = words[0]
            all_verbs = [
                v for verbs in EnhancedResumeNLP.ACTION_VERBS.values() for v in verbs
            ]
            if first_word not in all_verbs:
                suggestions.append(f"Start with an action verb (e.g., {all_verbs[0]})")

        return suggestions

    @staticmethod
    def extract_skills_from_text(text):
        """Extract potential skills from text"""
        if not text:
            return []

        text_lower = text.lower()
        found_skills = []

        # Check for industry keywords
        for industry, keywords in EnhancedResumeNLP.INDUSTRY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_skills.append(keyword)

        return list(set(found_skills))

    @staticmethod
    def format_bullet_points(text):
        """Format text into bullet points"""
        if not text:
            return []

        # Split by newlines or common delimiters
        points = [p.strip() for p in text.split("\n") if p.strip()]
        return points

    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone):
        """Validate phone number"""
        clean_phone = re.sub(r"[\s\-\(\)]", "", phone)
        return len(clean_phone) >= 10

    @staticmethod
    def analyze_resume_strength(resume_data):
        """Analyze overall resume strength"""
        score = 0
        feedback = []

        # Check completeness (max 40 points)
        if resume_data.get("name"):
            score += 5
        if resume_data.get("email"):
            score += 5
        if resume_data.get("summary"):
            score += 10
        else:
            feedback.append("Add a professional summary")

        if resume_data.get("education"):
            score += 10
        else:
            feedback.append("Add education information")

        if resume_data.get("experience"):
            score += 10
        else:
            feedback.append("Add work experience")

        # Check content quality (max 30 points)
        total_highlights = 0
        if resume_data.get("experience"):
            for exp in resume_data["experience"]:
                highlights = exp.get("highlights", "")
                if highlights:
                    total_highlights += len(highlights.split("\n"))

        if total_highlights >= 5:
            score += 15
        elif total_highlights > 0:
            score += 10
            feedback.append("Add more achievements in your experience")
        else:
            feedback.append("Add specific achievements and responsibilities")

        # Check for quantified achievements (max 15 points)
        all_text = str(resume_data)
        numbers_count = len(re.findall(r"\d+%|\d+x|\$\d+|\d+ [a-zA-Z]+", all_text))
        if numbers_count >= 3:
            score += 15
        elif numbers_count > 0:
            score += 10
            feedback.append("Add more quantified achievements (numbers, percentages)")
        else:
            feedback.append("Include metrics to quantify your impact")

        # Check for skills (max 15 points)
        if resume_data.get("skills"):
            num_skills = sum(
                len(s.get("items", "").split(",")) for s in resume_data["skills"]
            )
            if num_skills >= 8:
                score += 15
            elif num_skills >= 4:
                score += 10
            else:
                feedback.append("Add more relevant skills")
        else:
            feedback.append("Add a skills section")

        return score, feedback


def create_rendercv_yaml(data):
    """Create RenderCV compatible YAML structure"""

    cv_data = {
        "cv": {
            "name": data["name"],
            "label": data.get("label", ""),
            "location": data.get("location", ""),
            "email": data["email"],
            "phone": data.get("phone", ""),
            "website": data.get("website", ""),
            "social_networks": [],
            "summary": data.get("summary", ""),
            "sections": {},
        },
        "design": {
            "theme": data.get("theme", "classic"),
            "color": data.get("color", "blue"),
            "page_size": "a4paper",
        },
    }

    # Add social networks
    if data.get("linkedin"):
        cv_data["cv"]["social_networks"].append(
            {"network": "LinkedIn", "username": data["linkedin"]}
        )
    if data.get("github"):
        cv_data["cv"]["social_networks"].append(
            {"network": "GitHub", "username": data["github"]}
        )

    # Add Education
    if data.get("education"):
        cv_data["cv"]["sections"]["Education"] = []
        for edu in data["education"]:
            edu_entry = {
                "institution": edu["institution"],
                "area": edu["degree"],
                "degree": edu.get("field", ""),
                "start_date": edu.get("start_date", ""),
                "end_date": edu.get("end_date", ""),
                "highlights": EnhancedResumeNLP.format_bullet_points(
                    edu.get("highlights", "")
                ),
            }
            if edu.get("gpa"):
                edu_entry["gpa"] = edu["gpa"]
            cv_data["cv"]["sections"]["Education"].append(edu_entry)

    # Add Experience
    if data.get("experience"):
        cv_data["cv"]["sections"]["Experience"] = []
        for exp in data["experience"]:
            exp_entry = {
                "company": exp["company"],
                "position": exp["position"],
                "location": exp.get("location", ""),
                "start_date": exp.get("start_date", ""),
                "end_date": exp.get("end_date", "Present"),
                "highlights": EnhancedResumeNLP.format_bullet_points(
                    exp.get("highlights", "")
                ),
            }
            cv_data["cv"]["sections"]["Experience"].append(exp_entry)

    # Add Projects
    if data.get("projects"):
        cv_data["cv"]["sections"]["Projects"] = []
        for proj in data["projects"]:
            proj_entry = {
                "name": proj["name"],
                "date": proj.get("date", ""),
                "highlights": EnhancedResumeNLP.format_bullet_points(
                    proj.get("description", "")
                ),
            }
            if proj.get("url"):
                proj_entry["url"] = proj["url"]
            cv_data["cv"]["sections"]["Projects"].append(proj_entry)

    # Add Skills
    if data.get("skills"):
        cv_data["cv"]["sections"]["Skills"] = []
        for skill_cat in data["skills"]:
            cv_data["cv"]["sections"]["Skills"].append(
                {"label": skill_cat["category"], "details": skill_cat["items"]}
            )

    # Add Custom Sections
    if data.get("custom_sections"):
        for section in data["custom_sections"]:
            cv_data["cv"]["sections"][section["title"]] = section["content"]

    return cv_data


def generate_resume(yaml_data, output_name="resume"):
    """Generate PDF resume using RenderCV"""

    yaml_file = f"{output_name}.yaml"
    with open(yaml_file, "w") as f:
        yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)

    try:
        result = subprocess.run(
            ["rendercv", "render", yaml_file],
            capture_output=True,
            text=True,
            cwd="/home/claude",
        )

        pdf_path = f"/home/claude/rendercv_output/{output_name}/{output_name}.pdf"
        if os.path.exists(pdf_path):
            return pdf_path, None
        else:
            return None, f"PDF generation failed: {result.stderr}"

    except Exception as e:
        return None, str(e)


def init_session_state():
    if "education_count" not in st.session_state:
        st.session_state.education_count = 1
    if "experience_count" not in st.session_state:
        st.session_state.experience_count = 1
    if "project_count" not in st.session_state:
        st.session_state.project_count = 1
    if "skill_categories" not in st.session_state:
        st.session_state.skill_categories = ["Technical Skills"]
    if "show_ai_suggestions" not in st.session_state:
        st.session_state.show_ai_suggestions = True


def main():
    st.set_page_config(
        page_title="AI Resume Generator Pro", page_icon="📄", layout="wide"
    )

    init_session_state()

    st.title("🤖 AI-Powered Resume Generator Pro")
    st.markdown(
        "Create professional resumes with AI-enhanced content and real-time suggestions"
    )

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

        theme = st.selectbox(
            "Resume Theme",
            ["classic", "moderncv", "engineeringresumes", "sb2nov"],
            help="Choose your resume style",
        )
        color = st.selectbox(
            "Color Scheme",
            ["blue", "black", "green", "red", "purple"],
            help="Select accent color",
        )

        st.markdown("---")

        st.session_state.show_ai_suggestions = st.checkbox(
            "Show AI Suggestions",
            value=True,
            help="Enable real-time AI suggestions for content improvement",
        )

        st.markdown("---")
        st.markdown("### 💡 Pro Tips")
        st.info(
            """
        **Action Verbs:**
        - Leadership: Led, Managed, Coordinated
        - Technical: Developed, Engineered, Built
        - Achievement: Delivered, Exceeded, Achieved
        
        **Quantify Impact:**
        - Use percentages (40% improvement)
        - Include numbers (team of 5)
        - Show scale ($2M budget)
        """
        )

    # Main form
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "📋 Personal Info",
            "🎓 Education",
            "💼 Experience",
            "🚀 Projects & Skills",
            "🎨 Custom Sections",
            "📊 Resume Analysis",
        ]
    )

    resume_data = {}

    # Tab 1: Personal Information
    with tab1:
        st.header("Personal Information")

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name *", placeholder="John Doe")
            email = st.text_input("Email *", placeholder="john.doe@example.com")
            phone = st.text_input("Phone", placeholder="+1-234-567-8900")
            location = st.text_input("Location", placeholder="New York, NY")

        with col2:
            label = st.text_input("Professional Title", placeholder="Software Engineer")
            website = st.text_input("Website", placeholder="https://johndoe.com")
            linkedin = st.text_input("LinkedIn Username", placeholder="johndoe")
            github = st.text_input("GitHub Username", placeholder="johndoe")

        summary = st.text_area(
            "Professional Summary",
            placeholder="Write a brief professional summary highlighting your key skills and achievements...",
            height=150,
            help="2-3 sentences about your expertise, experience, and what you bring to the role",
        )

        # AI Suggestions for Summary
        if st.session_state.show_ai_suggestions and summary:
            suggestions = EnhancedResumeNLP.suggest_improvements(summary)
            if suggestions:
                st.info(
                    "💡 **AI Suggestions:**\n"
                    + "\n".join(f"- {s}" for s in suggestions)
                )

        # Validation
        if email and not EnhancedResumeNLP.validate_email(email):
            st.warning("⚠️ Please enter a valid email address")
        if phone and not EnhancedResumeNLP.validate_phone(phone):
            st.warning("⚠️ Please enter a valid phone number")

        resume_data.update(
            {
                "name": name,
                "email": email,
                "phone": phone,
                "location": location,
                "label": label,
                "website": website,
                "linkedin": linkedin,
                "github": github,
                "summary": summary,
                "theme": theme,
                "color": color,
            }
        )

    # Tab 2: Education (similar structure with AI suggestions)
    with tab2:
        st.header("Education")

        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("➕ Add Education"):
                st.session_state.education_count += 1

        education_list = []
        for i in range(st.session_state.education_count):
            with st.expander(f"Education #{i+1}", expanded=(i == 0)):
                col1, col2 = st.columns(2)

                with col1:
                    institution = st.text_input(
                        "Institution *",
                        key=f"edu_inst_{i}",
                        placeholder="University Name",
                    )
                    degree = st.text_input(
                        "Degree *",
                        key=f"edu_degree_{i}",
                        placeholder="Bachelor of Science",
                    )
                    field = st.text_input(
                        "Field of Study",
                        key=f"edu_field_{i}",
                        placeholder="Computer Science",
                    )

                with col2:
                    start_date = st.text_input(
                        "Start Date", key=f"edu_start_{i}", placeholder="2018-09"
                    )
                    end_date = st.text_input(
                        "End Date", key=f"edu_end_{i}", placeholder="2022-05"
                    )
                    gpa = st.text_input(
                        "GPA (optional)", key=f"edu_gpa_{i}", placeholder="3.8/4.0"
                    )

                highlights = st.text_area(
                    "Achievements/Highlights (one per line)",
                    key=f"edu_highlights_{i}",
                    placeholder="Graduated with Honors\nRelevant coursework: Data Structures, Algorithms",
                    height=100,
                )

                if institution and degree:
                    education_list.append(
                        {
                            "institution": institution,
                            "degree": degree,
                            "field": field,
                            "start_date": start_date,
                            "end_date": end_date,
                            "gpa": gpa,
                            "highlights": highlights,
                        }
                    )

        resume_data["education"] = education_list

    # Tab 3: Experience with AI suggestions
    with tab3:
        st.header("Work Experience")

        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("➕ Add Experience"):
                st.session_state.experience_count += 1

        experience_list = []
        for i in range(st.session_state.experience_count):
            with st.expander(f"Experience #{i+1}", expanded=(i == 0)):
                col1, col2 = st.columns(2)

                with col1:
                    company = st.text_input(
                        "Company *",
                        key=f"exp_company_{i}",
                        placeholder="Tech Company Inc.",
                    )
                    position = st.text_input(
                        "Position *",
                        key=f"exp_position_{i}",
                        placeholder="Software Engineer",
                    )
                    location = st.text_input(
                        "Location",
                        key=f"exp_location_{i}",
                        placeholder="San Francisco, CA",
                    )

                with col2:
                    start_date = st.text_input(
                        "Start Date", key=f"exp_start_{i}", placeholder="2022-06"
                    )
                    end_date = st.text_input(
                        "End Date", key=f"exp_end_{i}", placeholder="Present"
                    )

                highlights = st.text_area(
                    "Key Achievements & Responsibilities (one per line)",
                    key=f"exp_highlights_{i}",
                    placeholder="Developed and deployed microservices using Python and Docker\nImproved system performance by 40% through optimization",
                    height=150,
                )

                # AI Suggestions for Experience
                if st.session_state.show_ai_suggestions and highlights:
                    weak_words = EnhancedResumeNLP.detect_weak_language(highlights)
                    if weak_words:
                        st.warning(f"⚠️ Avoid passive language: {', '.join(weak_words)}")

                    # Check for quantification
                    if not re.search(r"\d+", highlights):
                        st.info(
                            "💡 Tip: Add numbers or metrics to quantify your impact"
                        )

                    # Suggest action verbs
                    bullet_points = highlights.split("\n")
                    for bullet in bullet_points[:2]:  # Check first 2 bullets
                        suggestions = EnhancedResumeNLP.suggest_improvements(bullet)
                        if suggestions:
                            st.info(f"💡 For '{bullet[:30]}...': " + suggestions[0])

                if company and position:
                    experience_list.append(
                        {
                            "company": company,
                            "position": position,
                            "location": location,
                            "start_date": start_date,
                            "end_date": end_date,
                            "highlights": highlights,
                        }
                    )

        resume_data["experience"] = experience_list

    # Tab 4: Projects & Skills
    with tab4:
        col_proj, col_skill = st.columns(2)

        with col_proj:
            st.header("Projects")

            if st.button("➕ Add Project"):
                st.session_state.project_count += 1

            project_list = []
            for i in range(st.session_state.project_count):
                with st.expander(f"Project #{i+1}", expanded=(i == 0)):
                    proj_name = st.text_input(
                        "Project Name *",
                        key=f"proj_name_{i}",
                        placeholder="E-commerce Platform",
                    )
                    proj_date = st.text_input(
                        "Date", key=f"proj_date_{i}", placeholder="2023"
                    )
                    proj_url = st.text_input(
                        "Project URL (optional)",
                        key=f"proj_url_{i}",
                        placeholder="https://github.com/...",
                    )
                    proj_desc = st.text_area(
                        "Description (one per line)",
                        key=f"proj_desc_{i}",
                        placeholder="Built full-stack web application using React and Node.js\nImplemented user authentication and payment processing",
                        height=100,
                    )

                    if proj_name:
                        project_list.append(
                            {
                                "name": proj_name,
                                "date": proj_date,
                                "url": proj_url,
                                "description": proj_desc,
                            }
                        )

            resume_data["projects"] = project_list

        with col_skill:
            st.header("Skills")

            if st.button("➕ Add Skill Category"):
                st.session_state.skill_categories.append(
                    f"Category {len(st.session_state.skill_categories) + 1}"
                )

            skills_list = []
            for i, category in enumerate(st.session_state.skill_categories):
                with st.expander(f"Skill Category #{i+1}", expanded=(i == 0)):
                    cat_name = st.text_input(
                        "Category Name",
                        value=category,
                        key=f"skill_cat_{i}",
                        placeholder="Programming Languages",
                    )
                    cat_items = st.text_input(
                        "Skills (comma-separated)",
                        key=f"skill_items_{i}",
                        placeholder="Python, Java, JavaScript, C++",
                    )

                    if cat_name and cat_items:
                        skills_list.append({"category": cat_name, "items": cat_items})

            resume_data["skills"] = skills_list

    # Tab 5: Custom Sections
    with tab5:
        st.header("Custom Sections")
        st.info(
            "Add additional sections like Certifications, Awards, Publications, etc."
        )

        num_custom = st.number_input(
            "Number of custom sections", min_value=0, max_value=5, value=0
        )

        custom_sections = []
        for i in range(num_custom):
            with st.expander(f"Custom Section #{i+1}"):
                section_title = st.text_input(
                    "Section Title",
                    key=f"custom_title_{i}",
                    placeholder="Certifications",
                )
                section_content = st.text_area(
                    "Content",
                    key=f"custom_content_{i}",
                    placeholder="AWS Certified Solutions Architect\nGoogle Cloud Professional",
                    height=100,
                )

                if section_title and section_content:
                    custom_sections.append(
                        {
                            "title": section_title,
                            "content": EnhancedResumeNLP.format_bullet_points(
                                section_content
                            ),
                        }
                    )

        resume_data["custom_sections"] = custom_sections

    # Tab 6: Resume Analysis
    with tab6:
        st.header("📊 Resume Strength Analysis")

        if st.button("🔍 Analyze Resume", type="primary"):
            score, feedback = EnhancedResumeNLP.analyze_resume_strength(resume_data)

            # Display score
            col1, col2, col3 = st.columns([2, 1, 2])

            with col2:
                st.metric("Resume Score", f"{score}/100")

            # Determine rating
            if score >= 80:
                rating = "Excellent 🌟"
                color = "green"
            elif score >= 60:
                rating = "Good 👍"
                color = "blue"
            elif score >= 40:
                rating = "Fair 📝"
                color = "orange"
            else:
                rating = "Needs Work 🔧"
                color = "red"

            st.markdown(f"### Rating: :{color}[{rating}]")

            # Progress bar
            st.progress(score / 100)

            # Display feedback
            if feedback:
                st.markdown("### 💡 Recommendations")
                for item in feedback:
                    st.markdown(f"- {item}")
            else:
                st.success("✅ Your resume looks great!")

            # Additional insights
            st.markdown("### 📈 Detailed Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Completeness:**")
                completeness_items = [
                    ("Name", bool(resume_data.get("name"))),
                    ("Email", bool(resume_data.get("email"))),
                    ("Summary", bool(resume_data.get("summary"))),
                    ("Education", bool(resume_data.get("education"))),
                    ("Experience", bool(resume_data.get("experience"))),
                    ("Skills", bool(resume_data.get("skills"))),
                ]
                for item, present in completeness_items:
                    icon = "✅" if present else "❌"
                    st.markdown(f"{icon} {item}")

            with col2:
                st.markdown("**Content Quality:**")
                # Count quantified achievements
                all_text = str(resume_data)
                numbers = len(re.findall(r"\d+%|\d+x|\$\d+|\d+ [a-zA-Z]+", all_text))
                st.markdown(f"📊 Quantified achievements: {numbers}")

                # Count total skills
                if resume_data.get("skills"):
                    total_skills = sum(
                        len(s.get("items", "").split(","))
                        for s in resume_data["skills"]
                    )
                    st.markdown(f"🎯 Skills listed: {total_skills}")

                # Count experience entries
                exp_count = len(resume_data.get("experience", []))
                st.markdown(f"💼 Work experiences: {exp_count}")

    # Generate Resume Button
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 2])

    with col2:
        generate_button = st.button(
            "🎯 Generate Resume", type="primary", use_container_width=True
        )

    if generate_button:
        if not resume_data.get("name"):
            st.error("❌ Please enter your name")
        elif not resume_data.get("email"):
            st.error("❌ Please enter your email")
        else:
            with st.spinner("🔄 Generating your professional resume..."):
                yaml_data = create_rendercv_yaml(resume_data)
                pdf_path, error = generate_resume(yaml_data, "my_resume")

                if pdf_path:
                    st.success("✅ Resume generated successfully!")

                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="📥 Download Resume (PDF)",
                            data=f,
                            file_name=f"{resume_data['name'].replace(' ', '_')}_Resume.pdf",
                            mime="application/pdf",
                        )

                    with st.expander("📄 View YAML Configuration"):
                        st.code(
                            yaml.dump(yaml_data, default_flow_style=False),
                            language="yaml",
                        )
                else:
                    st.error(f"❌ Error generating resume: {error}")
                    st.info("Make sure RenderCV is installed: `pip install rendercv`")


if __name__ == "__main__":
    main()
