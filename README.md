# ⚡ Real-Time Polling Engine

A high-performance, event-driven asynchronous web application designed to handle live user polling with instantaneous updates. This project leverages a modern full-stack backend architecture to manage thousands of concurrent connections smoothly without blocking input/output operations.

---

## 🚀 Live Demo
You can view the local running endpoint of this application here:  
🔗 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🛠️ System Architecture & Tech Stack

This engine is built entirely using an asynchronous pipeline to ensure optimal throughput and near-zero latency for live analytics updates.

* **Backend Framework:** **FastAPI (Python 3.12)** - Utilizes asynchronous event loops (`async/await`) for extreme data speed and native OpenAPI docs documentation.
* **Real-Time Transport:** **HTML5 WebSockets** - Maintains a persistent, bi-directional full-duplex TCP tunnel between frontend dashboards and backend routing layers.
* **Database Management:** **MySQL Server** - Core relational database mapping structural dependencies securely via **SQLAlchemy Async ORM**.
* **Concurrency & State Management:** **Redis** - In-memory data structures executing high-speed Pub/Sub messaging and uniqueness evaluations.

---

## 🏗️ Technical Implementation Details

### 1. High-Performance Event Loop Integration
Bypasses the standard OS framework blockages by directly enforcing clean `asyncio` execution paradigms on local environments, initializing workers seamlessly via programmatically configured Uvicorn run sequences:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, loop="asyncio")

Asynchronous Commits: Database transactions leverage non-blocking async drivers (aiomysql), preventing data bottlenecks during peak traffic loads.

Voter Identification: Implements real-time browser fingerprint validation through Redis Sets (SADD), evaluating entity uniqueness before pushing expensive transactions to the physical database hardware.

Cascading Rules Engine: Engineered database integrity using relational object maps (cascade="all, delete-orphan"), preventing orphaned records on parent record drop loops.

polling_engine/
│
├── main.py            # Primary application server, WebSocket handlers, and API endpoints
├── database.py        # Asynchronous MySQL connection setup and session configuration
├── models.py          # SQLAlchemy models defining the relational database schema
├── schemas.py         # Pydantic data schemas for request/response serialization
├── index.html         # Live UI dashboard harness with real-time WebSocket listening logic
└── requirements.txt   # File containing all project dependencies and versions

Prerequisites
Make sure you have Python 3.12+, MySQL Server, and Redis installed and running on your machine.

Clone the repository:

Bash
git clone [https://github.com/ayushiKhandelwal24/Real-Time-Polling-Engine.git](https://github.com/ayushiKhandelwal24/Real-Time-Polling-Engine.git)
cd Real-Time-Polling-Engine
Install the dependencies:

Bash
pip install -r requirements.txt
Configure Database Settings:
Update your database credentials inside database.py to match your local MySQL configuration string.

Launch the Engine Application:

Bash
python main.py
Access Dashboard UI:
Open your browser and navigate to http://127.0.0.1:8000 to interact with the engine.
