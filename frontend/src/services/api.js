const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";
const WEBSOCKET_URL =
  import.meta.env.VITE_WEBSOCKET_URL || "ws://localhost:8000/ws";

export async function chat(message) {
  const res = await fetch(`${BACKEND_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error("Chat request failed");
  return res.json();
}

export async function assignDriver(payload) {
  const res = await fetch(`${BACKEND_URL}/api/assign_driver`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Assign driver failed");
  return res.json();
}

export async function routeEta(origin, destination) {
  const res = await fetch(`${BACKEND_URL}/api/route_eta`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ origin, destination }),
  });
  if (!res.ok) throw new Error("ETA failed");
  return res.json();
}

export async function getDriverStatus(driverId) {
  const res = await fetch(`${BACKEND_URL}/api/drivers/${driverId}/status`);
  if (!res.ok) throw new Error("Driver status failed");
  return res.json();
}

export function connectSocket(onMessage) {
  const ws = new WebSocket(WEBSOCKET_URL);
  ws.onmessage = (evt) => {
    try {
      const data = JSON.parse(evt.data);
      onMessage?.(data);
    } catch (e) {
      console.error("WS parse error", e);
    }
  };
  return ws;
}

export async function listDrivers() {
  const res = await fetch(`${BACKEND_URL}/api/drivers`);
  if (!res.ok) throw new Error("Drivers fetch failed");
  return res.json();
}

export async function listLoads() {
  const res = await fetch(`${BACKEND_URL}/api/loads`);
  if (!res.ok) throw new Error("Loads fetch failed");
  return res.json();
}

export async function listAssignments() {
  const res = await fetch(`${BACKEND_URL}/api/assignments`);
  if (!res.ok) throw new Error("Assignments fetch failed");
  return res.json();
}

export async function updateAssignmentStatus(assignmentId, status) {
  const res = await fetch(`${BACKEND_URL}/api/assignments/status`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ assignment_id: assignmentId, status }),
  });
  if (!res.ok) throw new Error("Update assignment failed");
  return res.json();
}
