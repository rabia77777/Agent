import React, { useEffect, useMemo, useState } from "react";
import { listAssignments, listDrivers, listLoads } from "../services/api";

function StatCard({ label, value }) {
  return (
    <div className="p-4 rounded border border-gray-200 dark:border-gray-700">
      <div className="text-sm text-gray-500">{label}</div>
      <div className="text-2xl font-semibold">{value}</div>
    </div>
  );
}

export default function Dashboard() {
  const [drivers, setDrivers] = useState([]);
  const [loads, setLoads] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const run = async () => {
      setLoading(true);
      try {
        const [d, l, a] = await Promise.all([
          listDrivers(),
          listLoads(),
          listAssignments(),
        ]);
        setDrivers(d.drivers || []);
        setLoads(l.loads || []);
        setAssignments(a.assignments || []);
      } finally {
        setLoading(false);
      }
    };
    run();
  }, []);

  const stats = useMemo(() => {
    const availableDrivers = drivers.filter(
      (d) => d.status === "available"
    ).length;
    const inTransit = assignments.filter(
      (a) => a.status === "in_transit"
    ).length;
    const delivered = assignments.filter(
      (a) => a.status === "delivered"
    ).length;
    const unassignedLoads = loads.filter(
      (l) => l.status === "unassigned"
    ).length;
    return { availableDrivers, inTransit, delivered, unassignedLoads };
  }, [drivers, loads, assignments]);

  if (loading) return <div className="p-6">Loading…</div>;

  return (
    <div className="max-w-6xl mx-auto p-4 space-y-6">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard label="Available Drivers" value={stats.availableDrivers} />
        <StatCard label="In Transit" value={stats.inTransit} />
        <StatCard label="Delivered" value={stats.delivered} />
        <StatCard label="Unassigned Loads" value={stats.unassignedLoads} />
      </div>

      <div className="p-4 rounded border border-gray-200 dark:border-gray-700">
        <div className="font-semibold mb-3">Recent Activity</div>
        <div className="text-sm text-gray-500">
          Interact via Chat or Assignments to see updates in real time.
        </div>
        <ul className="mt-2 list-disc list-inside text-sm">
          {assignments
            .slice(-5)
            .reverse()
            .map((a) => (
              <li key={a._id}>
                {a._id}: {a.driver_id} → {a.load_id} • {a.status}
              </li>
            ))}
          {assignments.length === 0 && (
            <li>No activity yet. Try assigning a load.</li>
          )}
        </ul>
      </div>
    </div>
  );
}
