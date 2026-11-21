# scraper architecture

## Module structure
- Models: 6 Python files under models/.
- API: 6 Python files under api/.
- Services: 2 Python files under services/.
- Tests: 2; migrations: 3 (not run).

## Processing pattern
Where present, URL declarations bind handlers in api/views; handlers use serializers and models, with services/tasks for selected operations. Exact app-specific classes and references are listed in api.md and services-and-workflows.md. This is not assumed to be uniform.

## Source directory inventory

### api
api/urls.py
api/__init__.py
api/serializers/scraper_serializers.py
api/serializers/__init__.py
api/views/scraper_views.py
api/views/__init__.py

### models
models/parent_selector.py
models/scraped_data.py
models/scraping_config.py
models/scraping_job.py
models/website.py
models/__init__.py

### services
services/scraper_services.py
services/__init__.py

### tests
tests/test_scraper.py
tests/__init__.py

### migrations
migrations/0001_initial.py
migrations/0002_source_connectors_and_run_metrics.py
migrations/__init__.py


Shared architecture links: [backend catalog](../../02-system-component-catalog.md), [data relationships](../../06-database-and-model-catalog.md), [security and permissions](../../07-authentication-and-permissions.md).
