# S&P 500 Stock Return Analyzer

A Streamlit web app that lets users compare the 1-year return of any two S&P 500 stocks under the same investment budget, powered by live data from Yahoo Finance.

---

## 1. Problem & User

> *Which of two S&P 500 stocks would have generated a higher return if I had invested the same budget 1 year ago?*

This tool is designed for investors who want a quick, visual, and data-driven way to compare two stocks fairly when they trade at very different price levels. — without needing to write code themselves. This tool answers the question: *given the same budget, which of two S&P 500 stocks would have generated a higher return over the past year?* 

## 2. Data
- **Source:** Stooq (https://stooq.com) — free public historical price data, no API key required
- **Access date:** 25 April 2026
- **Coverage:** Any US-listed stock using standard ticker symbols (e.g. AAPL, MSFT, TSLA)
- **Key fields:** Date, Close price (daily, resampled to weekly)
- **Method:** `pandas.read_csv()` via direct Stooq CSV URL — no third-party library required

## 3. Methods
1. **Data acquisition** — fetch daily closing prices from Stooq via URL, parsed directly into a `pandas` DataFrame
2. **Cleaning** — sort ascending (Stooq returns newest-first), drop nulls, resample daily → weekly using `.resample("W").last()`
3. **Alignment** — both series clipped to a common start date for a fair comparison window
4. **Investment simulation** — calculate shares purchased (`budget // start_price`), final portfolio value, and profit/loss
5. **Risk metrics** — annualised volatility from weekly log-returns (`std × √52`), maximum drawdown, 52-week high/low
6. **Visualisation** — three `matplotlib` charts: normalised index chart (both rebased to 100), portfolio value over time, side-by-side return bar chart

## 4. Key Findings
- Normalising both stocks to 100 at the start reveals momentum differences that raw price charts hide
- A higher return does not always mean lower risk — the tool shows volatility and max drawdown alongside return so users can assess risk-adjusted performance
- Whole-share purchasing means the actual cash deployed differs slightly between stocks, which affects the real P&L comparison
- Short-term (1-year) return rankings can reverse significantly depending on the exact start date chosen
- Weekly resampling removes daily noise while preserving meaningful intra-year price trends

## 5. How to Run

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/sp500-stock-analyzer.git
cd sp500-stock-analyzer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the Streamlit app
streamlit run app.py
```

**Requirements:** Python 3.9+, packages listed in `requirements.txt`
No API key or account needed — data loads automatically from Stooq.

To run the notebook:
```bash
jupyter notebook ACC102_notebook.ipynb
```

## 6. Product Link / Demo
- 🌐 Live app: [your Streamlit Cloud link here]
- 🎥 Demo video: [your video link here]

## 7. Limitations & Next Steps
**Current limitations:**
- Price return only — dividends not separately itemised (may understate total return for dividend-paying stocks)
- Whole shares only — fractional share investing not modelled
- Fixed 1-year lookback — results are sensitive to the exact start date
- Stooq may not carry data for very small-cap or recently listed stocks

**Possible next steps:**
- Add a benchmark comparison line (e.g. SPY / S&P 500 index)
- Include Sharpe ratio for a formal risk-adjusted return metric
- Allow user-defined date range beyond 1 year
- Support dividend-adjusted total return calculation
- Add a third stock slot for three-way comparison

