import json
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

current_dir = os.path.dirname(os.path.abspath(__file__))

def generate_resume(data_file, template_file, output_pdf):
    """
    Generates a PDF resume from a JSON data file and an HTML template.
    """
    try:
        # Load resume data from the JSON file
        with open(data_file, 'r', encoding='utf-8') as f:
            resume_data = json.load(f)

        # Set up the Jinja2 environment to load the HTML template
        env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.abspath(__file__))))
        template = env.get_template(template_file)

        # Render the HTML template with the resume data
        html_out = template.render(**resume_data)

        # Convert the rendered HTML to a PDF using WeasyPrint
        HTML(string=html_out, base_url=current_dir).write_pdf(output_pdf)

        print(f"✅ Resume generated successfully at {output_pdf}")

    except FileNotFoundError as e:
        print(f"Error: A file was not found. Please check your file paths. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
# generate_resume('twenty_second_profile.json', 'twenty_second_template.html', 'twenty_second_resume.pdf')
