import Link from "next/link";

export default function Home() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Ottoneu GM Terminal</h1>
      <p>
        Welcome to your fantasy baseball command center.  This app connects to
        your Ottoneu league, ingests player news, projections and Statcast
        data, and surfaces actionable insights to help you win your league.
      </p>
      <p>
        To get started, navigate to the <Link href="/roster" className="text-blue-400 underline">Roster</Link> page or connect your Ottoneu account using the connector page.
      </p>
    </div>
  );
}