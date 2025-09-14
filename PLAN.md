# Plan

Our plan is to create a new website, mosaicplane.info. The process for understanding the new FAA MOSAIC regulations are a pain.

We'll be creating 2 apps within the `src/` directory:
* ui
* api

The `ui` will be a Vue based application, running the latest available versions of Vue.js packages.

The `api` will be a Django based application, written in Python, which constructs the backend that the `ui` will query for data.

## ✅ Completed: Comprehensive Database & API Implementation

### Enhanced Data Model (Implemented)
* **Aircraft**
    * Manufacturer (Foreign Key)
    * Model Name
    * Clean Stall Speed (Vs1) - with MOSAIC validation (≤61 knots)
    * Top Speed & Maneuvering Speed (Va)
    * Maximum Takeoff Weight (no MOSAIC limit)
    * Seating Capacity (1-4 seats under MOSAIC)
    * Retractable Landing Gear & Variable Pitch Propeller (booleans)
    * Certification Date (when aircraft was first certificated)
    * **Verification Source** - POH references, type certificates, documentation
    * **Engine Configurations** - ManyToMany relationship with Engine model
    * MOSAIC Compliant (auto-calculated: ≤61 knots stall + certification date logic)
    * Sport Pilot Eligible (auto-calculated: ≤59 knots stall)
    * Timestamps (created/updated)

* **Engine** (New Model)
    * Manufacturer & Model designation
    * Horsepower & Displacement (liters)
    * Fuel Type (Avgas/Mogas/Diesel/Electric)
    * Engine Type (Piston/Turboprop/Electric)
    * Fuel Injection (boolean)
    * Timestamps (created/updated)

* **Manufacturer**
    * Name (unique)
    * Is Currently Manufacturing Aircraft (boolean)
    * Aircraft Count (calculated)
    * Timestamps (created/updated)

* **AircraftCorrection** (Community Contributions)
    * Aircraft (Foreign Key)
    * Field Name & Current/Suggested Values
    * Reason & Source Documentation
    * Submitter Information (optional)
    * Status (Pending/Approved/Rejected/Implemented)
    * Admin Notes & Review Timestamps

### API Features (Implemented)
* **RESTful Endpoints**: Full CRUD operations for Aircraft, Engines, Manufacturers
* **Advanced Filtering**: By pilot certificate, manufacturer, MOSAIC compliance, gear type
* **Search**: By aircraft model and manufacturer name
* **Ordering**: By all speed/performance metrics
* **Enhanced Serializers**: Include engine configurations and verification sources
* **Community Corrections API**: Submit and manage user corrections
* **Swagger Documentation**: Interactive API docs at `/api/docs/`
* **Admin Interface**: Django admin for data management

### Database (Implemented)
* **SQLite**: Development database with verified MOSAIC-accurate data
* **Comprehensive Data**: 120 aircraft including specific variants (Cessna 150A-150M, 172A-172S, 182A-182T), 19+ manufacturers, 11+ engines
* **Data Verification**: All aircraft include source documentation (POHs, type certificates)
* **Engine Database**: Continental, Lycoming, Rotax engines with specifications
* **MOSAIC Validation**: Automatic compliance calculation based on stall speeds and certification dates

### Management Tools (Implemented)
* **Data Population**: `python manage.py update_mosaic_aircraft` - populate database with verified data
* **Unified Seed Command**: `python manage.py seed_exact` - consolidated command with exactly 120 aircraft variants including specific Cessna 150/172/182 models
* **Correction Review**: `python manage.py review_corrections` - full CLI for managing user corrections
  * List pending corrections: `--list`
  * Review specific correction: `--show ID`
  * Approve/reject corrections: `--approve ID --notes "reason"`

## ✅ Completed: Modern Vue.js UI Implementation

### Core UI Features (Implemented)
* **Aircraft Database Table**: Responsive aircraft listing with filtering and search
* **Detailed Aircraft Pages**: Comprehensive specifications with clickable links from main table
* **MOSAIC Compliance Interface**: Clear visual indicators and educational content
* **Community Corrections**: User-friendly form for submitting data corrections
* **Dark/Light Mode**: Automatic theme switching with CSS variables

### Critical User Interface Requirements (Implemented)

1. **✅ Sport Pilot Badge System**
   - Clear visual indicators for sport pilot eligibility (≤59 knots)
   - Warning badges for aircraft requiring private pilot (59-61 knots)
   - Endorsement indicators (retractable gear, variable pitch prop)
   - **Accessibility Feature**: Eligibility legend dropdown with detailed explanations

2. **✅ MOSAIC Information Panel**
   - Effective dates (October 22, 2025 for sport pilot privileges, July 24, 2026 for new aircraft certification)
   - Certification date requirements (legacy vs. new aircraft)
   - Stall speed limits clearly explained
   - Passenger limitations for sport pilots (1 passenger max)
   - Comprehensive about page with legal disclaimers

3. **✅ Aircraft Detail Pages**
   - **Performance Specifications**: All speeds, weights, seating with context
   - **Engine Information**: Detailed engine specs, horsepower, fuel types
   - **Certification Details**: Dates and MOSAIC compliance explanations
   - **Data Verification**: Source documentation for transparency
   - **MOSAIC Impact**: Regulation explanations specific to each aircraft

4. **✅ Educational Components**
   - MOSAIC impact explanation (70% of GA fleet now accessible)
   - Major newly eligible aircraft highlighted (Cessna 172!)
   - Difference between MOSAIC LSA and sport pilot eligibility
   - Interactive eligibility guide with badge explanations

5. **✅ Advanced Filtering & Search**
   - By pilot certificate requirements (Sport/Private/Not Eligible)
   - By manufacturer with aircraft counts
   - By seating capacity (2 vs 4 seats)
   - Dynamic certification year range filtering with vue-slider-component@next
   - Search by aircraft model and manufacturer name
   - Pagination for large datasets

6. **✅ Community Features**
   - User correction submission system
   - Source documentation tracking
   - Administrative review workflow
   - Transparent data verification process

### User Experience Goals (Achieved)
- **✅ Mobile-First Design**: Fully responsive across all devices with mobile-optimized layouts
- **✅ Performance Focused**: Fast loading with efficient API calls and pagination
- **✅ Educational**: Comprehensive MOSAIC explanations and contextual help
- **✅ Transparent**: All limitations, requirements, and data sources clearly visible
- **✅ Accessible**: Legend dropdowns, proper ARIA labels, keyboard navigation, skip links
- **✅ Interactive**: Clickable aircraft links, correction forms, theme switching, navigation menu
- **✅ Professional Components**: Modern slider components with tooltip positioning
- **✅ API-Driven Filtering**: Dynamic year ranges based on actual certification data

# Technical Criteria
* Database will be SQLite (changed from PostgreSQL for simplicity)
* Ensure that the `ui` is composed with Vue.js
* Ensure that the `api` is composed with Python using the Django framework
* API documentation available via Swagger UI
* All MOSAIC constraints must be user-visible in UI

## Production Deployment Options

### ✅ Cloudflare Workers (Static Assets)
* **UI Deployment**: Vue.js assets hosted on Cloudflare Workers
* **API Endpoint**: Runtime detection of production vs development API base URLs
* **Commands**: 
  - Development: `make cf-deploy-dev`
  - Production: `make cf-deploy-prod`
* **Configuration**: `src/ui/wrangler.toml` with environment-specific variables
* **URL**: https://mosaicplane-info-ui.ajcblz2019.workers.dev/

### ✅ Heroku Container Registry
* **API Deployment**: Django API deployed to Heroku using container registry
* **Build Command**: `heroku container:push --app api-mosaicplane-info web`
* **Features**: 
  - Automatic database migrations and data seeding on startup
  - Production-ready with gunicorn WSGI server
  - Environment variable configuration via Heroku config
  - CORS enabled for cross-origin requests from frontend
* **URL**: https://api.mosaicplane.info
* **Architecture**: Single Django container serving API endpoints at `/v1/aircraft/`, `/v1/manufacturers/`, etc.

### ✅ Docker Compose Development
* **Command**: `docker compose up`
* **Architecture**: Multi-service setup with nginx reverse proxy
  - **nginx**: Main entry point on port 8080, handles routing
  - **api**: Django container (internal port 8000)
  - **ui**: Vue.js development server (internal port 3000)
* **Routing**:
  - `http://localhost:8080/` → Vue.js UI
  - `http://localhost:8080/api/` → Django API (nginx strips `/api/` prefix)
* **Features**:
  - Live development with hot reload
  - Multi-platform Docker builds with automatic platform detection
  - Docker-specific Vite configuration excluding Cloudflare Workers plugin
  - Volume mounts for source code changes
  - CORS configuration for cross-service communication
  - Platform compatibility fixes for Apple Silicon and Intel architectures

## Reference Material
* MOSAIC Final Issuance PDF: https://www.faa.gov/newsroom/MOSAIC_Final_Rule_Issuance.pdf
* API Documentation: http://localhost:8000/api/docs/
