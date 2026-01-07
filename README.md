# 🏠 Property-Valuation
**Tabular Data + Satellite Imagery**

## 📌 Project Overview
This project implements a **multimodal regression system** to predict residential property prices by combining:

- **Structured tabular data** (location, size, temporal features, etc.)
- **Satellite imagery** capturing environmental and neighborhood context

A **CNN-based image feature extractor** is used to encode satellite images into numerical embeddings, which are fused with tabular features and modeled using **LightGBM**.  
The goal is to demonstrate that incorporating visual context improves valuation accuracy over traditional tabular-only models.

---

## 🧠 Modeling Approach

### 1. Tabular Pipeline
- Data cleaning and preprocessing
- Feature engineering (e.g., extracting year and month from date)
- Baseline regression using LightGBM

### 2. Image Pipeline
- Satellite images processed using a pretrained CNN
- Fixed-length image embeddings extracted and cached
- Embeddings represent neighborhood and environmental characteristics

### 3. Multimodal Fusion
- Tabular features concatenated with image embeddings
- LightGBM trained on the fused feature space
- Performance compared against a tabular-only baseline

---

## 📊 Exploratory Data Analysis (EDA)
The following analyses and visualizations are included:
- Distribution of property prices
- Temporal trends in prices
- Sample satellite images showing neighborhood variation
- Visual insights relating greenery, road density, and built-up areas to property value

All EDA plots and images are documented in the final report.

---

## 🏗️ Architecture (High Level)

Satellite Images ──► CNN ──► Image Embeddings ┐
                                              ├─► Feature Fusion ─► LightGBM ─► Price
Tabular Features ─────────────────────────────┘

---

## 📈 Results
The **multimodal model (Tabular + Satellite Images)** outperforms the tabular-only baseline:

- Lower prediction error (RMSE)
- Higher explained variance (R²)
- Better capture of neighborhood-level value drivers

Detailed quantitative results are provided in the project report.

---

## 📁 Project Structure
├── data/
│ ├── train(1).xlsx
│ ├── test2.xlsx
│ ├── cleaned/
│     ├── train_clean.xlsx
│     ├── test_clean.xlsx
│     └── image_embeddings.npy
│ ├── sattelite_images_test/
│ └── satellite_images/
│
├── eda.ipynb
├── feature_engineering.ipynb
├── multimodal_training.ipynb
│
├── models/
│ ├── cnn_feature_extractor.pkl
│ └── lightgbm_model.pkl
│
├── 23112054_final.csv # Prediction file (submission)
├── 23112054_report.pdf # Final project report (PDF)
└── README.md
