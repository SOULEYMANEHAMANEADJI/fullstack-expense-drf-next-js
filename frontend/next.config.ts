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
    // Exclude backup files from linting
    dirs: ['app'],
  },
  // Exclude backup files from build
  pageExtensions: ['tsx', 'ts', 'jsx', 'js'],
  // Exclude backup files
  webpack: (config, { isServer }) => {
    config.module.rules.push({
      test: /\.(tsx|ts)$/,
      exclude: /(page_backup_old|page_old)\.tsx$/,
    });
    return config;
  },
};

export default nextConfig;
