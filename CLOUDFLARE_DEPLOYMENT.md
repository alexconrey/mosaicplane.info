# Cloudflare Workers Deployment Guide

This guide covers deploying the MOSAIC Plane Info application to Cloudflare Workers using static assets hosting.

## Prerequisites

1. **Cloudflare Account**: Sign up at [cloudflare.com](https://cloudflare.com)
2. **Domain**: Add your domain to Cloudflare (optional, can use workers.dev subdomain)
3. **Wrangler CLI**: Install globally or use the local dev dependency

## Setup Steps

### 1. Install Dependencies

```bash
cd src/ui
npm install
```

### 2. Cloudflare Authentication

```bash
# Login to Cloudflare
npx wrangler login

# Or set API token
export CLOUDFLARE_API_TOKEN=your-api-token
```

### 3. Configure Environment Variables

Edit `src/ui/wrangler.toml` and update:

- `name`: Your worker name
- `routes`: Your custom domain routes (if using custom domain)
- Environment variables in `[vars]` section

### 4. Set API Backend URL

For production deployment, you need to update the API URL in `wrangler.toml`:

```toml
[env.production.vars]
ENVIRONMENT = "production"
API_BASE_URL = "https://your-actual-api-domain.com"
```

Or set it as a build-time environment variable:

```bash
# For production build
VITE_API_BASE_URL=https://your-api-domain.com npm run deploy:prod
```

## Deployment Commands

### Development
```bash
# Deploy to development environment
npm run deploy:dev

# Or using Makefile
make cf-deploy-dev
```

### Production
```bash
# Deploy to production environment
npm run deploy:prod

# Or using Makefile
make cf-deploy-prod
```

## Local Development with Cloudflare

```bash
# Start local Cloudflare Workers development server
npm run cf:dev

# View logs from deployed worker
npm run cf:tail
```

## Configuration Details

### wrangler.toml Structure

```toml
name = "mosaicplane-info-ui"
main = "src/index.js"
compatibility_date = "2024-12-12"

[build]
command = "npm run build"

[assets]
bucket = "./dist"

[vars]
ENVIRONMENT = "production"
```

### Worker Script Features

- **SPA Routing**: Serves `index.html` for all unmatched routes
- **API Proxying**: Forwards `/api/*` requests to Django backend
- **CORS Handling**: Adds appropriate CORS headers
- **Security Headers**: Adds security headers to HTML responses
- **Static Assets**: Serves built Vite assets efficiently

## Custom Domain Setup

1. Add your domain to Cloudflare
2. Update `wrangler.toml` with routes:

```toml
routes = [
  { pattern = "mosaicplane.info/*", zone_name = "mosaicplane.info" }
]
```

3. Deploy with custom routes:

```bash
npm run deploy:prod
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_BASE_URL` | Django API backend URL | Yes |
| `ENVIRONMENT` | Environment name | No |

## Monitoring & Logs

```bash
# View real-time logs
npx wrangler tail --env production

# View worker analytics in Cloudflare dashboard
# Navigate to Workers & Pages > Your Worker > Analytics
```

## Troubleshooting

### Common Issues

1. **404 on refresh**: Ensure SPA routing is properly configured in Worker script
2. **API calls failing**: Verify `API_BASE_URL` environment variable is set
3. **CORS errors**: Check CORS headers in Worker script
4. **Build failures**: Ensure `npm run build` works locally first

### Debug Commands

```bash
# Test local build
npm run build
npm run preview

# Check Cloudflare account
npx wrangler whoami

# Validate wrangler.toml
npx wrangler validate
```

## Performance Optimizations

The deployment includes several optimizations:

- **Asset chunking**: Separates vendor and app code
- **Minification**: Removes console logs and debug code
- **Compression**: Cloudflare automatically compresses assets
- **Edge caching**: Static assets cached at edge locations globally

## Security Features

- **CSP Headers**: Content Security Policy for XSS protection
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, etc.
- **HTTPS Only**: All traffic served over HTTPS
- **Edge security**: Cloudflare's security features (DDoS protection, WAF)

## Cost Considerations

- **Workers**: Free tier includes 100,000 requests/day
- **Static Assets**: Included in Workers pricing
- **Bandwidth**: Cloudflare provides unlimited bandwidth
- **Custom Domains**: Free with Cloudflare account

For production usage, consider the Workers Paid plan for higher limits and advanced features.