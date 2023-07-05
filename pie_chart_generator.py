import re
from fpdf import FPDF
import matplotlib.pyplot as plt

def create_pie_chart(data):
    labels = list(data.keys())
    values = list(data.values())
    colors = ['#799EF6', '#4ADEDE', '#1AA7EC', '#1E2F97', '#128FC8', '#FFE45C']

    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()




expenses = [
    'Water Bill',
    'Electric Bill',
    'Vet bills',
    'Vegetables',
    'Fruits',
    'Snacks',
    'Shopping Clothes',
    'Dining Out',
    'Movies',
    'Gym Membership',
    'Medicines',
    'Petrol fare',
    'Cable bill',
    'Travel Savings',
    'Educational Savings',
    'Housing Loan'
]

expense_categories = {
    'Bills': ['bills', 'bill', 'deposit','loan'],
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

amounts = [3000, 4000, 1500, 2500, 2000, 500, 5000, 2500, 2500, 7000, 2500, 3000,3000, 15000, 10000, 15000]

for expense, amount in zip(expenses, amounts):
    for category, keywords in expense_categories.items():
        pattern = re.compile(r'\b(?:{})\b'.format('|'.join(keywords)), re.IGNORECASE)
        if pattern.search(expense):
            categorized_expenses[category].append(expense)
            expense_amount[category] += amount
            break


create_pie_chart(expense_amount)
