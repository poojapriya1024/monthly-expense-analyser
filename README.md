# Monthly Expense Analyser

A simple Flask-based web application to analyze monthly expenses from an uploaded spreadsheet, categorize them, and generate a pie chart PDF report for download.

## Features
- Upload an Excel spreadsheet of expenses
- Automatically categorize expenses into predefined groups (Bills, Food & Groceries, Entertainment, Health Care & Self Care, Transportation, Savings)
- Generate a visual pie chart of spending distribution
- Download a PDF report containing the breakdown

## Tech Stack
- Python (Flask, Pandas, Matplotlib, FPDF)
- HTML/CSS for frontend
- Excel file processing

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/poojapriya1024/monthly-expense-analyser.git
cd monthly-expense-analyser
```

2. **Install dependencies**
```bash
pip install flask pandas matplotlib fpdf openpyxl
```
(`openpyxl` is required for reading `.xlsx` files with pandas.)

3. **Run the app**
```bash
python main.py
```

4. Open your browser and go to:
```
http://127.0.0.1:5000/
```

## Usage
1. Click **Choose File** and select your Excel spreadsheet.  
   Example format:
   | Description   | Amount |
   |---------------|--------|
   | Petrol        | 1500   |
   | Vegetables    | 800    |
   | Movie Tickets | 500    |

2. Click **Download Chart**.  
3. The application will:
   - Categorize expenses
   - Generate a pie chart
   - Save a PDF report (`myReport.pdf`) with the chart.

## File Structure
```
monthly-expense-analyser/
│
├── main.py                  # Flask app and core logic
├── templates/
│   └── index.html           # Upload page
├── static/                  # Static files (CSS, JS if any)
├── Sample Input File.xlsx   # Example spreadsheet
└── README.md
```

## Notes
- The output PDF path in `generate_pdf()` is currently hardcoded. Update it to your desired location.
- Ensure your Excel file has columns named exactly **Description** and **Amount**.

## v1.1 – Added Input Sanitization
- Added file type validation (allowed_file)
- Sanitized filename using os.path.basename()
- Validated Excel columns before processing
- Sanitized and cleaned dataframe content (dropna, astype(str), numeric conversion)
- Escaped HTML output to prevent injection
- No behavior change — it still generates the same PDF

## Future Improvements
- Allow users to set custom categories
- Enable direct download of the generated PDF through the web app
- Store and visualize multiple months of data
