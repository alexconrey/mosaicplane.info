# Claude

You are a world class UI/UX designer, and before that - you were a highly accomplished software engineer with a focus in backend programming.

Follow the `PLAN.md` document for the overall plan of the project.

## Project Status
- ✅ **Django API Complete**: Comprehensive REST API with enhanced serializers and community features
- ✅ **MOSAIC-Accurate Database**: 25 verified aircraft, 17 engines, comprehensive data sources
- ✅ **Vue.js UI Complete**: Modern responsive interface with detailed aircraft pages
- ✅ **Community Features**: User correction system with administrative review tools
- ✅ **Data Verification**: All aircraft specifications verified against official sources

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
3. **✅ Filtering**: Robust filtering by pilot certificate, manufacturer, seating
4. **✅ Mobile-First**: Fully responsive design with mobile-optimized layouts
5. **✅ Accessibility**: ARIA labels, keyboard navigation, dropdown explanations
6. **✅ Data Integrity**: Community correction system with verification sources

## Key Features Completed
### Aircraft Detail Pages
- **Comprehensive Specifications**: Performance data with contextual explanations
- **Engine Information**: Detailed engine specifications, fuel types, horsepower
- **MOSAIC Impact Analysis**: Regulation explanations specific to each aircraft
- **Data Sources**: Verification documentation (POHs, type certificates)
- **Community Corrections**: User-friendly form for submitting data corrections

### Aircraft Database Interface  
- **Interactive Table**: Clickable aircraft names linking to detail pages
- **Eligibility Legend**: Accessible dropdown explaining all badge meanings
- **Advanced Filtering**: Sport pilot, private pilot, manufacturer, seating filters
- **Search Functionality**: By aircraft model and manufacturer name
- **Responsive Design**: Mobile-first with desktop enhancements

### Data Management Tools
- **Population Command**: `python manage.py update_mosaic_aircraft`
- **Unified Seed Command**: `python manage.py seed_exact` - consolidated command with exactly 120 aircraft variants
- **Correction Review**: `python manage.py review_corrections --list`
- **Admin Interface**: Full Django admin for data management

## Production Deployment
### Heroku-Compliant Docker Container
- **Build Command**: `make docker-prod`
- **Architecture**: Multi-stage build with Django serving everything on configurable port
- **Runtime Environment Detection**: Smart API endpoint routing based on deployment context
- **Container Features**:
  - Django server handling both API and static assets
  - Built Vue.js static assets integrated into Django
  - Automatic database migrations and seeding
  - Uses `$PORT` environment variable (Heroku requirement)
  - Non-root user execution for security
  - Runtime environment variable configuration
  - Compatible with both Docker and Heroku container registry
- **Deployment Options**:
  - **Docker**: `docker run -p 8000:8000 mosaicplane-info:production`
  - **Heroku**: Uses `Procfile` with gunicorn for production WSGI server

## Reference Material
* MOSAIC Final Issuance PDF: https://www.faa.gov/newsroom/MOSAIC_Final_Rule_Issuance.pdf
* API Documentation: http://localhost:8000/api/docs/
* Live Application: http://localhost:3000 (Vue.js frontend)
* Admin Interface: http://localhost:8000/admin (Django admin)