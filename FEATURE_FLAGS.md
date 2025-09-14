# Feature Flags System

The MosaicPlane.Info application includes a comprehensive feature flag system that allows you to control UI features without deploying new code.

## Overview

Feature flags enable you to:
- Enable/disable features dynamically
- Control ad display while waiting for approval
- Toggle beta features for testing
- Implement maintenance mode
- Track all changes with audit history

## Available Feature Flags

| Flag Key | Display Name | Default | Description |
|----------|--------------|---------|-------------|
| `ads_enabled` | Google AdSense Ads | Disabled | Enable Google AdSense ads throughout the application |
| `amp_ads_enabled` | AMP Ads | Disabled | Enable AMP ads on aircraft detail pages |
| `analytics_enabled` | Google Analytics | Enabled | Enable Google Analytics tracking |
| `beta_features` | Beta Features | Disabled | Enable beta features for testing |
| `maintenance_mode` | Maintenance Mode | Disabled | Show maintenance notice to users |

## API Endpoints

### Simple Format (Frontend Consumption)
```bash
GET /v1/feature-flags/
```
Returns: `{"ads_enabled": true, "amp_ads_enabled": false, ...}`

### Detailed Format
```bash
GET /v1/feature-flags/detailed/
```
Returns full objects with descriptions and display names.

### Individual Flag
```bash
GET /v1/feature-flags/{flag_key}/
```

## Command Line Management

The `feature_flag` management command provides comprehensive CLI control with immediate effect:

### List All Flags
```bash
python manage.py feature_flag list
python manage.py feature_flag list --enabled-only
python manage.py feature_flag list --disabled-only
```

### Show Flag Details
```bash
python manage.py feature_flag show ads_enabled
python manage.py feature_flag show ads_enabled --history
```

### Enable/Disable Flags (Immediate Effect)
```bash
# Enable single flag
python manage.py feature_flag enable ads_enabled --reason "Google approved"

# Enable multiple flags
python manage.py feature_flag enable ads_enabled amp_ads_enabled --reason "Launch ads"

# Disable flags
python manage.py feature_flag disable beta_features --reason "End beta test"
```

### Toggle Flags (Immediate Effect)
```bash
python manage.py feature_flag toggle maintenance_mode --reason "Emergency maintenance"
```

### Create New Flags
```bash
python manage.py feature_flag create new_feature_key \
  --description "Description of new feature" \
  --enabled
```

### Delete Flags (Immediate Effect)
```bash
python manage.py feature_flag delete old_feature_key --confirm
```


## Docker Usage

When using Docker Compose:

```bash
# List flags
docker compose exec api python manage.py feature_flag list

# Enable ads when Google approves
docker compose exec api python manage.py feature_flag enable ads_enabled amp_ads_enabled \
  --reason "Google AdSense approved"

# Emergency disable
docker compose exec api python manage.py feature_flag disable ads_enabled \
  --reason "Emergency disable due to policy violation"

# Toggle maintenance mode
docker compose exec api python manage.py feature_flag toggle maintenance_mode \
  --reason "System maintenance window"
```

## Frontend Integration

### Vue.js Composable
```javascript
import { useFeatureFlags } from '@/composables/useFeatureFlags'

// In setup()
const { isFeatureEnabled } = useFeatureFlags()
const adsEnabled = isFeatureEnabled('ads_enabled')
const ampAdsEnabled = isFeatureEnabled('amp_ads_enabled')

// In template
<div v-if="adsEnabled && ampAdsEnabled">
  <amp-ad>...</amp-ad>
</div>
```

### Multiple Flags
```javascript
const { getFeatures } = useFeatureFlags()
const { ads_enabled, beta_features, maintenance_mode } = getFeatures(
  'ads_enabled', 'beta_features', 'maintenance_mode'
)
```

## Django Admin Interface

1. Navigate to `/admin/feature_flags/featureflag/`
2. View all flags with status indicators
3. Edit individual flags
4. Use bulk actions to enable/disable multiple flags
5. View change history

## Performance

- API responses serve fresh data directly from database
- No caching layer - changes are immediately visible
- Lightweight database queries for fast response times

## Audit Trail

All changes are tracked in the `FeatureFlagHistory` model:
- Previous and new state
- User who made the change
- Timestamp
- Reason for change

View history:
```bash
python manage.py feature_flag show ads_enabled --history
```

## Production Workflow Example

### Enabling Ads After Google Approval
```bash
# Check current status
docker compose exec api python manage.py feature_flag list

# Enable both ad flags
docker compose exec api python manage.py feature_flag enable ads_enabled amp_ads_enabled \
  --reason "Google AdSense application approved - ticket #1234"

# Verify change
curl https://api.mosaicplane.info/v1/feature-flags/ | jq .
```

### Emergency Disable
```bash
# Immediate disable if issues arise
docker compose exec api python manage.py feature_flag disable ads_enabled \
  --reason "Emergency disable - policy violation reported"
```

### Maintenance Mode
```bash
# Enable maintenance mode
docker compose exec api python manage.py feature_flag enable maintenance_mode \
  --reason "Scheduled database migration - 2 hour window"

# Disable after maintenance
docker compose exec api python manage.py feature_flag disable maintenance_mode \
  --reason "Maintenance complete - all systems operational"
```

## Best Practices

1. **Always provide meaningful reasons** when changing flags
2. **Use descriptive flag keys** that clearly indicate their purpose
3. **Test flag changes in development** before production
4. **Monitor application after flag changes** for unexpected behavior
5. **Document flag dependencies** (e.g., amp_ads_enabled requires ads_enabled)
6. **Use maintenance_mode sparingly** and communicate with users
7. **Keep audit trail** for compliance and debugging

## Security

- Feature flags are read-only from the frontend
- Only authenticated Django admin users can modify flags
- CLI changes are tracked with 'CLI' as the modifier
- No sensitive information should be stored in flag descriptions

## Troubleshooting

### Changes Not Appearing
All changes are immediate since there's no caching. If changes don't appear:
```bash
# Verify the change in the database
docker compose exec api python manage.py feature_flag list
```

### Database Issues
If flags aren't persisting, check database connectivity:
```bash
docker compose exec api python manage.py dbshell
```

### Frontend Not Updating
Ensure the API endpoint is accessible:
```bash
curl http://localhost:8080/api/v1/feature-flags/
```