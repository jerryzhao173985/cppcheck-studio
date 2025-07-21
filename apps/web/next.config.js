/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@cppcheck-studio/core', '@cppcheck-studio/ui'],
  experimental: {
    serverActions: true,
  },
  webpack: (config) => {
    // Handle monaco-editor web workers
    config.module.rules.push({
      test: /\.worker\.(js|ts)$/,
      use: { loader: 'worker-loader' },
    });
    
    return config;
  },
}

module.exports = nextConfig