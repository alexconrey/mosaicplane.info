from django.core.management.base import BaseCommand
from feature_flags.models import FeatureFlag


class Command(BaseCommand):
    help = 'Initialize default feature flags'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset existing flags to default values',
        )

    def handle(self, *args, **options):
        """
        Create default feature flags
        """
        default_flags = [
            {
                'feature_key': 'ads_enabled',
                'enabled': False,
                'description': 'Enable Google AdSense ads throughout the application. Disable while waiting for Google approval.'
            },
            {
                'feature_key': 'amp_ads_enabled',
                'enabled': False,
                'description': 'Enable AMP ads on aircraft detail pages. Requires ads_enabled to also be true.'
            },
            {
                'feature_key': 'analytics_enabled',
                'enabled': True,
                'description': 'Enable Google Analytics tracking and user behavior analysis.'
            },
            {
                'feature_key': 'beta_features',
                'enabled': False,
                'description': 'Enable beta features for testing. Should be disabled in production.'
            },
            {
                'feature_key': 'maintenance_mode',
                'enabled': False,
                'description': 'Enable maintenance mode banner. Shows a maintenance notice to users.'
            },
        ]

        created_count = 0
        updated_count = 0

        for flag_data in default_flags:
            flag, created = FeatureFlag.objects.get_or_create(
                feature_key=flag_data['feature_key'],
                defaults={
                    'enabled': flag_data['enabled'],
                    'description': flag_data['description'],
                    'last_modified_by': 'system_init'
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created feature flag: {flag_data["feature_key"]} ({"enabled" if flag_data["enabled"] else "disabled"})'
                    )
                )
            elif options['reset']:
                flag.enabled = flag_data['enabled']
                flag.description = flag_data['description']
                flag.last_modified_by = 'system_reset'
                flag.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'Reset feature flag: {flag_data["feature_key"]} ({"enabled" if flag_data["enabled"] else "disabled"})'
                    )
                )
            else:
                self.stdout.write(
                    f'Feature flag already exists: {flag_data["feature_key"]} (skipped)'
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nFeature flags initialization complete: {created_count} created, {updated_count} updated'
            )
        )

        if created_count == 0 and updated_count == 0 and not options['reset']:
            self.stdout.write(
                self.style.WARNING(
                    'All feature flags already exist. Use --reset to update existing flags.'
                )
            )