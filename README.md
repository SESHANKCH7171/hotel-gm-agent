# 🏨 Hotel GM Revenue Intelligence Agent

An AI-powered agent designed specifically for Hotel General Managers to analyze performance, track occupancy, detect revenue leaks, and provide actionable insights in real-time.

---

## 🌟 Key Features

- **📊 Comprehensive Summary Stats**: Instantly get key metrics such as total revenue, ADR, average length of stay, and confirmed booking counts.
- **📈 Interactive Revenue Trend Charts**: Visualize monthly revenue trends between dates using dynamic Plotly charts.
- **🔍 Revenue Leak Detection**: Discover periods with high occupancy but low Average Daily Rate (ADR) to maximize yield.
- **🚫 Cancellation Analytics**: Spot cancellation patterns by market segment.
- **⏱️ Lead Time Reports**: Analyze how far in advance guests book by market segment.

---

## 🛠️ Technology Stack

- **Core**: Python & Streamlit
- **AI Framework**: LangChain & LangChain Google GenAI
- **Data Engine**: Pandas & NumPy
- **Visuals**: Plotly Express

---

## 🚀 Setup & Run Locally

### 1. Clone the repository
```bash
git clone <your-repository-url>
cd HOTEL_GM_AGENT
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Secrets
Create a `.streamlit/secrets.toml` file in the project root:
```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

### 4. Run the App
```bash
streamlit run app.py
```

---

## ☁️ Deployment

This app is optimized for deployment on **Streamlit Community Cloud**:
1. Push this repository to GitHub (ensure `hotel_bookings.csv` is included).
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Connect your GitHub repository and set `app.py` as the main entry point.
4. Add your `GEMINI_API_KEY` under Streamlit Cloud app settings secrets.
