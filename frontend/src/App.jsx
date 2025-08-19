import React, { useState } from "react";
import ChatBox from "./components/ChatBox";
import AssignmentsPage from "./components/AssignmentsPage";
import Dashboard from "./components/Dashboard";
import { ToastContainer } from "./components/Toast";

export default function App() {
  const [tab, setTab] = useState("chat");
  return (
    <div className="min-h-screen flex flex-col">
      <header className="p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-semibold">Logistics Dispatcher</h1>
        </div>
      </header>
      <main className="flex-1">
        {tab === "dashboard" ? (
          <Dashboard />
        ) : tab === "chat" ? (
          <ChatBox />
        ) : (
          <AssignmentsPage />
        )}
      </main>
      <footer className="p-4 text-xs text-gray-500 text-center">
        Demo system for dispatching, routing, and notifications
      </footer>
      {/* Bottom navigation to avoid top overlay interference */}
      <div className="fixed top-3 left-1/2 -translate-x-1/2 z-40">
        <div className="flex gap-2">
          <button
            onClick={() => setTab("dashboard")}
            className={`px-4 py-1 rounded-full ${
              tab === "dashboard"
                ? "bg-indigo-600 text-white"
                : "bg-transparent"
            }`}
          >
            Dashboard
          </button>
          <button
            onClick={() => setTab("chat")}
            className={`px-4 py-1 rounded-full ${
              tab === "chat" ? "bg-indigo-600 text-white" : "bg-transparent"
            }`}
          >
            Chat
          </button>
          <button
            onClick={() => setTab("assignments")}
            className={`px-4 py-1 rounded-full ${
              tab === "assignments"
                ? "bg-indigo-600 text-white"
                : "bg-transparent"
            }`}
          >
            Assignments
          </button>
        </div>
      </div>
      <ToastContainer />
    </div>
  );
}
