# Claude

You are a world class UI/UX designer, and before that - you were a highly accomplished software engineer with a focus in backend programming.

Follow the `PLAN.md` document for the overall plan of the project.

## Project Status
- ✅ **Django API Complete**: Comprehensive REST API with enhanced serializers and community features
- ✅ **MOSAIC-Accurate Database**: 173 aircraft, 40 manufacturers, comprehensive data sources
- ✅ **Vue.js UI Complete**: Modern responsive interface with detailed aircraft pages
- ✅ **Community Features**: User correction system with administrative review tools
- ✅ **Data Verification**: All aircraft specifications verified against official sources
- ✅ **Comprehensive Testing**: 53+ tests covering E2E, accessibility, legal compliance, and best practices
- ✅ **CI/CD Pipeline**: Automated testing and deployment via GitHub Actions
- ✅ **Modern Tech Stack**: Python 3.12, Django 5.1.11, Node.js 24, Vue.js 3.5.27
- ✅ **Production Security**: Comprehensive security headers, CSP, API authentication, HTTPS enforcement
- ✅ **SEO Optimization**: Meta tags, Open Graph, structured data, dynamic sitemaps, performance optimization
- ✅ **Code Quality**: MyPy type checking, pre-commit hooks, automated formatting and linting
- ✅ **Asset Caching**: Cloudflare Workers with intelligent caching strategy reducing 50%+ uncached bandwidth

## Critical MOSAIC Constraints for UI Design
**These must be clearly visible to end users:**

### Sport Pilot Eligibility (October 2025+)
- **Stall Speed Limit**: ≤59 knots CAS for sport pilot operation
- **Passenger Limit**: Sport pilots limited to 1 passenger (regardless of aircraft seating)
- **Endorsements Available**: Retractable gear & variable pitch propeller with logbook endorsement

### MOSAIC LSA Certification Limits
- **Stall Speed Limit**: ≤61 knots CAS for MOSAIC LSA certification
- **Seating**: Up to 4 seats allowed in LSA aircraft
- **Weight**: No maximum takeoff weight limit under MOSAIC
- **Certification Date Requirement**: New aircraft must be certified after July 24, 2026 to qualify as MOSAIC LSA
- **Legacy Aircraft**: All existing aircraft certified before July 24, 2026 are eligible if they meet performance requirements
- **Effective Dates**: 
  - Sport pilot privileges: October 22, 2025
  - New aircraft certification: July 24, 2026

### Major Aircraft Now Eligible
- **Cessna 172** (early models) - Revolutionary change!
- **70% of GA fleet** now accessible to sport pilots
- Cessna 150/152, Piper Cherokee 140, J-3 Cub, and more

## UI Design Principles (Implemented)
1. **✅ Transparency**: All MOSAIC constraints clearly displayed with eligibility legend
2. **✅ Educational**: Comprehensive help system and contextual explanations 
3. **✅ Filtering**: Robust filtering by pilot certificate, manufacturer, seating with dynamic year ranges
4. **✅ Mobile-First**: Fully responsive design with mobile-optimized layouts
5. **✅ Accessibility**: ARIA labels, keyboard navigation, dropdown explanations
6. **✅ Data Integrity**: Community correction system with verification sources
7. **✅ Professional UI Components**: vue-slider-component@next for Vue 3 compatibility

## Key Features Completed
### Aircraft Detail Pages
- **Unified Aircraft Information Section**: Redesigned full-width section combining performance specifications and certification data in an efficient 2x2 grid layout
- **MOSAIC Eligibility Summary**: Prominent header displaying eligibility badge and key specifications (stall speed, MTOW, seating) with enhanced typography
- **Complete V-Speed Data**: All critical aviation speeds (Vx, Vy, Vs0, Vg, Vfe, Vno, Vne) organized in logical groupings with user corrections
- **Optimized Layout**: Four distinct information sections - Flight Envelope, Performance Speeds, Aircraft Limits, and Certification - distributed evenly in a space-efficient grid
- **Engine Information**: Detailed engine specifications, fuel types, horsepower
- **MOSAIC Impact Analysis**: Regulation explanations specific to each aircraft
- **Data Sources**: Verification documentation (POHs, type certificates)
- **Community Corrections**: User-friendly form for submitting data corrections

### Aircraft Database Interface  
- **Interactive Table**: Clickable aircraft names linking to detail pages
- **Eligibility Legend**: Accessible dropdown explaining all badge meanings
- **Advanced Filtering**: Sport pilot, private pilot, manufacturer, seating filters
- **Dynamic Year Range Filtering**: Certification year slider with API-driven min/max values
- **Professional Slider Components**: vue-slider-component@next with accessibility features
- **Search Functionality**: By aircraft model and manufacturer name
- **Navigation Menu**: Accessible dropdown with MOSAIC info and About pages
- **Responsive Design**: Mobile-first with desktop enhancements

### Manufacturer Features
- **Manufacturer Detail Pages**: Dedicated pages for each manufacturer with aircraft listings
- **Manufacturer Logos**: Professional logo display with responsive sizing and error handling
- **Manufacturing Status**: Clear indicators for active vs. historic manufacturers
- **Aircraft Count**: Dynamic count of available aircraft models per manufacturer
- **Mobile V-Speed Display**: Compact Vx and Vy speeds in manufacturer aircraft tables

### Data Management Tools
- **Population Command**: `python manage.py update_mosaic_aircraft`
- **Unified Seed Command**: `python manage.py seed_exact` - consolidated command with exactly 120 aircraft variants
- **Correction Review**: `python manage.py review_corrections --list`
- **Admin Interface**: Full Django admin for data management

## Production Deployment
### Multi-Platform Deployment Architecture
- **Heroku Container Registry**: Django API at https://api.mosaicplane.info
  - **Build Command**: `heroku container:push --app api-mosaicplane-info web`
  - Production-ready gunicorn WSGI server with CORS support
  - Environment variable configuration for scalability
  - Automatic database migrations and seeding on deployment
  
- **Docker Compose Development**: Full-stack local development
  - **Command**: `docker compose up`
  - **Access**: http://localhost:8080 (nginx reverse proxy)
  - **Architecture**: nginx → UI (Vue.js) + API (Django) containers
  - **Features**: Hot reload, volume mounts, platform-specific builds
  
- **Container Features**:
  - Multi-platform Docker builds with automatic platform detection
  - Docker-specific Vite configuration excluding Cloudflare Workers plugin
  - Django API serving endpoints at `/v1/aircraft/`, `/v1/manufacturers/`
  - CORS configuration for cross-origin requests
  - Non-root user execution for security
  - Runtime environment variable configuration
  - Platform-agnostic builds resolving Rosetta/workerd binary compatibility issues

## Current UI Features
### Enhanced Year Range Filtering
- **Dynamic Range Calculation**: Year ranges computed from actual aircraft certification dates in database
- **API-Driven Defaults**: Returns null when API is unavailable, preventing hardcoded fallbacks
- **Professional Slider**: vue-slider-component@next with tooltip positioning and accessibility
- **Clean Interface**: Removed redundant year labels while maintaining visual clarity

### Navigation & Accessibility
- **Header Navigation**: Theme toggle positioned left of accessible menu dropdown
- **Skip Links**: Keyboard navigation support with skip-to-content functionality
- **ARIA Compliance**: Comprehensive screen reader support with proper roles and labels
- **Mobile Optimization**: Responsive design with touch-friendly interactions

### V-Speed Integration
- **Complete Aviation Data**: All critical V-speeds (Vx, Vy, Vs0, Vg, Vfe, Vno, Vne) in aircraft database
- **Database Schema**: 7 new V-speed fields added to Aircraft model with proper validation
- **UI Integration**: V-speeds displayed in aircraft detail pages, comparison views, and manufacturer tables
- **Community Corrections**: V-speed data included in user correction system for accuracy

### Manufacturer Logo System
- **Dynamic Logo Display**: Manufacturer logos from URL fields with graceful fallback to placeholders
- **Responsive Sizing**: Logo containers adapt to screen sizes (200px → 150px → 120px)
- **Error Handling**: Automatic fallback to placeholder when logo URLs fail to load
- **Professional Styling**: Clean bordered containers with shadows and proper image scaling

### Docker Platform Compatibility
- **Multi-Architecture Support**: Builds for both ARM64 (Apple Silicon) and AMD64 architectures
- **Cloudflare Workers Isolation**: Separate Docker Vite config prevents workerd binary conflicts
- **Platform-Agnostic Deployment**: Automatic platform detection without explicit constraints

## Recent System Improvements

### Deployment Configuration Optimization (December 2024)
- **SPA Routing Fix**: Implemented proper Cloudflare Workers SPA support via `wrangler.toml` configuration
- **Multi-Domain Support**: Added aircraftdb.info domain support with API CORS and branding integration
- **Build System Fixes**: Resolved terser `drop_unused` option error and django-stubs version compatibility
- **Documentation Enhancement**: Created comprehensive DEPLOYMENT_NOTES.md with lessons learned
- **V-Speed Data Continuation**: Added 3 more aircraft (Mooney M20C, CTLS, Cherokee 140) to seed script

### Aircraft Information Section Redesign (September 2024)
- **Unified Layout**: Consolidated performance specifications and certification information into a single full-width "Aircraft Information" section
- **2x2 Grid Design**: Organized data into four logical sections:
  - **Flight Envelope**: Critical safety speeds (Vs1, Vs0, Va, Vno, Vne, Top Speed)
  - **Performance Speeds**: Operational speeds (Vx, Vy, Vg, Vfe, Cruise Speed)  
  - **Aircraft Limits**: Weight and seating constraints (MTOW, Seating Capacity)
  - **Certification**: Regulatory compliance (Certification Date, MOSAIC/Sport Pilot Eligibility)
- **Enhanced Typography**: Increased font size and weight for key specifications in MOSAIC eligibility summary
- **Space Optimization**: Implemented auto-sizing grid rows and reduced padding to eliminate excessive whitespace
- **Mobile Responsive**: Grid collapses to single column on screens ≤768px while maintaining readability
- **Preserved Functionality**: All EditableField components and user correction features maintained throughout redesign
- **Airspeed Gauge**: Temporarily disabled for future re-implementation

### Technical Implementation
- **CSS Grid Layout**: `aircraft-info-grid` with `grid-template-columns: 1fr 1fr` and `grid-template-rows: auto auto`
- **Component Structure**: Individual `info-section` cards with consistent styling and spacing
- **Responsive Design**: Automatic stacking on mobile devices with optimized touch interactions
- **Performance**: Efficient rendering with conditional V-speed display based on data availability

## Testing Infrastructure
### Comprehensive Test Coverage (53+ Tests)
- **E2E Tests**: 28 tests covering all user flows with 100% pass rate
- **Legal Compliance**: 5 tests for disclaimer functionality and footer links
- **Accessibility**: 10 tests for WCAG compliance, keyboard navigation, screen reader support
- **Best Practices**: 10 tests for SEO, performance, semantic HTML, security
- **Docker Integration**: All tests run in consistent Docker containers using Playwright v1.55.0

### CI/CD Pipeline
- **Pull Request Testing**: Automated Django, Vue.js, and E2E testing on every PR
- **Security Scanning**: Python (Bandit) and Node.js (npm audit) vulnerability detection
- **Development Deployment**: Automated Cloudflare Workers deployment on develop branch
- **Production Deployment**: Heroku API + Cloudflare UI deployment on main branch with health checks

### Database Status
- **Aircraft**: 173 models across 40 manufacturers
- **V-Speed Completion**: 40/173 aircraft (23.1%) have complete v-speed data
- **Expansion Plan**: TODO_AIRCRAFT_MANUFACTURERS.md and TODO_AIRCRAFT_IMPORTS.md created
- **VSPEED_TODO.md**: Detailed backfill plan for remaining 133 aircraft

## Reference Material
* MOSAIC Final Issuance PDF: https://www.faa.gov/newsroom/MOSAIC_Final_Rule_Issuance.pdf
* API Documentation: http://localhost:8000/api/docs/
* Live Application: http://localhost:3000 (Vue.js frontend)
* Admin Interface: http://localhost:8000/admin (Django admin)
* Production: https://mosaicplane.info (UI) + https://api.mosaicplane.info (API)