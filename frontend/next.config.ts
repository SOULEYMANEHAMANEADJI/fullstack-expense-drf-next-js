import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  typescript: {
    // Ignore TypeScript errors during build in CI
    ignoreBuildErrors: false,
  },
  eslint: {
    // Ignore ESLint errors during build in CI
    ignoreDuringBuilds: false,
  },
};

export default nextConfig;
