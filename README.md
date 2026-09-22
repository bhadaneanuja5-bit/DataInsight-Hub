# 📊 DataInsight Hub

DataInsight Hub is a Django-based data analytics platform that allows users to upload CSV datasets, explore their data, generate automatic insights, view statistical summaries, and visualize relationships between numeric columns.

The project combines web development and data analytics using Python, Django, Pandas, and Chart.js.

---

## 🎯 Project Objective

The main objective of DataInsight Hub is to make basic data analysis easier for users without requiring them to manually write Python code for every dataset.

Users can upload a CSV file and quickly explore:

- Dataset size
- Column information
- Missing values
- Numeric columns
- Statistical summaries
- Average values
- Minimum and maximum values
- Automatic observations
- Interactive data visualization

---

# ✨ Features

## 👤 User Authentication

DataInsight Hub includes user authentication using Django's built-in authentication system.

Features include:

- User registration
- User login
- User logout
- Session-based authentication
- User-specific dataset access

---

## 📤 Dataset Upload

Users can upload CSV datasets through the web interface.

Features include:

- CSV file upload
- Dataset description
- Automatic dataset storage
- Automatic redirection to the analysis page
- User-specific dataset association

---

## 🔍 Data Analysis

The application automatically analyzes uploaded datasets using Pandas.

It provides:

- Number of rows
- Number of columns
- Column names
- Missing values
- Missing data percentage
- Numeric column detection
- Statistical summary

---

## 💡 Automatic Data Insights

The application automatically calculates insights for numeric columns.

It provides:

- Average values
- Minimum values
- Maximum values
- Highest average numeric column
- Lowest average numeric column
- Basic dataset observations

For example:

```text
The dataset has no missing values.

The dataset contains 4 numeric columns.

R&D Spend has the highest average value among numeric columns.
