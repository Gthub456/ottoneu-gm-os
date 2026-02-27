"use client";

import React from "react";
import {
  useReactTable,
  ColumnDef,
  getCoreRowModel,
  flexRender,
} from "@tanstack/react-table";

// Define TypeScript types for roster entries returned by the API.
export interface Player {
  id: number;
  name: string;
  position?: string | null;
  ottoneu_player_id?: number | null;
  fangraphs_id?: number | null;
  mlbam_id?: number | null;
}

export interface RosterEntry {
  id: number;
  salary?: number | null;
  acquired?: string | null;
  player: Player;
}

export interface Team {
  id: number;
  name?: string | null;
  cap_space?: number | null;
  roster_entries: RosterEntry[];
}

export interface League {
  id: number;
  ottoneu_league_id: number;
  name?: string | null;
  teams: Team[];
}

interface Props {
  league: League;
}

export default function RosterTable({ league }: Props) {
  // Flatten roster entries for all teams (in a future iteration you might show multiple teams)
  const rows = React.useMemo(() => {
    const entries: RosterEntry[] = [];
    league.teams.forEach((team) => {
      team.roster_entries.forEach((entry) => entries.push(entry));
    });
    return entries;
  }, [league]);

  const columns = React.useMemo<ColumnDef<RosterEntry>[]>(
    () => [
      {
        header: "Player",
        accessorFn: (row) => row.player.name,
        cell: (info) => info.getValue(),
      },
      {
        header: "Position",
        accessorFn: (row) => row.player.position ?? "",
        cell: (info) => info.getValue(),
      },
      {
        header: "Salary ($)",
        accessorFn: (row) => row.salary ?? 0,
        cell: (info) => info.getValue(),
      },
    ],
    []
  );

  const table = useReactTable({
    data: rows,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-sm divide-y divide-gray-700">
        <thead className="bg-gray-800">
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th
                  key={header.id}
                  className="px-4 py-2 text-left font-medium text-gray-300 uppercase tracking-wider"
                >
                  {header.isPlaceholder
                    ? null
                    : flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody className="divide-y divide-gray-700">
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id} className="hover:bg-gray-800">
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id} className="px-4 py-2 whitespace-nowrap">
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}