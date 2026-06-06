import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# --- STEP 1: SIMULATE MESSY RAW DATA ---
print("Generating messy raw data...")
data = {
    'Region': ['North', 'South', 'East', 'West', 'North', 'South', 'East', 'West', 'North', 'South'],
    'Sales': ['12000', '15000', 'invalid_str', '22000', '12000', '15000', '18000', np.nan, '13500', '16000'],
    'Date': ['2026-01-01', '2026/01/02', '2026-01-03', '04-01-2026', '2026-01-01', '2026-01-02', '2026-01-03', '2026-01-04', '2026-01-05', '2026-01-06']
}
df_raw = pd.DataFrame(data)
df_raw.to_csv('raw_data.csv', index=False)

# --- STEP 2: AUTOMATED DATA CLEANING WORKFLOW ---
print("Executing automated cleaning pipeline...")
df = pd.read_csv('raw_data.csv')

# 1. Remove duplicate rows
df.drop_duplicates(inplace=True)

# 2. Fix data type inconsistencies & handle missing values
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')  # Converts 'invalid_str' to NaN
median_sales = df['Sales'].median()
df['Sales'] = df['Sales'].fillna(median_sales)  # Impute missing values with median

# 3. Standardize date formats
df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')

# Save the polished data to Excel for business use
df.to_excel('cleaned_data.xlsx', index=False)

# --- STEP 3: AUTOMATED VISUALIZATION ---
print("Generating summary chart...")
summary = df.groupby('Region')['Sales'].sum().reset_index()

plt.figure(figsize=(6, 4))
plt.bar(summary['Region'], summary['Sales'], color=['#3498db', '#2ecc71', '#e74c3c', '#f1c40f'])
plt.title('Total Sales by Region')
plt.xlabel('Region')
plt.ylabel('Sales ($)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('sales_summary.png')
plt.close()

# --- STEP 4: AUTOMATED REPORT GENERATION (PDF) ---
print("Compiling PDF Executive Report...")
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(52, 73, 94)
        self.cell(0, 10, 'Automated Performance Summary Report', border=0, ln=1, align='C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

pdf = PDFReport()
pdf.add_page()
pdf.set_font('Arial', '', 12)

# Write Summary Text
pdf.set_text_color(44, 62, 80)
pdf.multi_cell(0, 8, "This report was automatically generated following the scheduled data cleaning workflow.\n"
                     "Pipeline operations performed: Duplicate removal, missing value imputation via median, "
                     "and date standardization.")
pdf.ln(10)

# Append Visual Chart
pdf.image('sales_summary.png', x=25, y=50, w=160)

# Save PDF Document
pdf.output('executive_summary_report.pdf')

# Clean up temporary chart image file
if os.path.exists('sales_summary.png'):
    os.remove('sales_summary.png')

print("Workflow complete! 'cleaned_data.xlsx' and 'executive_summary_report.pdf' are ready.")
