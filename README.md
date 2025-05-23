Amazon Reviews Streaming & Sentiment Analysis
This repository contains a fully Dockerized end-to-end pipeline for streaming Amazon review data, performing real-time sentiment classification with Apache Spark MLlib, storing results in MongoDB, and visualizing them both in real-time and offline dashboards built with Django and Chart.js.

🚀 Architecture
text

Copy
Amazon JSONL → Kafka → Spark Structured Streaming →
  ├─ Real-time WebSocket Broadcast (Django Channels) → React/Browser
  └─ MongoDB Archive → Django Offline Dashboard (Chart.js)
Producer: Reads data.jsonl and streams JSON reviews to Kafka topic amazon-reviews.
Spark Processor: Consumes from Kafka, applies a trained Random Forest pipeline (rf_pipeline_amazon_json), tags 10% of messages as test, writes all to MongoDB (amazon.reviews) and broadcasts live reviews via HTTP to Django Channels.
MongoDB: Stores classified reviews with fields: review, sentiment, timestamp, isTest.
Django Dashboard:
Online: Real-time feed via WebSocket /ws/live-reviews/.
Offline: Aggregated charts of last 7 days and sentiment distribution at /reviews/.
📂 Repository Structure
text

Copy
├── kafka_streaming/        # Producer code & Dockerfile
│   ├── producer.py
│   └── Dockerfile
├── spark_processor/        # Spark consumer & ML pipeline
│   ├── consumer.py
│   ├── rf_pipeline_amazon_json/
│   └── Dockerfile
├── reviews_dashboard-main/ # Django project and app
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── reviews_dashboard/  # Django project settings
│   └── reviews/           # Django app: views, urls, templates
├── docker-compose.yml
└── data.jsonl             # Sample Amazon reviews for streaming
🔧 Prerequisites
Docker & Docker Compose
(Optional) make for convenience
🛠 Getting Started
Build all images:

bash

Copy
docker-compose build
Launch services:

bash

Copy
docker-compose up -d \
  zookeeper kafka mongo redis producer spark dashboard
Producer streams all reviews from data.jsonl into Kafka.

Spark processes, classifies, writes to MongoDB, and pushes live to Django.

Dashboard available at:

Real-time feed: http://localhost:8000/reviews/online/
Offline analytics: http://localhost:8000/reviews/
🔍 Verification
MongoDB count:

bash

Copy
docker-compose exec mongo \
  mongo amazon --quiet --eval 'db.reviews.countDocuments({})'
View sample docs:

bash

Copy
docker-compose exec mongo \
  mongo amazon --quiet --eval 'db.reviews.find().limit(5).pretty()'
📝 Notes
Checkpointing is enabled for Spark via checkpointLocation to ensure exactly-once semantics.
WhiteNoise serves static files in Django.
Adjust isTest sampling ratio or Docker Compose ports as needed.
💡 Extending
Add product-level or keyword-level filtering.
Build alerts on high negative rates via Celery or Prometheus.
Scale Kafka partitions and Spark executors for higher throughput.
© 2025 IMAD EL ANNASI. Licensed under MIT.
