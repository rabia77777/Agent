# Logistics Dispatcher System

A full-stack logistics truck dispatcher with:
- React + Tailwind chat UI (typed + voice input)
- FastAPI backend with AI dispatcher logic (assign drivers, compute ETAs, check HOS, notify customers)
- MongoDB for drivers, loads, assignments
- WebSocket for real-time updates
- Dockerized, with docker-compose for local/dev deployment

## Architecture
- Frontend: React (Vite) + Tailwind. A chatbox sends commands to the backend and listens to real-time events.
- Backend: FastAPI with endpoints:
  - POST /api/assign_driver
  - POST /api/route_eta
  - GET /api/drivers/{driver_id}/status (alias: /api/get_driver_status?driver_id=...)
  - POST /api/notify
  - POST /api/chat (AI dispatcher parses chat commands and routes to the above)
  - WebSocket: /ws for real-time broadcast events
- AI: Rule-based parser (extensible) to map natural chat commands to operations. Hours-of-Service (HOS) checks are simplified but enforce realistic constraints.
- DB: MongoDB (collections: drivers, loads, assignments)
- Real-time: WebSocket broadcast to subscribed UIs

## Quickstart

1) Copy environment example and adjust as needed

```bash
cp .env.example .env
```

2) Launch with Docker Compose

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000 (docs at /docs)
- WebSocket: ws://localhost:8000/ws
- MongoDB: mongodb://localhost:27017

3) Seed data

On first startup the backend will seed sample drivers and loads if collections are empty.

## Chat Examples
- "assign load L1001 to the nearest available driver"
- "eta from Los Angeles to San Francisco"
- "status of driver D2"
- "notify customer for load L1001: running 30 minutes late"

## Project Structure

- backend/
  - app/
    - main.py                # FastAPI app setup, routers, WebSocket, startup seeding
    - config.py              # Environment config
    - db.py                  # Mongo (Motor) client
    - schemas.py             # Pydantic models
    - models.py              # DB helper functions
    - seed.py                # Sample data seeding
    - routers/
      - endpoints.py         # REST endpoints
      - chat.py              # /api/chat dispatcher endpoint
    - dispatcher/
      - ai_dispatcher.py     # Rule-based parser and orchestration
      - hos_rules.py         # HOS checks
      - routing.py           # Distance + ETA
      - notifier.py          # Notification + broadcast hooks
    - realtime/
      - websocket.py         # WebSocket connection manager
  - requirements.txt
  - Dockerfile
- frontend/
  - src/ (React components and services)
  - Dockerfile
  - Tailwind + Vite config
- docker-compose.yml
- .env.example

## Hours of Service (simplified)
- Max 11 hours driving in a 14-hour on-duty window
- 30-minute break required after 8 hours of driving
- Reset if off-duty >= 10 hours

These are simplified checks to illustrate logic; adapt to your operation.

## Notes
- No external map API is required. Routing uses Haversine for distance and a fixed average speed for ETA.
- Notifications are broadcast over WebSocket and logged; integrate SMS/Email providers as needed.

## Development without Docker (optional)

Backend:
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

Ensure MongoDB is running locally at MONGO_URI.
