import React, { useEffect, useRef, useState } from "react";
import VoiceRecorder from "./VoiceRecorder";
import { chat, connectSocket } from "../services/api";
import { useToast } from "./Toast";

export default function ChatBox() {
  const [messages, setMessages] = useState([
    {
      role: "system",
      text: 'Welcome to the Dispatcher. Try: "assign load L1001 to nearest", "eta from Toronto to Winnipeg".',
    },
  ]);
  const [input, setInput] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    const ws = connectSocket((event) => {
      setMessages((prev) => [
        ...prev,
        {
          role: "event",
          text:
            event?.event === "assignment"
              ? `Assignment update: ${event?.payload?.driver_id} -> ${event?.payload?.load_id}`
              : JSON.stringify(event),
        },
      ]);
    });
    return () => ws.close();
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const { notify } = useToast();

  const handleSend = async () => {
    if (!input.trim()) return;
    const userMessage = input;
    setMessages((prev) => [...prev, { role: "user", text: userMessage }]);
    setInput("");
    try {
      const res = await chat(userMessage);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: formatAssistant(res) },
      ]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "Error: " + e.message },
      ]);
      notify(e.message, "error");
    }
  };

  const formatAssistant = (res) => {
    const { action, data } = res;
    if (action === "route_eta") {
      if (data.error) return `Error: ${data.error}`;
      return `Distance: ${data.distance_miles} mi, ETA: ${data.eta_hours} h`;
    }
    if (action === "assign_driver") {
      if (data.error)
        return `Error: ${data.error}${
          data.hos_reason ? " (" + data.hos_reason + ")" : ""
        }`;
      const msg = `Assigned ${data.driver._id} to ${
        data.load._id
      }. ETA: ${data.assignment.eta_hours.toFixed(2)} h`;
      notify(`Assigned ${data.driver._id} to ${data.load._id}`, "success");
      return msg;
    }
    if (action === "get_driver_status") {
      const d = data?.driver;
      if (!d) return "Driver not found.";
      const loc = d.current_location || {};
      const onDuty = d.on_duty_start
        ? new Date(d.on_duty_start).toLocaleString()
        : "—";
      const lastBreak = d.last_break_start
        ? new Date(d.last_break_start).toLocaleString()
        : "—";
      const assigned = d.assigned_load_id || "—";
      return `Driver ${d._id} — ${d.name}
Status: ${d.status}
Location: ${loc.city || "—"}${
        loc.lat !== undefined && loc.lon !== undefined
          ? ` (${loc.lat}, ${loc.lon})`
          : ""
      }
Hours driven today: ${d.hours_driven_today}
On duty since: ${onDuty}
Last break: ${lastBreak}
Assigned load: ${assigned}`;
    }
    if (action === "notify") {
      return `Notification sent.`;
    }
    return `Unknown command.`;
  };

  return (
    <div className="flex flex-col h-full w-full max-w-3xl mx-auto">
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={
              m.role === "user"
                ? "text-right"
                : m.role === "assistant"
                ? "text-left"
                : "text-center text-xs text-gray-500"
            }
          >
            <span
              className={`inline-block px-3 py-2 rounded whitespace-pre-wrap ${
                m.role === "user"
                  ? "bg-indigo-600 text-white"
                  : m.role === "assistant"
                  ? "bg-gray-200 dark:bg-gray-800"
                  : ""
              }`}
            >
              {m.text}
            </span>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
      <div className="p-4 border-t border-gray-200 dark:border-gray-700 flex gap-2 items-center">
        <input
          className="flex-1 px-3 py-2 rounded border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800"
          placeholder="Type a command..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <VoiceRecorder onResult={(t) => setInput(t)} />
        <button
          onClick={handleSend}
          className="px-3 py-2 rounded bg-indigo-600 text-white hover:bg-indigo-700"
        >
          Send
        </button>
      </div>
    </div>
  );
}
