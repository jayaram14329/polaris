import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "POLARIS | Polar Knowledge & Outreach Intelligence System (SIH26063 - MoES/NCPOR)",
  description: "Integrated Polar Science Outreach, Knowledge Repository, Station GIS and Media Dissemination Portal developed for the Ministry of Earth Sciences and NCPOR.",
  keywords: ["POLARIS", "NCPOR", "MoES", "Antarctica", "Arctic", "Maitri", "Bharati", "Himadri", "Polar Science", "RAG AI", "SIH26063"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <head>
        <link
          rel="stylesheet"
          href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
          integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
          crossOrigin=""
        />
        <script
          src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
          integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
          crossOrigin=""
          async
        ></script>
      </head>
      <body className="min-h-screen bg-[#060d1f] text-slate-100 antialiased selection:bg-cyan-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
