# MOSAIC Plane Info

A comprehensive web application for exploring aircraft eligibility under the FAA's new MOSAIC (Modernization of Special Airworthiness Certificates) regulations, effective October 22, 2025.

## Overview

The MOSAIC regulations represent a revolutionary change in general aviation, expanding sport pilot privileges to approximately 70% of the existing GA fleet. This application helps pilots understand which aircraft they can legally operate under different certificate levels and what endorsements may be required.

## Key Features

### 🛩️ Aircraft Database
- **120+ Aircraft**: Comprehensive database including specific variants (Cessna 150A-150M, 172A-172S, 182A-182T)
- **Detailed Specifications**: Performance data, engine configurations, certification dates
- **MOSAIC Compliance**: Automatic calculation based on stall speeds and certification requirements
- **Data Verification**: All aircraft specifications verified against POHs and type certificates

### 📊 Eligibility Analysis
- **Sport Pilot Eligible**: Aircraft with stall speeds ≤59 knots CAS
- **MOSAIC LSA Compliant**: Aircraft with stall speeds ≤61 knots CAS
- **Endorsement Requirements**: Clear indicators for retractable gear and variable pitch propeller
- **Certification Date Logic**: Distinguishes between legacy and new aircraft requirements

### 🎯 User Interface
- **Interactive Aircraft Table**: Searchable, filterable database with detailed aircraft pages
- **Mobile-Responsive Design**: Optimized for all devices with dark/light mode support
- **Educational Content**: Comprehensive MOSAIC explanations and regulatory context
- **Community Corrections**: User-friendly system for submitting data corrections

## Technology Stack

- **Frontend**: Vue.js 3 with modern responsive design
- **Backend**: Django REST Framework with comprehensive API
- **Database**: SQLite with verified MOSAIC-accurate data
- **Documentation**: Swagger/OpenAPI integration

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
- **Application**: http://localhost:3000
- **API Documentation**: http://localhost:8000/api/docs/
- **Django Admin**: http://localhost:8000/admin

## Production Deployment

### Cloudflare Workers (Recommended)

This application is optimized for deployment on Cloudflare Workers with static assets hosting.

```bash
# Deploy to production
make cf-deploy-prod

# Or deploy to development
make cf-deploy-dev
```

See [CLOUDFLARE_DEPLOYMENT.md](./CLOUDFLARE_DEPLOYMENT.md) for detailed deployment instructions.

### Docker Deployment

```bash
# Build and start with Docker Compose
make docker-up

# Stop services
make docker-down
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
- `GET /api/aircraft/` - List all aircraft with filtering
- `GET /api/aircraft/{id}/` - Detailed aircraft specifications
- `GET /api/manufacturers/` - Aircraft manufacturers
- `GET /api/engines/` - Engine specifications
- `POST /api/corrections/` - Submit data corrections

### Filtering Options
- `?pilot_certificate=sport|private` - Filter by pilot requirements
- `?manufacturer=<name>` - Filter by manufacturer
- `?seating=2|4` - Filter by seating capacity
- `?search=<term>` - Search aircraft models and manufacturers

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