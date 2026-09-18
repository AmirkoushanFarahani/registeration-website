import json
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from registrations.models import KanoonAgency

class Command(BaseCommand):
    help = 'Import the public Kanoon office directory JSON into Django.'

    def add_arguments(self, parser):
        parser.add_argument('--file', default='data/kanoon_agencies.json')

    def handle(self, *args, **options):
        source = Path(options['file'])
        if not source.exists():
            raise CommandError(f'File not found: {source}')
        rows = json.loads(source.read_text(encoding='utf-8'))
        imported = 0
        for row in rows:
            KanoonAgency.objects.update_or_create(
                province=row['province'], office_name=row['office_name'], source_url=row['source_url'],
                defaults={
                    'city': row['city'], 'address': row['address'], 'phone_numbers': row['phone_numbers'],
                    'retrieved_at_utc': datetime.fromisoformat(row['retrieved_at_utc']),
                },
            )
            imported += 1
        self.stdout.write(self.style.SUCCESS(f'Imported {imported} Kanoon agencies.'))
