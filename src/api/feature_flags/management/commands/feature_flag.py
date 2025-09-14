from django.core.management.base import BaseCommand, CommandError
from feature_flags.models import FeatureFlag, FeatureFlagHistory
from django.db import transaction


class Command(BaseCommand):
    help = 'Manage feature flags from the command line'

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='action', help='Available actions')
        subparsers.required = True

        # List command
        list_parser = subparsers.add_parser('list', help='List all feature flags')
        list_parser.add_argument(
            '--enabled-only',
            action='store_true',
            help='Show only enabled flags'
        )
        list_parser.add_argument(
            '--disabled-only',
            action='store_true',
            help='Show only disabled flags'
        )

        # Show command
        show_parser = subparsers.add_parser('show', help='Show details of a specific flag')
        show_parser.add_argument('flag_key', help='Feature flag key to show')
        show_parser.add_argument(
            '--history',
            action='store_true',
            help='Include change history'
        )

        # Enable command
        enable_parser = subparsers.add_parser('enable', help='Enable feature flag(s) - changes are immediate')
        enable_parser.add_argument('flag_keys', nargs='+', help='Feature flag key(s) to enable')
        enable_parser.add_argument(
            '--reason',
            default='Enabled via CLI',
            help='Reason for the change'
        )

        # Disable command
        disable_parser = subparsers.add_parser('disable', help='Disable feature flag(s) - changes are immediate')
        disable_parser.add_argument('flag_keys', nargs='+', help='Feature flag key(s) to disable')
        disable_parser.add_argument(
            '--reason',
            default='Disabled via CLI',
            help='Reason for the change'
        )

        # Toggle command
        toggle_parser = subparsers.add_parser('toggle', help='Toggle feature flag(s) - changes are immediate')
        toggle_parser.add_argument('flag_keys', nargs='+', help='Feature flag key(s) to toggle')
        toggle_parser.add_argument(
            '--reason',
            default='Toggled via CLI',
            help='Reason for the change'
        )

        # Create command
        create_parser = subparsers.add_parser('create', help='Create a new feature flag')
        create_parser.add_argument('flag_key', help='Feature flag key to create')
        create_parser.add_argument(
            '--description',
            required=True,
            help='Description of the feature flag'
        )
        create_parser.add_argument(
            '--enabled',
            action='store_true',
            help='Create flag in enabled state (default: disabled)'
        )

        # Delete command
        delete_parser = subparsers.add_parser('delete', help='Delete feature flag(s) - changes are immediate')
        delete_parser.add_argument('flag_keys', nargs='+', help='Feature flag key(s) to delete')
        delete_parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion (required)'
        )


    def handle(self, *args, **options):
        action = options['action']

        if action == 'list':
            self.list_flags(options)
        elif action == 'show':
            self.show_flag(options)
        elif action == 'enable':
            self.enable_flags(options)
        elif action == 'disable':
            self.disable_flags(options)
        elif action == 'toggle':
            self.toggle_flags(options)
        elif action == 'create':
            self.create_flag(options)
        elif action == 'delete':
            self.delete_flags(options)

    def list_flags(self, options):
        """List all feature flags"""
        queryset = FeatureFlag.objects.all()

        if options.get('enabled_only'):
            queryset = queryset.filter(enabled=True)
        elif options.get('disabled_only'):
            queryset = queryset.filter(enabled=False)

        if not queryset.exists():
            self.stdout.write(self.style.WARNING('No feature flags found'))
            return

        # Print header
        self.stdout.write(
            f"{'FLAG KEY':<25} {'STATUS':<10} {'DISPLAY NAME':<30} {'MODIFIED BY':<15}"
        )
        self.stdout.write('-' * 80)

        for flag in queryset:
            status = self.style.SUCCESS('ENABLED') if flag.enabled else self.style.ERROR('DISABLED')
            display_name = flag.get_feature_key_display()
            modified_by = flag.last_modified_by or 'N/A'

            self.stdout.write(
                f"{flag.feature_key:<25} {status:<10} {display_name:<30} {modified_by:<15}"
            )

    def show_flag(self, options):
        """Show details of a specific flag"""
        flag_key = options['flag_key']

        try:
            flag = FeatureFlag.objects.get(feature_key=flag_key)
        except FeatureFlag.DoesNotExist:
            raise CommandError(f'Feature flag "{flag_key}" does not exist')

        # Show flag details
        status_color = self.style.SUCCESS if flag.enabled else self.style.ERROR
        status = 'ENABLED' if flag.enabled else 'DISABLED'

        self.stdout.write(f"\nFeature Flag: {self.style.HTTP_INFO(flag.feature_key)}")
        self.stdout.write(f"Display Name: {flag.get_feature_key_display()}")
        self.stdout.write(f"Status: {status_color(status)}")
        self.stdout.write(f"Description: {flag.description}")
        self.stdout.write(f"Created: {flag.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        self.stdout.write(f"Updated: {flag.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        self.stdout.write(f"Last Modified By: {flag.last_modified_by or 'N/A'}")

        # Show history if requested
        if options.get('history'):
            history = flag.history.all()[:10]  # Last 10 changes
            if history:
                self.stdout.write(f"\nRecent Changes:")
                self.stdout.write(f"{'DATE':<20} {'CHANGE':<15} {'BY':<15} {'REASON':<30}")
                self.stdout.write('-' * 80)

                for change in history:
                    change_str = f"{change.previous_state} → {change.new_state}"
                    date_str = change.changed_at.strftime('%Y-%m-%d %H:%M:%S')
                    self.stdout.write(
                        f"{date_str:<20} {change_str:<15} {change.changed_by:<15} {change.reason[:30]:<30}"
                    )

    def enable_flags(self, options):
        """Enable feature flag(s)"""
        self._modify_flags(options['flag_keys'], True, options['reason'])

    def disable_flags(self, options):
        """Disable feature flag(s)"""
        self._modify_flags(options['flag_keys'], False, options['reason'])

    def toggle_flags(self, options):
        """Toggle feature flag(s)"""
        flag_keys = options['flag_keys']
        reason = options['reason']
        changed_count = 0

        with transaction.atomic():
            for flag_key in flag_keys:
                try:
                    flag = FeatureFlag.objects.get(feature_key=flag_key)
                    old_state = flag.enabled
                    new_state = not old_state

                    # Create history record
                    FeatureFlagHistory.objects.create(
                        feature_flag=flag,
                        previous_state=old_state,
                        new_state=new_state,
                        changed_by='CLI',
                        reason=reason
                    )

                    flag.enabled = new_state
                    flag.last_modified_by = 'CLI'
                    flag.save()

                    action = 'enabled' if new_state else 'disabled'
                    color = self.style.SUCCESS if new_state else self.style.ERROR
                    self.stdout.write(color(f'✓ Toggled "{flag_key}" to {action}'))
                    changed_count += 1

                except FeatureFlag.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Feature flag "{flag_key}" does not exist')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'\nToggled {changed_count} feature flag(s)')
        )

    def _modify_flags(self, flag_keys, enabled, reason):
        """Helper method to enable/disable flags"""
        changed_count = 0
        action = 'enabled' if enabled else 'disabled'
        action_past = 'enabled' if enabled else 'disabled'

        with transaction.atomic():
            for flag_key in flag_keys:
                try:
                    flag = FeatureFlag.objects.get(feature_key=flag_key)

                    if flag.enabled == enabled:
                        self.stdout.write(
                            self.style.WARNING(f'⚠ Feature flag "{flag_key}" is already {action_past}')
                        )
                        continue

                    # Create history record
                    FeatureFlagHistory.objects.create(
                        feature_flag=flag,
                        previous_state=flag.enabled,
                        new_state=enabled,
                        changed_by='CLI',
                        reason=reason
                    )

                    flag.enabled = enabled
                    flag.last_modified_by = 'CLI'
                    flag.save()

                    color = self.style.SUCCESS if enabled else self.style.ERROR
                    self.stdout.write(color(f'✓ {action.capitalize()} "{flag_key}"'))
                    changed_count += 1

                except FeatureFlag.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Feature flag "{flag_key}" does not exist')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'\n{action.capitalize()} {changed_count} feature flag(s)')
        )

    def create_flag(self, options):
        """Create a new feature flag"""
        flag_key = options['flag_key']
        description = options['description']
        enabled = options.get('enabled', False)

        # Check if flag_key is valid (should be in FEATURE_CHOICES)
        valid_keys = [choice[0] for choice in FeatureFlag.FEATURE_CHOICES]
        if flag_key not in valid_keys:
            self.stdout.write(
                self.style.WARNING(f'Warning: "{flag_key}" is not in predefined choices.')
            )
            self.stdout.write(f'Valid choices: {", ".join(valid_keys)}')

            # Ask for confirmation
            confirm = input('Continue anyway? (y/N): ').lower().strip()
            if confirm not in ['y', 'yes']:
                self.stdout.write('Aborted.')
                return

        try:
            flag = FeatureFlag.objects.create(
                feature_key=flag_key,
                enabled=enabled,
                description=description,
                last_modified_by='CLI'
            )

            status = 'enabled' if enabled else 'disabled'
            color = self.style.SUCCESS if enabled else self.style.ERROR
            self.stdout.write(
                color(f'✓ Created feature flag "{flag_key}" ({status})')
            )
            self.stdout.write(f'Description: {description}')

        except Exception as e:
            raise CommandError(f'Failed to create feature flag: {str(e)}')

    def delete_flags(self, options):
        """Delete feature flag(s)"""
        flag_keys = options['flag_keys']

        if not options.get('confirm'):
            raise CommandError(
                'Deletion requires confirmation. Use --confirm flag to proceed.'
            )

        deleted_count = 0

        with transaction.atomic():
            for flag_key in flag_keys:
                try:
                    flag = FeatureFlag.objects.get(feature_key=flag_key)
                    flag.delete()
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Deleted feature flag "{flag_key}"')
                    )
                    deleted_count += 1

                except FeatureFlag.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Feature flag "{flag_key}" does not exist')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'\nDeleted {deleted_count} feature flag(s)')
        )

