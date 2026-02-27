/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Opt into the new app directory (Next.js 15 uses it by default)
  experimental: {
    appDir: true,
  },
};

module.exports = nextConfig;