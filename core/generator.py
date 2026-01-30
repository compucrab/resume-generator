import yaml
import subprocess
import os
from datetime import datetime

class Generator:
    @staticmethod
    def create_rendercv_yaml(data):
        """Maps saved session data to the exact RenderCV YAML schema."""
        cv_data = {
            "cv": {
                "name": data.get("name", "Applicant"),
                "email": data.get("email", ""),
                "location": data.get("location", ""),
                "phone": data.get("phone", ""),
                "social_networks": [],
                "sections": {}
            },
            "design": {"theme": "classic"}
        }

        # Education
        if "education" in data and data["education"]:
            cv_data["cv"]["sections"]["education"] = [
                {
                    "institution": edu["institution"],
                    "area": edu["degree"],
                    "degree": edu.get("field", ""),
                    "start_date": edu["start_date"],
                    "end_date": edu["end_date"],
                    "highlights": edu["highlights"].split("\n") if edu["highlights"] else []
                } for edu in data["education"]
            ]

        # Experience
        if "experience" in data and data["experience"]:
            cv_data["cv"]["sections"]["experience"] = [
                {
                    "company": exp["company"],
                    "position": exp["position"],
                    "start_date": exp["start_date"],
                    "end_date": exp["end_date"],
                    "highlights": exp["highlights"].split("\n") if exp["highlights"] else []
                } for exp in data["experience"]
            ]

        # Custom Sections (Certifications, Skills, etc.)
        if "custom_sections" in data:
            for section in data["custom_sections"]:
                if section["title"] and section["content"]:
                    cv_data["cv"]["sections"][section["title"]] = section["content"].strip().split("\n")

        return cv_data

    @staticmethod
    def generate_pdf(data):
        """Writes YAML and triggers RenderCV CLI."""
        yaml_content = Generator.create_rendercv_yaml(data)
        
        # Use a fixed name or timestamp for the input file
        input_yaml = "input.yaml"
        output_name = f"Resume_{datetime.now().strftime('%H%M%S')}"
        
        with open(input_yaml, "w") as f:
            yaml.dump(yaml_content, f, sort_keys=False)

        try:
            # Trigger RenderCV command line
            # rendercv render input.yaml
            subprocess.run(["rendercv", "render", input_yaml], check=True)
            
            # RenderCV outputs to: rendercv_output/Name_Classic_Theme.pdf
            # We look for any PDF in the output folder
            output_folder = "rendercv_output"
            if os.path.exists(output_folder):
                files = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.endswith(".pdf")]
                if files:
                    # Return the path to the newest/only PDF found
                    return files[0], None
            
            return None, "PDF generation finished but file not found."
            
        except subprocess.CalledProcessError as e:
            return None, f"RenderCV CLI Error: {e}"
        except Exception as e:
            return None, str(e)