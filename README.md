# 🌍 Global Renewable Energy Trends (2000–2023)

An interactive data analysis and visualisation web app built with **Python** and **Streamlit**, exploring global solar, wind, and hydropower generation trends across major countries over two decades.


## 📋 Features

| Tab | Feature |
|-----|---------|
| 📈 Trends | Interactive line charts and stacked area charts by country and source |
| 🔮 Forecast | CAGR-based projection to 2030 with confidence bands |
| 🎮 Scenarios | Policy scenario simulator — aggressive, moderate, conservative growth |
| 🧪 Synthetic Control | Econometric counterfactual analysis comparing countries |
| 🇪🇸 Spain Dashboard | Spain-specific policy milestones and 2030 target tracking |
| 📥 Export | Download filtered dataset as CSV and insight brief as TXT |

### Additional highlights
- 4 KPI metric cards showing global totals and growth since 2000
- Dynamic sidebar filters — countries, year range, energy sources
- Year-on-year growth rate chart
- Country comparison bar chart for any selected year
- World energy mix pie chart
- Spain 2030 gauge indicators vs NECP targets
- Spain Policy Readiness Index (composite score)
- `@st.cache_data` for optimised performance

---

## 🌐 Countries Covered

World · China · USA · Germany · India · Brazil · Spain

---

## 📊 Dataset

Data compiled and approximated from:

- [IEA — International Energy Agency](https://www.iea.org/)
- [IRENA — International Renewable Energy Agency](https://www.irena.org/)
- [Our World in Data — Energy](https://ourworldindata.org/energy)

**Coverage:** Solar, Wind, and Hydropower generation in TWh · Years: 2000–2023

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10+ | Core language |
| Streamlit | 1.32.0 | Web app framework |
| Pandas | 2.2.1 | Data manipulation |
| Plotly | 5.20.0 | Interactive visualisations |
| NumPy | latest | Numerical computation |

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/renewable-energy-trends.git
cd renewable-energy-trends
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub (public repository)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click **New app** → select this repo → set main file as `app.py`
5. Click **Deploy** — live in ~2 minutes

---

## 📁 Project Structure

```
renewable-energy-trends/
│
├── app.py                  # Main Streamlit application
└── README.md               # Project documentation
```

---

## 📈 Key Insights from the Data

- **Solar** grew from just 1 TWh (2000) to 1,850 TWh (2023) globally — a ~185,000% increase
- **Wind** grew from 31 TWh (2000) to 1,980 TWh (2023) — fastest scaling after solar
- **China** now leads all countries in both solar and wind generation
- **Spain** has one of the most mature wind sectors in Europe relative to its size
- **Hydro** remains the largest renewable source but is growing slowly compared to solar and wind

---

## 🔭 Future Improvements

- [ ] Connect to live IEA/IRENA API for real-time data
- [ ] Add CO₂ emissions vs renewable growth correlation
- [ ] Add per capita generation metrics
- [ ] Extend coverage to 50+ countries
- [ ] Add ML-based forecasting (ARIMA / LSTM)

---

## 👤 Author

**Muhammad Ali Afzal**
AI/ML Engineer · Full Stack Developer · BS Computer Science, FAST-NUCES

🌐 [muhammadaliafzalsportfolio.netlify.app](https://muhammadaliafzalsportfolio.netlify.app)
📧 muhammadaliafzal205@gmail.com

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

*Built as part of a growing interest in applying machine learning and data science to clean energy challenges — directly relevant to computational materials research for energy applications.*
