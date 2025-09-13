from django.core.management.base import BaseCommand
from django.utils import timezone
from aircraft.models import Aircraft, AircraftCorrection
from datetime import datetime
import json


class Command(BaseCommand):
    help = 'Review and manage user-submitted aircraft corrections'

    def add_arguments(self, parser):
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all pending corrections'
        )
        parser.add_argument(
            '--show',
            type=int,
            help='Show details for a specific correction ID'
        )
        parser.add_argument(
            '--approve',
            type=int,
            help='Approve a correction by ID'
        )
        parser.add_argument(
            '--reject',
            type=int,
            help='Reject a correction by ID'
        )
        parser.add_argument(
            '--implement',
            type=int,
            help='Mark a correction as implemented by ID'
        )
        parser.add_argument(
            '--notes',
            type=str,
            help='Admin notes to add when approving/rejecting'
        )
        parser.add_argument(
            '--status',
            choices=['PENDING', 'APPROVED', 'REJECTED', 'IMPLEMENTED'],
            help='Filter corrections by status'
        )

    def handle(self, *args, **options):
        if options['list']:
            self.list_corrections(options.get('status'))
        elif options['show']:
            self.show_correction(options['show'])
        elif options['approve']:
            self.approve_correction(options['approve'], options.get('notes', ''))
        elif options['reject']:
            self.reject_correction(options['reject'], options.get('notes', ''))
        elif options['implement']:
            self.implement_correction(options['implement'], options.get('notes', ''))
        else:
            self.stdout.write(self.style.WARNING(
                'Please specify an action: --list, --show ID, --approve ID, --reject ID, or --implement ID'
            ))

    def list_corrections(self, status_filter=None):
        corrections = AircraftCorrection.objects.all()
        if status_filter:
            corrections = corrections.filter(status=status_filter)
        else:
            corrections = corrections.filter(status='PENDING')

        if not corrections.exists():
            status_msg = f" with status {status_filter}" if status_filter else " pending"
            self.stdout.write(f"No corrections{status_msg}")
            return

        self.stdout.write(self.style.SUCCESS(f'Aircraft Corrections ({corrections.count()} total):\n'))
        
        for correction in corrections:
            status_color = {
                'PENDING': self.style.WARNING,
                'APPROVED': self.style.SUCCESS,
                'REJECTED': self.style.ERROR,
                'IMPLEMENTED': self.style.HTTP_INFO,
            }.get(correction.status, self.style.NOTICE)
            
            self.stdout.write(
                f"ID: {correction.id:<4} | "
                f"{status_color(correction.status.ljust(12))} | "
                f"{correction.aircraft} | "
                f"{correction.get_field_name_display()} | "
                f"Submitted: {correction.created_at.strftime('%Y-%m-%d')}"
            )

    def show_correction(self, correction_id):
        try:
            correction = AircraftCorrection.objects.get(id=correction_id)
        except AircraftCorrection.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Correction {correction_id} not found'))
            return

        self.stdout.write(self.style.SUCCESS(f'\n=== Correction Details (ID: {correction.id}) ===\n'))
        self.stdout.write(f"Aircraft: {correction.aircraft}")
        self.stdout.write(f"Field: {correction.get_field_name_display()}")
        self.stdout.write(f"Status: {correction.status}")
        self.stdout.write(f"Submitted: {correction.created_at}")
        
        if correction.submitter_name:
            self.stdout.write(f"Submitter: {correction.submitter_name}")
        if correction.submitter_email:
            self.stdout.write(f"Email: {correction.submitter_email}")

        self.stdout.write(f"\nCurrent Value:")
        self.stdout.write(f"  {correction.current_value}")
        
        self.stdout.write(f"\nSuggested Value:")
        self.stdout.write(f"  {correction.suggested_value}")
        
        self.stdout.write(f"\nReason:")
        self.stdout.write(f"  {correction.reason}")
        
        if correction.source_documentation:
            self.stdout.write(f"\nSource Documentation:")
            self.stdout.write(f"  {correction.source_documentation}")
            
        if correction.admin_notes:
            self.stdout.write(f"\nAdmin Notes:")
            self.stdout.write(f"  {correction.admin_notes}")

    def approve_correction(self, correction_id, notes=''):
        try:
            correction = AircraftCorrection.objects.get(id=correction_id)
        except AircraftCorrection.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Correction {correction_id} not found'))
            return

        correction.status = 'APPROVED'
        correction.reviewed_at = timezone.now()
        if notes:
            correction.admin_notes = notes
        correction.save()

        self.stdout.write(
            self.style.SUCCESS(f'✅ Approved correction {correction_id}: {correction.aircraft} - {correction.get_field_name_display()}')
        )
        self.stdout.write(f'   Current: {correction.current_value}')
        self.stdout.write(f'   Suggested: {correction.suggested_value}')
        self.stdout.write(self.style.WARNING('\n⚠️  Remember to manually implement the change and mark as IMPLEMENTED'))

    def reject_correction(self, correction_id, notes=''):
        try:
            correction = AircraftCorrection.objects.get(id=correction_id)
        except AircraftCorrection.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Correction {correction_id} not found'))
            return

        correction.status = 'REJECTED'
        correction.reviewed_at = timezone.now()
        if notes:
            correction.admin_notes = notes
        correction.save()

        self.stdout.write(
            self.style.ERROR(f'❌ Rejected correction {correction_id}: {correction.aircraft} - {correction.get_field_name_display()}')
        )
        if notes:
            self.stdout.write(f'   Reason: {notes}')

    def implement_correction(self, correction_id, notes=''):
        try:
            correction = AircraftCorrection.objects.get(id=correction_id)
        except AircraftCorrection.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Correction {correction_id} not found'))
            return

        if correction.status != 'APPROVED':
            self.stdout.write(
                self.style.WARNING(f'Correction {correction_id} is not approved (current status: {correction.status})')
            )
            confirm = input('Mark as implemented anyway? [y/N]: ')
            if confirm.lower() != 'y':
                return

        correction.status = 'IMPLEMENTED'
        correction.reviewed_at = timezone.now()
        if notes:
            correction.admin_notes += f"\nImplemented: {notes}" if correction.admin_notes else f"Implemented: {notes}"
        correction.save()

        self.stdout.write(
            self.style.HTTP_INFO(f'✅ Marked correction {correction_id} as implemented: {correction.aircraft} - {correction.get_field_name_display()}')
        )