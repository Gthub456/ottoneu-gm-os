"use client";

import { useEffect, useState } from "react";
import RosterTable, { League } from "../../components/RosterTable";

export default function RosterPage() {
  const [data, setData] = useState<League | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchRoster() {
      try {
        const baseUrl = process.env.NEXT_PUBLIC_API_URL;
        const res = await fetch(`${baseUrl}/roster`);
        if (!res.ok) {
          throw new Error(`Failed to fetch roster: ${res.statusText}`);
        }
        const json = await res.json();
        setData(json.league as League);
      } catch (err: any) {
        console.error(err);
        setError(err.message || "Unknown error");
      } finally {
        setLoading(false);
      }
    }
    fetchRoster();
  }, []);

  if (loading) {
    return <p>Loading roster...</p>;
  }
  if (error) {
    return <p className="text-red-400">{error}</p>;
  }
  if (!data) {
    return <p>No roster found.  Connect your Ottoneu account or run the seed script.</p>;
  }
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Roster</h1>
      <RosterTable league={data} />
    </div>
  );
}