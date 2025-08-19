import React, { useEffect, useMemo, useState } from "react";
import {
  listAssignments,
  listDrivers,
  listLoads,
  updateAssignmentStatus,
  connectSocket,
  assignDriver,
} from "../services/api";
import { useToast } from "./Toast";

export default function AssignmentsPage() {
  const [drivers, setDrivers] = useState([]);
  const [loads, setLoads] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { notify } = useToast();

  const driverById = useMemo(
    () => Object.fromEntries(drivers.map((d) => [d._id, d])),
    [drivers]
  );
  const loadById = useMemo(
    () => Object.fromEntries(loads.map((l) => [l._id, l])),
    [loads]
  );

  useEffect(() => {
    let ws;
    const init = async () => {
      try {
        setLoading(true);
        const [d, l, a] = await Promise.all([
          listDrivers(),
          listLoads(),
          listAssignments(),
        ]);
        setDrivers(d.drivers || []);
        setLoads(l.loads || []);
        setAssignments(a.assignments || []);
        ws = connectSocket((evt) => {
          if (
            evt.event === "assignment" ||
            evt.event === "assignment_updated"
          ) {
            listAssignments().then((a2) =>
              setAssignments(a2.assignments || [])
            );
            const p = evt.payload || {};
            if (p.driver_id && p.load_id) {
              notify(`Assigned ${p.driver_id} to ${p.load_id}`, "success");
            }
          }
        });
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };
    init();
    return () => ws && ws.close();
  }, []);

  const handleStatus = async (assignmentId, next) => {
    try {
      await updateAssignmentStatus(assignmentId, next);
      notify(`Assignment ${assignmentId} -> ${next}`, "success");
      const a = await listAssignments();
      setAssignments(a.assignments || []);
    } catch (e) {
      setError(e.message);
      notify(e.message, "error");
    }
  };

  const handleAssignNearest = async (loadId) => {
    try {
      await assignDriver({ load_id: loadId });
      notify(`Assigned nearest driver to ${loadId}`, "success");
      const [l, a] = await Promise.all([listLoads(), listAssignments()]);
      setLoads(l.loads || []);
      setAssignments(a.assignments || []);
    } catch (e) {
      setError(e.message);
      notify(e.message, "error");
    }
  };

  if (loading) return <div className="p-6">Loading…</div>;
  if (error) return <div className="p-6 text-red-600">Error: {error}</div>;

  return (
    <div className="max-w-6xl mx-auto p-4 space-y-4">
      <section>
        <h2 className="text-lg font-semibold mb-2">Current Assignments</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="text-left border-b border-gray-200 dark:border-gray-700">
                <th className="py-2 pr-4">Assignment</th>
                <th className="py-2 pr-4">Driver</th>
                <th className="py-2 pr-4">Load</th>
                <th className="py-2 pr-4">Route</th>
                <th className="py-2 pr-4">ETA (h)</th>
                <th className="py-2 pr-4">Distance (mi)</th>
                <th className="py-2 pr-4">Status</th>
                <th className="py-2 pr-4">Actions</th>
              </tr>
            </thead>
            <tbody>
              {assignments.length === 0 && (
                <tr>
                  <td className="py-3" colSpan={8}>
                    No assignments yet.
                  </td>
                </tr>
              )}
              {assignments.map((a) => {
                const d = driverById[a.driver_id];
                const l = loadById[a.load_id];
                return (
                  <tr
                    key={a._id}
                    className="border-b border-gray-100 dark:border-gray-800"
                  >
                    <td className="py-2 pr-4 font-mono">{a._id}</td>
                    <td className="py-2 pr-4">
                      {d ? (
                        <div>
                          <div className="font-medium">
                            {d.name} ({d._id})
                          </div>
                          <div className="text-xs text-gray-500">
                            {d.current_location?.city || "—"} · {d.status}
                          </div>
                        </div>
                      ) : (
                        a.driver_id
                      )}
                    </td>
                    <td className="py-2 pr-4">
                      {l ? (
                        <div>
                          <div className="font-medium">{l._id}</div>
                          <div className="text-xs text-gray-500">
                            {l.status}
                          </div>
                        </div>
                      ) : (
                        a.load_id
                      )}
                    </td>
                    <td className="py-2 pr-4">
                      {l ? (
                        <div className="text-xs">
                          <div>Pickup: {l.pickup?.city}</div>
                          <div>Dropoff: {l.dropoff?.city}</div>
                        </div>
                      ) : (
                        "—"
                      )}
                    </td>
                    <td className="py-2 pr-4">
                      {Number(a.eta_hours).toFixed(2)}
                    </td>
                    <td className="py-2 pr-4">
                      {Number(a.distance_miles).toFixed(0)}
                    </td>
                    <td className="py-2 pr-4">
                      <span
                        className={`px-2 py-1 rounded text-xs ${
                          a.status === "assigned"
                            ? "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100"
                            : a.status === "in_transit"
                            ? "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-100"
                            : a.status === "delivered"
                            ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100"
                            : "bg-gray-200 dark:bg-gray-800"
                        }`}
                      >
                        {a.status}
                      </span>
                    </td>
                    <td className="py-2 pr-4 space-x-2">
                      {a.status === "assigned" && (
                        <button
                          onClick={() => handleStatus(a._id, "in_transit")}
                          className="px-2 py-1 rounded bg-indigo-600 text-white"
                        >
                          Start
                        </button>
                      )}
                      {a.status !== "delivered" && (
                        <button
                          onClick={() => handleStatus(a._id, "delivered")}
                          className="px-2 py-1 rounded bg-green-600 text-white"
                        >
                          Mark Delivered
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h3 className="font-semibold mb-2">Drivers</h3>
          <div className="space-y-2">
            {drivers.map((d) => (
              <div
                key={d._id}
                className="p-3 rounded border border-gray-200 dark:border-gray-700"
              >
                <div className="font-medium">
                  {d.name}{" "}
                  <span className="text-xs text-gray-500">({d._id})</span>
                </div>
                <div className="text-xs text-gray-500">
                  {d.current_location?.city || "—"} · {d.status}
                </div>
              </div>
            ))}
          </div>
        </div>
        <div>
          <h3 className="font-semibold mb-2">Loads</h3>
          <div className="space-y-2">
            {loads.map((l) => (
              <div
                key={l._id}
                className="p-3 rounded border border-gray-200 dark:border-gray-700"
              >
                <div className="font-medium">{l._id}</div>
                <div className="text-xs text-gray-500">
                  {l.pickup?.city} → {l.dropoff?.city} · {l.status}
                </div>
                {l.status === "unassigned" && (
                  <div className="mt-2">
                    <button
                      onClick={() => handleAssignNearest(l._id)}
                      className="px-2 py-1 rounded bg-indigo-600 text-white"
                    >
                      Assign nearest driver
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
