# Data Processing Pipeline and Web Dashboard

A real-time data processing pipeline coupled with a responsive web dashboard that fetches, processes, and visualizes stock market data using the Yahoo Finance API.

This project demonstrates an end-to-end data pipeline cycle including data extraction, transformation, storage, automation, and presentation using modern technologies.

---

## Features

- **Real-time Data Fetching:** Uses the [yfinance API](https://pypi.org/project/yfinance/) to retrieve up-to-date stock market data.
- **Automated Workflow:** Apache Airflow orchestrates the data pipeline with DAG creation, scheduling, and logging.
- **Data Storage:** Processed data is stored in a PostgreSQL database.
- **Database Management:** View and manage database records using DBeaver.
- **Backend API:** Flask serves as the backend to expose APIs that read data from the PostgreSQL database.
- **Frontend Dashboard:** React-based web dashboard visualizes the latest stock open and close prices for a selected ticker symbol (default: AAPL).
- **Containerized Architecture:** The project runs two Docker containers — one for the data processing pipeline (Airflow, PostgreSQL) and one for the web dashboard (Flask API, React app) — enabling easy deployment and scalability.
- **CI/CD Automation**: Basic GitHub Actions workflows automate testing, linting, and deployment of both backend and frontend services whenever changes are pushed to the repository.

---

## Technologies Used

- **Data Extraction & Automation:** Apache Airflow, yfinance API
- **Database:** PostgreSQL
- **Backend:** Flask
- **Frontend:** React.js
- **Containerization:** Docker, Docker Compose
- **Database GUI:** DBeaver
- **CI/CD:** Github Actions

---

## Architecture Overview

1. **Data Extraction:** Airflow DAG fetches real-time stock prices using yfinance.
2. **Data Storage:** The fetched data is cleaned and inserted into a PostgreSQL database.
3. **Backend Service:** Flask API queries PostgreSQL for the latest stock data.
4. **Frontend Dashboard:** React app fetches data from Flask API and displays recent open/close prices.
5. **Automation & Logging:** Airflow manages the workflow scheduling and provides detailed logs.

---

## Visual Overview

### React Web Dashboard  
![React Web Dashboard](https://github.com/user-attachments/assets/e48518dd-25ac-46c2-b7c8-79f671aa1d28)

### Apache Airflow DAG  
![Apache Airflow DAG](https://github.com/user-attachments/assets/c5982452-8fee-4c52-a2ca-859ce2d54871)

### Apache Airflow Run Log  
![Apache Airflow Run Log](https://github.com/user-attachments/assets/aefc183f-7a58-4496-bfa4-9fc45bb0d889)

### DBeaver PostgreSQL Connection  
<img width="1470" alt="DBeaver PostgreSQL Connection" src="https://github.com/user-attachments/assets/317e05f8-8055-427d-abc8-b9bb4f838b47" />

### Docker Container Desktop  
<img width="1470" alt="Docker Container Desktop" src="https://github.com/user-attachments/assets/2070681f-07bd-4457-8f14-66becd7b9c2b" />

---

## Future Improvements

- Add support for multiple ticker symbols with dynamic input on the dashboard.
- Implement data caching and optimized queries for faster response times.
- Add more financial indicators and visualizations.
- Enhance error handling and logging in the pipeline.
- Integrate user authentication for personalized dashboards.

---
