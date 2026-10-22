# backend_django/jobs_opportunity/management/commands/scrape_jobs.py
from django.core.management.base import BaseCommand
from jobs_opportunity.scraper import JobScraperService
from jobs_opportunity.models import JobOpportunity


class Command(BaseCommand):
    help = 'Synchronously scrape job opportunities and save them to the database.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(
            "Initializing synchronous job scraper..."))
        scraper = JobScraperService()
        jobs = scraper.fetch_and_parse()

        count = 0
        for job_data in jobs:
            JobOpportunity.objects.update_or_create(
                external_id=job_data.get('external_id'),
                defaults=job_data
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully scraped and updated {count} jobs."))
