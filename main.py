import pandas as pd
from flask import Flask, render_template, request
import re
from fpdf import FPDF
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.get('/')
def upload():
    return render_template('index.html')

def sort_expenses(expenses, amounts):
    expense_categories = {
        'Bills': ['bills', 'bill', 'deposit', 'loan'],
        'Food & Groceries': ['vegetables', 'fruits', 'food', 'snacks'],
        'Entertainment': ['shopping', 'footwear', 'movies', 'dining'],
        'Health Care & Self Care': ['gym', 'medicines'],
        'Transportation': ['petrol', 'diesel', 'bus', 'car', 'train'],
        'Savings': ['savings', 'fixed deposit']
    }
    
    categorized_expenses = {
        'Bills': [],
        'Food & Groceries': [],
        'Entertainment': [],
        'Health Care & Self Care': [],
        'Transportation': [],
        'Savings': []
    }

    expense_amount = {
        'Bills': 0,
        'Food & Groceries': 0,
        'Entertainment': 0,
        'Health Care & Self Care': 0,
        'Transportation': 0,
        'Savings': 0
    }

    for expense, amount in zip(expenses, amounts):
        for category, keywords in expense_categories.items():
            pattern = re.compile(r'\b(?:{})\b'.format('|'.join(keywords)), re.IGNORECASE)
            if pattern.search(expense):
                categorized_expenses[category].append(expense)
                expense_amount[category] += amount
                break
    
    # Returns the dict which contains the net amount from each expense category
    return expense_amount

def create_pie_chart(data):
    labels = list(data.keys())
    values = list(data.values())
    colors = ['#799EF6', '#4ADEDE', '#1AA7EC', '#1E2F97', '#128FC8', '#FFE45C']

    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('pie_chart.png')  # Saving the chart as an image 

def excel_to_list(dataframe):
    # Reads the content and divides them into categories 
    description_column = dataframe['Description']
    description_list = description_column.tolist()
    amount_column = dataframe['Amount']
    amount_list = amount_column.tolist()
    expense_amount = sort_expenses(description_column, amount_list)
    generate_pdf(expense_amount)


def generate_pdf(expense_amount): 
    # Creates the pie chart and generates the PDF
    create_pie_chart(expense_amount)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Expense Breakdown', ln=True, align='C')
    pdf.image('pie_chart.png', x=10, y=10, w=190)  # Add the image to the PDF
    # Request path from the user
    output_path = r'C:\Users\Pooja priya\OneDrive\Desktop\test1.pdf'
    pdf.output(output_path)

@app.post('/download')
def download_chart():
    file = request.files['file']
    file.save(file.filename)
    data = pd.read_excel(file)
    excel_to_list(data)
    return "<h2>Your pdf has been generated succesfully.<h2>"
    

if __name__ == '__main__':
    app.run(debug=1)