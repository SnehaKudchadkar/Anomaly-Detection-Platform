# 🦟 Dengue Anomaly Detection System
A Streamlit-based application for detecting and explaining anomalies in dengue case data across Goa Talukas using time series matrix profile analysis.

## 🌟 Features
- **Anomaly Detection:** Uses STUMPY's matrix profile algorithm to identify unusual patterns in dengue case data
-** Smart Explanation System:** Automatically generates insights and recommendations based on detected anomalies
- **Interactive Dashboard:** Visualize anomalies with region-specific time series plots
- **Configurable Parameters:** Adjust sensitivity and detection window through an intuitive interface

## 📊 How It Works
- **Upload Data:** CSV file with Date, Region, and Confirmed Cases columns
- **Configure Detection:** Set anomaly severity threshold and detection window size
- **Visualize Results:** See anomalies highlighted on interactive time series plots
- **Receive Insights:** Get automatically generated explanations and response recommendations
- **Analyze Correlations:** View correlations between confirmed cases and deaths for each region

## ⚙️ Technical Architecture
The system consists of three main components:
- **Anomaly Detection Module** (**anomaly.py**): Implements time series anomaly detection using STUMPY's matrix profile algorithm
- **Explanation Engine** (**explain.py**): Generates contextual insights and recommendations for detected anomalies
- **Streamlit Interface** (**app.py**): Provides the user interface and visualization capabilities


## Installation
Install required packages individually
- pip install streamlit
- pip install pandas
- pip install matplotlib
- pip install seaborn
- pip install numpy
- pip install stumpy

## Run the application
streamlit run app.py

## 📋 Requirements
Python 3.7+
pandas
numpy
streamlit
matplotlib
seaborn
stumpy

## 📝 Usage Example
- Upload your dengue case data CSV
- Adjust the anomaly threshold using the sidebar slider (higher = fewer anomalies)
- Set the detection window size based on your data patterns
- Click "Run Anomaly Detection" to generate insights
- Review detected anomalies and their explanations
- Examine the visual time series plots showing anomalous points and correlation between cases and deaths


## 📷 Screenshots
![image](https://github.com/user-attachments/assets/918c6790-bd44-4b58-9396-84f6deaf464f)
![image](https://github.com/user-attachments/assets/6fb3292b-133d-4851-b19c-99f84639e620)
![image](https://github.com/user-attachments/assets/fd853089-1cf7-4468-94c7-1a61649b372e)
![image](https://github.com/user-attachments/assets/bf289919-235b-4d9f-a08d-8e0d6ebb5386)
![image](https://github.com/user-attachments/assets/ed228cdb-a7de-42be-b20f-2d3ff3633f2a)


## 🧠 Anomaly Explanation Logic
The system intelligently generates explanations for anomalies based on:
- Unusually high confirmed cases
- Elevated death counts
- Disproportionate suspected vs. confirmed cases
- Anomaly severity classification
