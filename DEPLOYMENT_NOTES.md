# Deployment Configuration Notes

This document captures important configuration details and lessons learned for the MosaicPlane.info deployment.

## Single Page Application (SPA) Routing

### ✅ Correct Solution: Wrangler Configuration
The proper way to handle SPA routing in Cloudflare Workers is through the `wrangler.toml` configuration:

```toml
[assets]
directory = "./dist"
not_found_handling = "single-page-application"
```

### ❌ Incorrect Approaches (Tried and Failed)
1. **_redirects file with `/* /index.html 200`** - Causes infinite loop errors
2. **Complex _redirects with exclusions** - Still problematic with Cloudflare Workers
3. **Middleware-based SPA handling** - Unnecessary when proper wrangler config exists

### Key Learning
Cloudflare Workers has built-in SPA support that automatically serves `index.html` for non-file routes when `not_found_handling = "single-page-application"` is configured. This eliminates the need for custom redirect rules or middleware logic.

## Multi-Domain Support

### API Configuration
To support additional domains like `aircraftdb.info`, update:

**File:** `src/api/mosaicplane/settings.py`
```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    'api.mosaicplane.info',
    'api-mosaicplane-info.herokuapp.com',
    'api.aircraftdb.info',  # Added for multi-domain support
]

CORS_ALLOWED_ORIGINS = [
    "https://mosaicplane.info",
    "https://www.mosaicplane.info",
    "https://aircraftdb.info",      # Added for multi-domain support
    "https://www.aircraftdb.info",  # Added for multi-domain support
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Branding Configuration
The application already supports dynamic branding through `src/ui/functions/branding.js` which automatically serves different metadata and styling based on the hostname.

## Build Configuration Issues

### Terser Configuration
**Problem:** `drop_unused` option removed in terser 5.x
**File:** `src/ui/vite.config.js`
**Solution:** Remove the unsupported option:

```javascript
terserOptions: {
  compress: {
    drop_console: true,
    drop_debugger: true,
    dead_code: true
    // Note: drop_unused was removed in terser 5.x
  },
  mangle: {
    safari10: true
  }
}
```

### Django Dependencies
**Problem:** `django-stubs==5.1.4` version not available
**File:** `src/api/requirements.txt`
**Solution:** Update to available version:

```
django-stubs==5.2.5
```

**Compatibility:** django-stubs 5.2.5 supports Django 5.1.x, Python 3.10-3.13, and mypy 1.13-1.18.

## Development vs Production Configuration

### Database Seed Script Approach
For v-speed data and other aircraft specifications, use the database seed script approach:
- **File:** `src/api/aircraft/management/commands/seed.py`
- **Benefits:** Version controlled, reproducible across environments, systematic documentation
- **Command:** `python manage.py seed` (for development/testing)

### Environment-Specific Settings
The application supports environment-specific configuration through:
- Environment variables (`ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`)
- Wrangler environment configurations (`[env.development]`, `[env.production]`)
- Dynamic API base URL resolution in the UI

## Architecture Summary

```
Frontend (Cloudflare Workers)
├── Static Assets (cached with content hashing)
├── SPA Routing (wrangler.toml configuration)
├── Dynamic Branding (hostname-based)
├── Security Headers (_middleware.js)
└── API Proxy (functions/api/[[path]].js)

Backend (Heroku)
├── Django 5.1.11 REST API
├── Multi-domain CORS support
├── Type checking (mypy + django-stubs)
└── Database seeding system
```

## Key Deployment Commands

### UI Deployment
```bash
cd src/ui
npm run build
npm run deploy:prod  # or deploy:dev for development
```

### API Deployment
```bash
# Automatic via GitHub Actions on main branch push
# Manual: Heroku container deployment
```

## Testing Configuration
- **E2E Tests:** Run in Docker containers via `npm run test:e2e:docker`
- **API Tests:** Include authentication and CORS validation
- **Build Tests:** Validate terser configuration and asset generation

## Security Considerations
- **API Authentication:** Required for write operations, read operations public
- **CORS:** Configured for specific domains only
- **CSP Headers:** Comprehensive Content Security Policy via middleware
- **HTTPS Enforcement:** Strict Transport Security headers applied

---

**Last Updated:** December 2024
**Key Contributors:** System configuration and deployment optimization