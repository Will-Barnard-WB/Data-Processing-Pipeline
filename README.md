# Real-Time Stock Analytics Pipeline

  An end-to-end, event-driven data pipeline that ingests minute-level stock prices, streams them through Kafka to independent processing
  consumers, persists results to PostgreSQL, and serves live analytics and ML price predictions to a React dashboard over WebSockets.
  Containerised with Docker and deployed on AWS EC2 with a GitHub Actions CI/CD pipeline.

   **Live demo:** http://18.210.105.227:3030

  <img width="1470" height="956" alt="image" src="https://github.com/user-attachments/assets/a0f5a9a1-f268-4b86-9686-507bce3bc8dc" /> 
  
  ## What it does

  A scheduled Airflow DAG fetches minute-level prices for a ticker (AAPL by default) and publishes them to Kafka. Two independent Python
  consumers fan out from there — one computes live analytics and an ML price prediction, the other persists everything to PostgreSQL. A
  Flask/Socket.IO backend streams the latest data to a React dashboard in real time.

  ```
  Airflow DAG ──► Kafka: stock-raw ──► ml-consumer ──► Kafka: stock-predictions
  (minute-level                        (RSI + regression                 │
   yfinance)                            prediction)         ┌────────────┴────────────┐
                                                            ▼                         ▼
                                                  postgres-consumer           Flask + Socket.IO
                                                       │                            │
                                                       ▼                            ▼
                                                  PostgreSQL              React dashboard (WebSocket)
  ```

  ## Architecture

  - **Ingestion** — a scheduled Airflow DAG pulls minute-level prices via `yfinance` and produces them to the Kafka `stock-raw` topic.
  - **Processing** — `ml-consumer` reads `stock-raw`, computes RSI(14), a 5-period moving average, and a regression-based next-close
  prediction, then publishes to `stock-predictions`.
  - **Persistence** — `postgres-consumer` reads `stock-predictions` and upserts into PostgreSQL (`ON CONFLICT` for safe re-runs).
  - **Delivery** — a Flask + Socket.IO backend streams live updates to a React dashboard over WebSockets (price chart, RSI gauge, ML
  prediction).

  ## Tech stack

  | Layer          | Technology                                    |
  |----------------|-----------------------------------------------|
  | Language       | Python (pipeline) · JavaScript (dashboard)    |
  | Orchestration  | Apache Airflow                                |
  | Streaming      | Apache Kafka + Zookeeper                       |
  | Processing     | Python consumers (RSI, regression prediction) |
  | Database       | PostgreSQL                                     |
  | Backend / API  | Flask + Socket.IO                             |
  | Frontend       | React                                          |
  | Infra / CI-CD  | Docker Compose, AWS EC2, GitHub Actions       |

  ## Running locally

  ```bash
  # 1) pipeline: Airflow + Kafka + Zookeeper + Postgres + consumers
  cd "Data Processing Pipeline"
  echo "AIRFLOW_UID=$(id -u)" > .env
  docker-compose up -d --build

  # 2) dashboard: Flask + React
  cd ../Web-Dashboard
  docker-compose up -d --build  
  ```
  Open the dashboard at `http://localhost:3030`, then unpause the `dag_yfinance` DAG in the Airflow UI (`http://localhost:8080`).

  ## Deployment

  Deployed on AWS EC2 as a 10-service Docker stack, live at http://18.210.105.227:3030. A GitHub Actions pipeline builds, lints, and
  auto-deploys to EC2 on every push.
  
