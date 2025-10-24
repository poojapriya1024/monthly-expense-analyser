import os
import re
import pandas as pd
from flask import Flask, render_template, request
from markupsafe import escape
from fpdf import FPDF
import matplotlib.pyplot as plt

app = Flask(__name__, static_url_path='/static')

# Allowed file extensions for upload
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get('/')
def upload():
    return render_template('index.html')

def sort_expenses(expenses, amounts):
    expense_categories = {
        'Bills': ['bills', 'bill', 'deposit', 'loan'],
        'Food & Groceries': ['vegetables', 'fruits', 'food', 'snacks', 'Swiggy', 'Zomato'],
        'Entertainment': ['shopping', 'footwear', 'movies', 'dining'],
        'Health Care & Self Care': ['gym', 'medicines'],
        'Transportation': ['petrol', 'diesel', 'bus', 'car', 'train'],
        'Savings': ['savings', 'fixed deposit']
    }
    
    expense_amount = {cat: 0 for cat in expense_categories}

    for expense, amount in zip(expenses, amounts):
        for category, keywords in expense_categories.items():
            pattern = re.compile(r'\b(?:{})\b'.format('|'.join(keywords)), re.IGNORECASE)
            if pattern.search(expense):
                expense_amount[category] += amount
                break

    return expense_amount

def create_pie_chart(data):
    labels = list(data.keys())
    values = list(data.values())
    colors = ['#787FF6', '#7BD5F5', '#4ADEDE', '#1CA7EC', '#1F2F98', '#FFE45C']

    plt.figure(dpi=300)
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Expense Analyser', fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(top=0.8)
    plt.savefig('pie_chart.png', dpi=300)

def excel_to_list(dataframe):
    # Sanitize and validate data
    dataframe = dataframe.dropna(subset=['Description', 'Amount'])
    dataframe['Description'] = dataframe['Description'].astype(str).str.strip()
    dataframe['Amount'] = pd.to_numeric(dataframe['Amount'], errors='coerce').fillna(0)

    description_list = dataframe['Description'].tolist()
    amount_list = dataframe['Amount'].tolist()
    expense_amount = sort_expenses(description_list, amount_list)
    generate_pdf(expense_amount)

def generate_pdf(expense_amount):
    create_pie_chart(expense_amount)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.rect(5.0, 5.0, 200.0, 287.0)
    pdf.image('pie_chart.png', x=10, y=pdf.get_y() + 10, w=190)
    output_path = r'C:\Users\Pooja priya\OneDrive\Desktop\myReport.pdf'
    pdf.output(output_path)

@app.post('/download')
def download_chart():
    file = request.files['file']
    if not file or not allowed_file(file.filename):
        return "<h3>Invalid file type. Please upload an Excel file (.xlsx or .xls).</h3>", 400

    filename = os.path.basename(file.filename)
    file.save(filename)
    data = pd.read_excel(filename)

    # Validate required columns
    if 'Description' not in data.columns or 'Amount' not in data.columns:
        return "<h3>Invalid file format. Please include 'Description' and 'Amount' columns.</h3>", 400

    excel_to_list(data)
    message = "Your PDF has been generated successfully."
    return f"<h2>{escape(message)}</h2>"

if __name__ == '__main__':
    app.run(debug=True)
