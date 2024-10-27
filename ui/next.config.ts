import { NextConfig } from "next";
import { next } from "@million/lint";
import createNextIntlPlugin from "next-intl/plugin";

const withNextIntl = createNextIntlPlugin("./src/config/i18n.ts");
const withBundleAnalyzer = require("@next/bundle-analyzer")({
  enabled: process.env.ANALYZE === "true",
});

const nextConfig: NextConfig = {
  bundlePagesRouterDependencies: true,
  experimental: {
    reactCompiler: true,
  },
};
const millionConfig = {
  rsc: true,
  enabled: true,
};

/**
The function will handle the configuration of the Next.js application.
It will be based on the phase and the default configuration.
 */
export default (phase: string) => {
  const isProduction =
    phase.includes("production") ||
    process.env.NODE_ENV.toLowerCase() === "production";

  if (isProduction) return withNextIntl(nextConfig);

  return withBundleAnalyzer(next(millionConfig)(withNextIntl(nextConfig)));
};
