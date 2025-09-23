# MOSAIC Plane Info

A comprehensive web application for exploring aircraft eligibility under the FAA's new MOSAIC (Modernization of Special Airworthiness Certificates) regulations, effective October 22, 2025.

## Overview

The MOSAIC regulations represent a revolutionary change in general aviation, expanding sport pilot privileges to approximately 70% of the existing GA fleet. This application helps pilots understand which aircraft they can legally operate under different certificate levels and what endorsements may be required.

## Key Features

### 🛩️ Aircraft Database
- **190+ Aircraft**: Comprehensive database including specific variants (Cessna 150A-150M, 172A-172S, 182A-182T)
- **Detailed Specifications**: Performance data, engine-type specific configurations, certification dates
- **MOSAIC Compliance**: Automatic calculation based on stall speeds and certification requirements
- **Data Verification**: All aircraft specifications verified against POHs and type certificates

### 📊 Eligibility Analysis
- **Sport Pilot Eligible**: Aircraft with stall speeds ≤59 knots CAS
- **MOSAIC LSA Compliant**: Aircraft with stall speeds ≤61 knots CAS
- **Endorsement Requirements**: Clear indicators for retractable gear and variable pitch propeller
- **Certification Date Logic**: Distinguishes between legacy and new aircraft requirements

### 🎯 User Interface
- **Interactive Aircraft Table**: Searchable, filterable database with detailed aircraft pages
- **Dynamic Year Range Filtering**: Professional slider component with API-driven certification date ranges
- **Navigation Menu**: Accessible dropdown with MOSAIC information and About pages
- **Mobile-Responsive Design**: Optimized for all devices with dark/light mode support
- **Educational Content**: Comprehensive MOSAIC explanations and regulatory context
- **Community Corrections**: User-friendly system for submitting data corrections
- **Accessibility Features**: Skip links, ARIA labels, keyboard navigation support
- **Multi-Domain Support**: Dynamic branding for multiple domains (mosaicplane.info, aircraftdb.info)
- **SPA Routing**: Proper client-side routing with Cloudflare Workers integration

## Technology Stack

- **Frontend**: Vue.js 3 with Composition API and vue-slider-component@next
- **Backend**: Django REST Framework with comprehensive API
- **Database**: SQLite with verified MOSAIC-accurate data
- **Documentation**: Swagger/OpenAPI integration
- **Containerization**: Docker with multi-platform support and platform-specific configurations
- **Development**: Vite with Cloudflare Workers integration and Docker-specific configs

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Virtual environment (recommended)

### Development Setup

#### Using Makefile (Recommended)
```bash
# Install all dependencies
make install

# Start both API and UI development servers
make dev
```

#### Manual Setup

**Backend Setup:**
```bash
cd src/api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_exact  # Load aircraft database
python manage.py runserver
```

**Frontend Setup:**
```bash
cd src/ui
npm install
npm run dev
```

### Access Points

#### Development (Individual Services)
- **Application**: http://localhost:3000
- **API Documentation**: http://localhost:8000/api/docs/
- **Django Admin**: http://localhost:8000/admin

#### Docker Compose (Recommended for Local Development)
```bash
# Start all services with nginx reverse proxy
docker compose up

# Access the full application
# Application: http://localhost:8080
```

## Production Deployment

### Multi-Platform Architecture

#### Heroku Container Registry (API Backend)
```bash
# Deploy Django API to Heroku
heroku container:push --app api-mosaicplane-info web
heroku container:release --app api-mosaicplane-info web

# Production API: https://api.mosaicplane.info
```

#### Cloudflare Workers (Frontend)
```bash
# Deploy Vue.js frontend to Cloudflare Workers
make cf-deploy-prod

# Production UI: https://mosaicplane.info
```

#### Docker Compose (Local Development)
```bash
# Full-stack development environment with nginx reverse proxy
docker compose up

# Access: http://localhost:8080
# - UI requests → nginx → ui container (Vue.js dev server)
# - API requests → nginx → api container (Django)

# Features:
# - Multi-platform builds (Apple Silicon & Intel)
# - Docker-specific Vite config avoiding Cloudflare Workers conflicts
# - Hot reload development with volume mounts
```

## Database Management

### Seed Database
```bash
python manage.py seed_exact
```
Loads exactly 120 aircraft with verified specifications including all Cessna variants.

### Review Community Corrections
```bash
python manage.py review_corrections --list
python manage.py review_corrections --show <ID>
python manage.py review_corrections --approve <ID> --notes "Review notes"
```

## Configuration & Deployment

For detailed deployment configuration, troubleshooting, and lessons learned, see:
📋 **[DEPLOYMENT_NOTES.md](./DEPLOYMENT_NOTES.md)**

Key topics covered:
- SPA routing configuration (`wrangler.toml`)
- Multi-domain support setup
- Build configuration fixes (terser, django-stubs)
- Development vs production environments
- Security and CORS configuration

## MOSAIC Regulation Summary

### Effective Dates
- **October 22, 2025**: Sport pilot privilege expansion
- **July 24, 2026**: New aircraft MOSAIC LSA certification requirement

### Sport Pilot Eligibility (≤59 knots stall speed)
- ✅ 1 passenger maximum
- ✅ Retractable gear with endorsement
- ✅ Variable pitch propeller with endorsement
- ✅ Up to 4 seats (passenger limit still applies)

### MOSAIC LSA Certification (≤61 knots stall speed)
- ✅ No maximum takeoff weight limit
- ✅ Up to 4 seats
- ✅ Legacy aircraft eligible if meeting performance requirements
- ✅ New aircraft must be certified after July 24, 2026

### Revolutionary Changes
- **Cessna 172** early models now sport pilot eligible
- **70% of GA fleet** accessible to sport pilots
- **Major aircraft included**: Cessna 150/152, Piper Cherokee 140, J-3 Cub, and more

## API Endpoints

### Core Resources
- `GET /v1/aircraft/` - List all aircraft with filtering
- `GET /v1/aircraft/{id}/` - Detailed aircraft specifications
- `GET /v1/manufacturers/` - Aircraft manufacturers
- `GET /v1/engines/` - Engine specifications
- `POST /v1/corrections/` - Submit data corrections

**Note**: In production, API endpoints are accessible via:
- **Development**: Direct API calls to `localhost:8000/v1/...`
- **Docker Compose**: Proxied through nginx at `localhost:8080/api/v1/...`
- **Production**: Cross-origin requests to `https://api.mosaicplane.info/v1/...`

### Filtering Options
- `?pilot_certificate=sport|private` - Filter by pilot requirements
- `?manufacturer=<name>` - Filter by manufacturer
- `?seating=2|4` - Filter by seating capacity
- `?search=<term>` - Search aircraft models and manufacturers
- **Dynamic Year Ranges**: UI automatically calculates min/max certification years from API data
- **Professional Sliders**: Vue 3 compatible slider components with tooltip positioning

## Data Sources & Verification

All aircraft data is verified against official sources:
- **Pilot Operating Handbooks (POHs)**
- **FAA Type Certificate Data Sheets**
- **Manufacturer specifications**
- **MOSAIC Final Rule documentation**

## Contributing

### Data Corrections
Users can submit corrections through the web interface. All submissions are reviewed by administrators before implementation.

### Development
1. Fork the repository
2. Create a feature branch
3. Submit pull request with detailed description

## Legal Disclaimer

This application is for informational purposes only. Always consult current FAA regulations, CFRs, and your designated pilot examiner or flight instructor for official guidance. Aircraft eligibility may change based on individual aircraft configuration and certification.

## Support

For issues, questions, or data corrections:
- Use the in-application correction system
- Check the comprehensive help documentation
- Review the MOSAIC Final Rule: https://www.faa.gov/newsroom/MOSAIC_Final_Rule_Issuance.pdf

## License

Open source project - see LICENSE file for details.