import "./globals.css";
import NavBar from "../components/NavBar";

export const metadata = {
  title: "Ottoneu GM Operating System",
  description: "A fantasy baseball GM toolkit",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <NavBar />
        <main className="p-4 max-w-7xl mx-auto">{children}</main>
      </body>
    </html>
  );
}