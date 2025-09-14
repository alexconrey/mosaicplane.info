# Cloudflare Workers Asset Caching Optimization

This document explains the caching strategy implemented to reduce uncached bandwidth usage and improve website performance.

## Overview

The caching system addresses the issue where 50%+ of bandwidth was uncached by implementing:
- Aggressive caching for static assets with content hashes
- Smart caching for API responses based on data volatility
- Proper MIME type handling
- Performance and security headers

## Implementation

### 1. Static Asset Caching (`functions/_middleware.js`)

**Content-hashed assets** (`/assets/` folder):
- **Cache Duration**: 1 year (31,536,000 seconds)
- **Strategy**: `public, max-age=31536000, immutable`
- **Reason**: Build-time generated files with content hashes never change

**JavaScript/CSS files**:
- **Cache Duration**: 1 week with revalidation
- **Strategy**: `public, max-age=604800, stale-while-revalidate=86400`

**Images and Fonts**:
- **Cache Duration**: 30 days with revalidation
- **Strategy**: `public, max-age=2592000, stale-while-revalidate=604800`

### 2. Optimized Asset Serving (`functions/assets/[[path]].js`)

- Dedicated handler for `/assets/` routes
- Immutable caching for content-hashed files
- Proper MIME type setting for better compression

### 3. API Response Caching (`functions/api/[[path]].js`)

**Individual aircraft details** (`/api/v1/aircraft/{id}/`):
- **Cache Duration**: 1 hour with 30-minute stale revalidation
- **Reason**: Aircraft data changes infrequently

**List endpoints** (`/api/v1/aircraft/`, `/api/v1/manufacturers/`):
- **Cache Duration**: 30 minutes with 15-minute stale revalidation
- **Reason**: Lists may change more frequently than individual records

**Other GET endpoints**:
- **Cache Duration**: 5 minutes with 1-minute stale revalidation
- **Reason**: Conservative caching for unknown data patterns

### 4. Build Optimization (`vite.config.js`)

- **Content-based file naming**: `[name]-[hash].js/css/etc`
- **Asset organization**: Images in `/images/`, fonts in `/fonts/`
- **Chunk splitting**: Vendor libraries separated for better caching
- **Compression**: Terser minification with console removal

## Expected Results

### Before Optimization
- 50%+ uncached bandwidth
- Repeated asset downloads
- Poor cache hit ratios

### After Optimization
- 90%+ cached asset requests
- Immutable assets never re-downloaded
- API responses cached appropriately
- Reduced bandwidth costs
- Improved page load times

## Cache Hierarchy

1. **Immutable assets** (1 year): Content-hashed JS/CSS/images
2. **Semi-static assets** (30 days): Images, fonts without hashes
3. **Dynamic data** (1 hour): Individual aircraft details
4. **List data** (30 minutes): Aircraft/manufacturer lists
5. **Real-time data** (5 minutes): Other API endpoints
6. **HTML pages** (5 minutes): Main application pages

## Security Headers

Additional headers added for security:
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`

## Performance Headers

- `X-DNS-Prefetch-Control: on`
- `Vary: Accept-Encoding`

## Deployment

The caching system is automatically deployed with the Cloudflare Workers application:

```bash
# Deploy to development
npm run deploy:dev

# Deploy to production
npm run deploy:prod
```

## Monitoring

Monitor cache performance via:
1. Cloudflare Analytics dashboard
2. Cache hit ratio metrics
3. Bandwidth usage reports
4. Core Web Vitals improvements