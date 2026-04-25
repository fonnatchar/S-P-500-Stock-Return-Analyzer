# S&P-500-Stock-Return-Analyzer

A Streamlit web app that lets users compare the 1-year return of any two S&P 500 stocks under the same investment budget, powered by live data from Yahoo Finance.


## 🎯 Analytical Problem

> *Which of two S&P 500 stocks would have generated a higher return if I had invested the same budget 1 year ago?*

This tool is designed for investors who want a quick, visual, and data-driven way to compare the performance and risk profile of two stocks — without needing to write code themselves.

---

## 🚀 Live Demo

👉 [View on Streamlit Cloud](#) *(replace with your deployed link)*

Demo video: [Watch 1–3 min walkthrough](#) *(replace with your video link)*

---

## 📦 Features

| Feature | Description |
|---|---|
| **Live data** | Fetches real weekly closing prices via `yfinance` |
| **Investment simulation** | Calculates shares bought, final value, and P&L for any budget |
| **Normalised chart** | Index-to-100 price chart for fair comparison regardless of stock price |
| **Portfolio value chart** | Shows dollar value of the portfolio over time |
| **Risk metrics** | Annualised volatility, 52-week high/low, and maximum drawdown |
| **Return bar chart** | Side-by-side visual return comparison |
| **Raw data view** | Expandable table of weekly prices |

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/sp500-stock-analyzer.git
cd sp500-stock-analyzer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

---

## 📁 File Structure

```
sp500-stock-analyzer/
│
├── app.py                  # Main Streamlit application
├── ACC102_notebook.ipynb   # Python analysis notebook
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── reflection_report.md    # 500–800 word reflection
```

---

## 📋 Requirements

```
streamlit>=1.32.0
yfinance>=0.2.40
pandas>=2.0.0
numpy>=1.26.0
matplotlib>=3.8.0
```


---

## 📊 Data Source

- **Provider:** Yahoo Finance
- **Library:** [`yfinance`](https://pypi.org/project/yfinance/) (open-source, MIT licence)
- **Frequency:** Weekly closing prices
- **Window:** 1 year from the date the app is run
- **Access:** Data is fetched live at runtime

---


.
