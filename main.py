import os
import datetime
import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

def get_invoice_number():
    return "018"

def generate_invoice_from_json(json_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(BASE_DIR, 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('caribbeancode.html')

    # Chargement du JSON complet
    with open(json_path, 'r', encoding='utf-8') as f:
        invoice_data = json.load(f)

    invoice_id = get_invoice_number()
    invoice_data.setdefault("currency", "€")
    invoice_data["invoice_id"] = invoice_id
    invoice_data["date"] = datetime.date.today().strftime("%B %d, %Y")
    invoice_data["total"] = sum(i["quantity"] * i["unit_price"] for i in invoice_data["items"])
    invoice_data["type"] = invoice_data["type"]

    # Optionnel : ajouter la devise au contexte Jinja
    invoice_data["currency"] = "€"

    output_path = f"./invoice_{invoice_id}.pdf"
    html_out = template.render(invoice_data)
    HTML(string=html_out, base_url=template_dir).write_pdf(output_path)

    print("✅ PDF généré :", output_path)
    return output_path

# Exemple d'appel
if __name__ == "__main__":
    generate_invoice_from_json("quote.json")
