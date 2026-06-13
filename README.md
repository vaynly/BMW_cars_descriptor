# 🏎️ The Best Cars — BMW: Second-Hand Market Descriptor

Welcome to **The Best Cars — BMW**, a sophisticated, interactive data dashboard designed to help enthusiasts and potential buyers navigate the second-hand BMW market with confidence. Built with **Python**, **Dash**, and **Plotly**, this tool transforms raw market data into actionable insights through high-performance visualizations.

---

## 🌟 Key Features

### 📊 Comprehensive Market Analysis
*   **3D Market Surface**: A rotatable 3D scatter plot visualizing the relationship between **Year, Mileage, and Price**. Find the "sweet spot" for your next purchase.
*   **Price Trends**: Analyze average price dynamics across production years to understand depreciation patterns.
*   **Market Hierarchy**: Explore the distribution of models across different transmission and fuel types using interactive Sunburst charts.

### ⚡ Efficiency & Performance
*   **MPG vs. Engine Size**: Compare fuel economy against engine displacement to find the most efficient powerhouses.
*   **Efficiency Profiles**: Radar charts comparing normalized metrics (Price, Mileage, Tax, MPG) across multiple models simultaneously.
*   **Transmission Impact**: Boxplots showing how different gearboxes (Manual, Automatic, Semi-Auto) affect fuel consumption.

### 🔍 Smart Choice: Data-Driven Finder
*   **Interactive DataTable**: Sort and filter through hundreds of listings in real-time.
*   **Dynamic Car Profiles**: Select any car from the table to view its **technical headshot**, technical specifications, and detailed market positioning.
*   **Mini Distribution**: Instant visual feedback on price distribution for your current search filters.

### 🛠️ Advanced Filtering System
*   **Global Filters**: A persistent sidebar allowing you to filter the *entire* dashboard by **Model** and **Year Range**.
*   **Real-time KPI Cards**: Instant calculation of **Total Ads, Average Price, Min Price,** and **Max Price** based on your active filters.

---

## 🎨 Design & Aesthetics
The dashboard features a **Modern Dark Theme** with a high-contrast color palette:
*   **Primary Colors**: Pure Black (`#000000`) and Pure White (`#ffffff`).
*   **Accents**: BMW-inspired Red (`#e71010`) and Sky Blue (`#638FEF`).
*   **UI/UX**: Custom CSS provides an elegant, responsive layout with interactive hover states and smooth transitions.

---

## 🚀 Getting Started

### Prerequisites
*   Python 3.8+
*   `pip` package manager

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd BMW_cars_descriptor
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to `http://127.0.0.1:8050`.

---

## 📂 Project Structure
*   `app.py`: Main application logic and server setup.
*   `assets/`: Contains custom CSS (`style.css`), logos, and car model images.
*   `bmw.csv`: The core dataset containing market listings.
*   `requirements.txt`: List of necessary Python libraries.

---

## 👤 Author
**Elizaveta Mishchanka**
*   *Student of Artificial Intelligence*
*   Produced with passion for automotive data and elegant software design.

---
*Note: Data was sourced from Kaggle's BMW Car Sales Dataset.*
