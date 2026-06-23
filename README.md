# PHISHING URL DETECTOR PROJECT

## Project Overview

Membangun aplikasi deteksi phishing berbasis Machine Learning menggunakan dataset:

PhiUSIIL Phishing URL Dataset

Target akhir project:

- Input URL melalui web interface
- Sistem melakukan ekstraksi fitur otomatis
- Model Machine Learning melakukan prediksi
- Output:
  - Legitimate Website
  - Phishing Website
- Menampilkan confidence score
- Deploy sebagai aplikasi web menggunakan Flask

---

# Dataset Information

Dataset:

PhiUSIIL_Phishing_URL_Dataset.csv

Jumlah Data:

235,795 URL

Distribusi Label:

- Legitimate (1): 57.19%
- Phishing (0): 42.81%

Dataset memiliki:

- 55 kolom
- 54 fitur
- 1 target (label)

Target:

```python
label
```

- 1 = Legitimate
- 0 = Phishing

---

# Exploratory Data Analysis (EDA)

Sudah dilakukan:

## Dataset Inspection

```python
df.info()
df.describe()
df.columns.tolist()
```

## Label Distribution

Distribusi target telah dicek.

## Correlation Analysis

Sudah dilakukan analisis korelasi terhadap label.

Feature dengan korelasi tertinggi:

```text
URLSimilarityIndex
HasSocialNet
HasCopyrightInfo
HasDescription
IsHTTPS
DomainTitleMatchScore
HasSubmitButton
IsResponsive
```

---

# Feature Selection

Feature yang tidak digunakan:

```python
URL
Domain
Title
TLD
```

Karena:

- berupa teks
- tidak digunakan pada training awal

Feature yang digunakan:

```python
50 fitur
```

---

# Machine Learning Comparison

Model yang telah dibandingkan:

## Logistic Regression

Accuracy:

```text
0.999851
```

## Decision Tree

Accuracy:

```text
1.000000
```

## KNN

Accuracy:

```text
0.997540
```

## Random Forest

Dipilih sebagai model utama.

Alasan:

- Stabil
- Akurasi sangat tinggi
- Tidak membutuhkan scaling
- Cocok untuk deployment

---

# Training Model Pertama

Model:

```python
RandomForestClassifier
```

Jumlah fitur:

```python
50 fitur
```

File model:

```text
models/phishing_model.pkl
models/feature_names.pkl
```

---

# Analisis Deployment Reality

Saat mulai membuat feature extractor ditemukan masalah besar.

Dataset memiliki beberapa fitur yang tidak bisa direproduksi secara akurat.

Feature yang sulit direproduksi:

```text
URLSimilarityIndex
CharContinuationRate
TLDLegitimateProb
URLCharProb
DomainTitleMatchScore
URLTitleMatchScore
```

Analisis Feature Importance menunjukkan:

```text
URLSimilarityIndex
```

adalah fitur paling berpengaruh.

Namun fitur tersebut tidak bisa direproduksi secara real-time hanya dari URL.

---

# Retraining Model

Keputusan:

Menghapus fitur yang tidak dapat direproduksi.

Jumlah fitur baru:

```text
44 fitur
```

Model retrain:

```python
RandomForestClassifier
```

---

# Hasil Retraining

Dataset:

```text
Train : 188,636
Test  : 47,159
```

Accuracy:

```text
0.9998303611
```

Classification Report:

```text
Precision : 1.00
Recall    : 1.00
F1-Score  : 1.00
```

Performa hampir identik dengan model 50 fitur.

---

# Model Final Saat Ini

File:

```text
models/phishing_model_44.pkl
models/feature_names_44.pkl
```

Jumlah fitur:

```text
44 fitur
```

Status:

```text
READY
```

---

# Project Structure Saat Ini

```text
phising-detector
├── app
│   ├── app.py
│   ├── features
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-313.pyc
│   │   │   ├── feature_extractor.cpython-313.pyc
│   │   │   ├── html_features.cpython-313.pyc
│   │   │   └── url_features.cpython-313.pyc
│   │   ├── feature_extractor.py
│   │   ├── html_features.py
│   │   └── url_features.py
│   ├── static
│   │   └── style.css
│   └── templates
│       └── index.html
├── dataset
│   └── PhiUSIIL_Phishing_URL_Dataset.csv
├── models
│   ├── feature_names.pkl
│   ├── feature_names_44.pkl
│   ├── phishing_model.pkl
│   └── phishing_model_44.pkl
├── notebooks
│   ├── .ipynb_checkpoints
│   │   └── phising-detector-checkpoint.ipynb
│   └── phising-detector.ipynb
├── project.md
└── test
    ├── test_extractor.py
    ├── test_feature_order.py
    ├── test_model.py
    ├── test_predict.py
    ├── test_scraper.py
    └── test_url.py
```

---

# Feature Extractor Status

Sudah dibuat:

## URL Features

Saat ini dapat menghasilkan:

```text
URLLength
DomainLength
IsHTTPS
NoOfSubDomain
TLDLength
HasObfuscation
NoOfObfuscatedChar
ObfuscationRatio
NoOfLettersInURL
NoOfDegitsInURL
LetterRatioInURL
DegitRatioInURL
NoOfEqualsInURL
NoOfQMarkInURL
NoOfAmpersandInURL
NoOfOtherSpecialCharsInURL
SpacialCharRatioInURL
IsDomainIP
NoOfURLRedirect
NoOfSelfRedirect
```

---

## HTML Features

Saat ini dapat menghasilkan:

```text
HasTitle
HasDescription
HasFavicon
NoOfImage
NoOfCSS
NoOfJS
NoOfiFrame
LineOfCode
LargestLineLength
Robots
IsResponsive
HasSubmitButton
HasHiddenFields
HasPasswordField
HasExternalFormSubmit
HasSocialNet
NoOfPopup
Bank
Pay
Crypto
HasCopyrightInfo
NoOfExternalRef
NoOfSelfRef
NoOfEmptyRef
```

---

# Current Problem

Model bekerja.

Feature mapping bekerja.

Jumlah fitur cocok.

Urutan fitur cocok.

Namun hasil prediksi real-world tidak sesuai.

Contoh:

## Google

```text
Prediction : 0
Probability : [0.51 0.49]
```

Padahal harusnya:

```text
Legitimate
```

---

## Github

```text
Prediction : 0
Probability : [0.76 0.24]
```

Padahal harusnya:

```text
Legitimate
```

---

## Bank Mandiri

```text
Prediction : 1
Probability : [0.41 0.59]
```

Sudah benar.

---

# Root Cause Analysis

Sudah dipastikan:

```text
Model tidak bermasalah
Feature order tidak bermasalah
Feature count tidak bermasalah
```

Masalah utama:

Feature extractor menghasilkan distribusi fitur yang berbeda dengan dataset asli.

Contoh:

Google menghasilkan:

```text
HasDescription = 0
HasFavicon = 0
Robots = 0
IsResponsive = 0
```

Padahal website asli kemungkinan memiliki semua fitur tersebut.

---

# Decision

Dipilih:

## Jalur B

Tetap menggunakan model 44 fitur.

Tidak mengurangi jumlah fitur.

Tujuan:

Membuat feature extraction yang lebih akurat dan mendekati proses crawling dataset asli.

---

# Expected Next Phase

Meningkatkan feature extraction menggunakan browser automation.

Tools yang akan dipelajari:

## Selenium

Tujuan:

- Render JavaScript
- Mengambil DOM final
- Menghitung fitur setelah halaman selesai dimuat

## Playwright

Alternatif modern Selenium.

Kemungkinan lebih cepat dan stabil.

---

# Next Objectives

## Phase 1

Audit seluruh fitur:

```text
44 fitur
```

dan identifikasi:

```text
Feature mana yang tidak sesuai dengan dataset asli
```

---

## Phase 2

Migrasi scraper dari:

```python
requests
BeautifulSoup
```

ke:

```python
Playwright
```

atau

```python
Selenium
```

---

## Phase 3

Membandingkan hasil:

```text
Google
Github
Bank Mandiri
Facebook
Instagram
Tokopedia
Shopee
```

dengan ekspektasi model.

---

## Phase 4

Membuat confidence score yang lebih stabil.

---

## Phase 5

Integrasi Flask

Flow:

URL
↓
Feature Extractor
↓
44 Features
↓
Random Forest
↓
Prediction
↓
Confidence Score
↓
Web Interface

---

# Current Progress

Overall Progress:

```text
Dataset Analysis       ██████████ 100%
EDA                    ██████████ 100%
Feature Selection      ██████████ 100%
Model Training         ██████████ 100%
Model Retraining       ██████████ 100%
Feature Extraction     ████████░░ 80%
Prediction Pipeline    ████████░░ 80%
Flask Integration      ░░░░░░░░░░ 0%
Deployment             ░░░░░░░░░░ 0%
```

Current Stage:

```text
Feature Extraction Validation & Real-World Calibration
```
