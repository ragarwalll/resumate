
const { next } = require('@million/lint');
const createNextIntlPlugin = require('next-intl/plugin');

const withNextIntl = createNextIntlPlugin('./src/config/i18n.ts');
const withBundleAnalyzer = require('@next/bundle-analyzer')({
    enabled: process.env.ANALYZE === 'true',
})
/** @type {import('next').NextConfig} */
const nextConfig = {};
const millionConfig = {
    rsc: true,
    enabled: true,
    production: {
        enabled: true,
    },
}

module.exports = withBundleAnalyzer(next(millionConfig)(withNextIntl(nextConfig)));