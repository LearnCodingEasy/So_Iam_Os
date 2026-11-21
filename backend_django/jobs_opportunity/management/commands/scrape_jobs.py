from django.core.management.base import BaseCommand, CommandError

from jobs_opportunity.models import JobSource
from jobs_opportunity.scraper import JobScraperService


class Command(BaseCommand):
    help = "Synchronize enabled HTML job sources through the unified ingestion pipeline."

    def add_arguments(self, parser):
        parser.add_argument("--source-id", type=int, help="Synchronize only this HTML source.")

    def handle(self, *args, **options):
        sources = JobSource.objects.filter(
            enabled=True, source_type=JobSource.SourceType.SCRAPER
        )
        if options.get("source_id"):
            sources = sources.filter(pk=options["source_id"])
        sources = list(sources.order_by("pk"))
        if not sources:
            raise CommandError(
                "No enabled HTML scraper sources found. Review source configuration and terms first."
            )

        service = JobScraperService()
        succeeded = 0
        failed = 0
        for source in sources:
            try:
                result = service.run(source.pk)
                succeeded += 1
                self.stdout.write(self.style.SUCCESS(
                    f"Source {source.pk} ({source.name}): {result.get('jobs', 0)} jobs processed."
                ))
            except Exception as exc:
                failed += 1
                self.stderr.write(self.style.ERROR(
                    f"Source {source.pk} ({source.name}) failed: {exc.__class__.__name__}: {exc}"
                ))
        self.stdout.write(
            f"Scraper sync finished: {succeeded} succeeded, {failed} failed."
        )
        if failed:
            raise CommandError("One or more scraper sources failed; see errors above.")
