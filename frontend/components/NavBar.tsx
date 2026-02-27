"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems: { href: string; label: string }[] = [
  { href: "/", label: "Home" },
  { href: "/roster", label: "Roster" },
  { href: "/free-agents", label: "Free Agents" },
  { href: "/trades", label: "Trade Machine" },
  { href: "/market", label: "Market" },
  { href: "/player-lab", label: "Player Lab" },
  { href: "/data-health", label: "Data Health" },
];

export default function NavBar() {
  const pathname = usePathname();
  return (
    <nav className="bg-gray-800 border-b border-gray-700 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-12 items-center justify-between">
          <div className="flex items-center space-x-4">
            {navItems.map((item) => {
              const active = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    active
                      ? "bg-gray-900 text-white"
                      : "text-gray-300 hover:bg-gray-700 hover:text-white"
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
}