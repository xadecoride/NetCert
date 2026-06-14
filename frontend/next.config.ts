import type { NextConfig } from "next";

const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080/api/v1";
const baseUrl = apiUrl.replace(/\/api\/v1$/, "");

const nextConfig: NextConfig = {
  output: "standalone",
  experimental: {
    serverActions: {
      bodySizeLimit: "2mb",
    },
  },
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${apiUrl}/:path*`,
      },
      {
        source: "/ws/:path*",
        destination: `${baseUrl}/ws/:path*`,
      },
    ];
  },
};

export default nextConfig;
