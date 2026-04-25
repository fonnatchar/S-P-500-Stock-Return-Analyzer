"""
S&P 500 Stock Return Analyzer — Streamlit Interactive App
ACC102 Mini Assignment | Track 4 — Interactive Data Analysis Tool
Author: [Your Name] | Student ID: [Your ID]
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from datetime import datetime, timedelta

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="S&P 500 Stock Return Analyzer",
    page_icon="📈",
    layout="wide",
)

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("📈 S&P 500 Stock Return Analyzer")
st.markdown(
    "Compare the 1-year return of **two S&P 500 stocks** under the same investment budget. "
    "Data is sourced from Yahoo Finance via the `yfinance` library."
)
st.divider()

# ── Sidebar inputs ────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    ticker1 = st.text_input("Stock A ticker", value="AAPL").upper().strip()
    ticker2 = st.text_input("Stock B ticker", value="MSFT").upper().strip()
    budget  = st.number_input("Investment budget (USD)", min_value=100.0,
                               max_value=10_000_000.0, value=10_000.0, step=100.0,
                               format="%.2f")
    run_btn = st.button("🔍 Analyze", use_container_width=True, type="primary")
    st.caption("Data: Yahoo Finance (weekly closes, 1-year window)")

# ── Helper functions ──────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def fetch_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Download weekly adjusted close prices from Yahoo Finance."""
    df = yf.download(ticker, start=start, end=end, interval="1wk",
                     auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError(f"No data returned for '{ticker}'. "
                         "Please check the ticker symbol.")
    df = df[["Close"]].dropna()
    df.columns = ["Close"]
    return df


def annualised_volatility(prices: pd.Series) -> float:
    """Annualised volatility from weekly log-returns (×√52)."""
    log_ret = np.log(prices / prices.shift(1)).dropna()
    return float(log_ret.std() * np.sqrt(52) * 100)


def max_drawdown(prices: pd.Series) -> float:
    """Maximum drawdown percentage over the period."""
    roll_max = prices.cummax()
    drawdown = (prices - roll_max) / roll_max
    return float(drawdown.min() * 100)


def investment_summary(df: pd.DataFrame, budget: float) -> dict:
    """Compute key investment metrics for one stock."""
    p0   = float(df["Close"].iloc[0])
    pN   = float(df["Close"].iloc[-1])
    ret  = (pN - p0) / p0 * 100
    shares   = int(budget // p0)
    invested = shares * p0
    final_val = shares * pN
    pnl  = final_val - invested
    hi   = float(df["Close"].max())
    lo   = float(df["Close"].min())
    vol  = annualised_volatility(df["Close"])
    mdd  = max_drawdown(df["Close"])
    return dict(p0=p0, pN=pN, ret=ret, shares=shares,
                invested=invested, final_val=final_val,
                pnl=pnl, hi=hi, lo=lo, vol=vol, mdd=mdd)


# ── Main analysis ─────────────────────────────────────────────────────────────
if run_btn or True:          # auto-run on first load with defaults
    if ticker1 == ticker2:
        st.error("Please enter two different ticker symbols.")
        st.stop()

    end_date   = datetime.today()
    start_date = end_date - timedelta(days=365)
    end_str    = end_date.strftime("%Y-%m-%d")
    start_str  = start_date.strftime("%Y-%m-%d")

    with st.spinner(f"Fetching data for {ticker1} and {ticker2}…"):
        try:
            df1 = fetch_data(ticker1, start_str, end_str)
            df2 = fetch_data(ticker2, start_str, end_str)
        except ValueError as e:
            st.error(str(e))
            st.stop()

    # Align to common date range
    common_start = max(df1.index[0], df2.index[0])
    df1 = df1[df1.index >= common_start]
    df2 = df2[df2.index >= common_start]

    m1 = investment_summary(df1, budget)
    m2 = investment_summary(df2, budget)

    access_date = datetime.today().strftime("%d %B %Y")
    winner = ticker1 if m1["ret"] > m2["ret"] else (ticker2 if m2["ret"] > m1["ret"] else None)

    # ── Winner banner ─────────────────────────────────────────────────────────
    if winner:
        wm = m1 if winner == ticker1 else m2
        st.success(
            f"**{winner}** outperformed over the past year with a "
            f"**{wm['ret']:+.2f}%** return — a **${wm['pnl']:+,.2f}** "
            f"profit/loss on your ${budget:,.2f} budget."
        )
    else:
        st.info("Both stocks delivered identical returns over the period.")

    # ── Metric cards ──────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    for col, ticker, m in [(col1, ticker1, m1), (col2, ticker2, m2)]:
        with col:
            st.subheader(f"🔷 {ticker}" if ticker == ticker1 else f"🔶 {ticker}")
            c1, c2 = st.columns(2)
            c1.metric("Start price",   f"${m['p0']:,.2f}")
            c2.metric("End price",     f"${m['pN']:,.2f}")
            c1.metric("1-year return", f"{m['ret']:+.2f}%")
            c2.metric("Shares bought", f"{m['shares']:,}")
            c1.metric("Final value",   f"${m['final_val']:,.2f}")
            c2.metric("Profit / Loss", f"${m['pnl']:+,.2f}")

    st.divider()

    # ── Normalised price chart ────────────────────────────────────────────────
    st.subheader("Normalised price performance (indexed to 100)")
    norm1 = (df1["Close"] / df1["Close"].iloc[0]) * 100
    norm2 = (df2["Close"] / df2["Close"].iloc[0]) * 100

    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(norm1.index, norm1.values, label=ticker1, color="#378ADD",
            linewidth=2)
    ax.plot(norm2.index, norm2.values, label=ticker2, color="#D85A30",
            linewidth=2, linestyle="--")
    ax.axhline(100, color="gray", linewidth=0.8, linestyle=":")
    ax.set_ylabel("Indexed value (start = 100)")
    ax.set_xlabel("Date")
    ax.legend()
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.0f"))
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # ── Portfolio value chart ─────────────────────────────────────────────────
    st.subheader("Portfolio value over time")
    port1 = df1["Close"] * m1["shares"]
    port2 = df2["Close"] * m2["shares"]

    fig2, ax2 = plt.subplots(figsize=(11, 4))
    ax2.fill_between(port1.index, port1.values, alpha=0.15, color="#378ADD")
    ax2.fill_between(port2.index, port2.values, alpha=0.15, color="#D85A30")
    ax2.plot(port1.index, port1.values, label=ticker1, color="#378ADD", linewidth=2)
    ax2.plot(port2.index, port2.values, label=ticker2, color="#D85A30",
             linewidth=2, linestyle="--")
    ax2.axhline(budget, color="gray", linewidth=0.8, linestyle=":", label="Initial budget")
    ax2.set_ylabel("Portfolio value (USD)")
    ax2.set_xlabel("Date")
    ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax2.legend()
    ax2.spines[["top", "right"]].set_visible(False)
    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

    # ── Risk metrics ──────────────────────────────────────────────────────────
    st.divider()
    st.subheader("Risk & volatility metrics")
    rc1, rc2 = st.columns(2)
    for col, ticker, m in [(rc1, ticker1, m1), (rc2, ticker2, m2)]:
        with col:
            st.markdown(f"**{ticker}**")
            r1, r2, r3 = st.columns(3)
            r1.metric("52-wk High", f"${m['hi']:,.2f}")
            r2.metric("52-wk Low",  f"${m['lo']:,.2f}")
            r3.metric("Ann. Volatility", f"{m['vol']:.1f}%")
            st.metric("Max Drawdown", f"{m['mdd']:.2f}%",
                      help="Largest peak-to-trough decline over the period")

    # ── Return bar comparison ─────────────────────────────────────────────────
    st.divider()
    st.subheader("Side-by-side return comparison")
    fig3, ax3 = plt.subplots(figsize=(6, 3.5))
    tickers = [ticker1, ticker2]
    returns = [m1["ret"], m2["ret"]]
    colors  = ["#378ADD" if r >= 0 else "#E24B4A" for r in returns]
    bars = ax3.bar(tickers, returns, color=colors, width=0.4, edgecolor="none")
    ax3.axhline(0, color="gray", linewidth=0.8)
    ax3.set_ylabel("1-year return (%)")
    ax3.yaxis.set_major_formatter(mtick.PercentFormatter())
    for bar, val in zip(bars, returns):
        ax3.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + (0.3 if val >= 0 else -1.5),
                 f"{val:+.2f}%", ha="center", va="bottom", fontsize=11,
                 fontweight="bold")
    ax3.spines[["top", "right"]].set_visible(False)
    fig3.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

    # ── Raw data ──────────────────────────────────────────────────────────────
    with st.expander("📋 View raw weekly price data"):
        merged = pd.DataFrame({ticker1: df1["Close"], ticker2: df2["Close"]}).dropna()
        merged.index = merged.index.strftime("%Y-%m-%d")
        st.dataframe(merged.style.format("${:.2f}"), use_container_width=True)

    # ── Data source note ──────────────────────────────────────────────────────
    st.caption(
        f"Data source: Yahoo Finance via `yfinance` library (weekly closing prices, "
        f"1-year window). Accessed {access_date}. "
        "Past performance does not guarantee future results. "
        "This tool is for educational purposes only."
    )
