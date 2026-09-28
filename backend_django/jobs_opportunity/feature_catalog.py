"""
Jobs Opportunity Feature Catalog

Canonical catalog for the Jobs Opportunity application.

IMPORTANT:
    This catalog describes product capabilities.
    It does NOT implement the business logic.

Business logic lives in:
    models.py
    services.py
    serializers.py
    views.py
    tasks.py
    integrations.py

The project contract intentionally contains exactly
150 product capabilities.
"""


FEATURES = [

    # ============================================================
    # 01 — DISCOVERY — 10
    # ============================================================

    ("Discovery", "Job source management"),
    ("Discovery", "Source enable/disable"),
    ("Discovery", "Source health monitoring"),
    ("Discovery", "Official API sources"),
    ("Discovery", "RSS/public feed sources"),
    ("Discovery", "Manual job source"),
    ("Discovery", "Scheduled source sync"),
    ("Discovery", "Manual source sync"),
    ("Discovery", "Bulk job import"),
    ("Discovery", "Job import normalization"),

    # ============================================================
    # 02 — DATA INTELLIGENCE — 10
    # ============================================================

    ("Data Intelligence", "Duplicate job detection"),
    ("Data Intelligence", "Canonical job keys"),
    ("Data Intelligence", "Company normalization"),
    ("Data Intelligence", "Location normalization"),
    ("Data Intelligence", "Remote classification"),
    ("Data Intelligence", "Hybrid classification"),
    ("Data Intelligence", "Employment type classification"),
    ("Data Intelligence", "Experience level extraction"),
    ("Data Intelligence", "Salary extraction"),
    ("Data Intelligence", "Salary period normalization"),

    # ============================================================
    # 03 — SEARCH — 10
    # ============================================================

    ("Search", "Global job search"),
    ("Search", "Advanced filters"),
    ("Search", "Multi-skill filtering"),
    ("Search", "Location filtering"),
    ("Search", "Salary range filtering"),
    ("Search", "Remote filtering"),
    ("Search", "Experience filtering"),
    ("Search", "Job type filtering"),
    ("Search", "Fresh jobs filtering"),
    ("Search", "Saved searches"),

    # ============================================================
    # 04 — MATCHING — 10
    # ============================================================

    ("Matching", "Job match score"),
    ("Matching", "Skill match"),
    ("Matching", "Skill level match"),
    ("Matching", "Missing skill detection"),
    ("Matching", "Skill gap severity"),
    ("Matching", "Weighted skill importance"),
    ("Matching", "Match explanation"),
    ("Matching", "Experience match"),
    ("Matching", "Location match"),
    ("Matching", "Salary match"),

    # ============================================================
    # 05 — CAREER FIT — 10
    # ============================================================

    ("Career Fit", "Job type preference match"),
    ("Career Fit", "Career goal match"),
    ("Career Fit", "Learning path match"),
    ("Career Fit", "Career interest match"),
    ("Career Fit", "Company preference match"),
    ("Career Fit", "Company blacklist"),
    ("Career Fit", "Personalized recommendations"),
    ("Career Fit", "Configurable score weights"),
    ("Career Fit", "Match breakdown"),
    ("Career Fit", "Job readiness score"),

    # ============================================================
    # 06 — SKILL GAP — 10
    # ============================================================

    ("Skill Gap", "Automatic skill gap records"),
    ("Skill Gap", "Required vs preferred requirements"),
    ("Skill Gap", "Skill gap prioritization"),
    ("Skill Gap", "Convert gap to learning goal"),
    ("Skill Gap", "Skill gap status tracking"),
    ("Skill Gap", "Learning progress linkage"),
    ("Skill Gap", "Skill gap refresh"),
    ("Skill Gap", "Readiness next actions"),
    ("Skill Gap", "Job readiness levels"),
    ("Skill Gap", "Skill improvement loop"),

    # ============================================================
    # 07 — APPLICATIONS — 10
    # ============================================================

    ("Applications", "Application pipeline"),
    ("Applications", "Application notes"),
    ("Applications", "Application deadline"),
    ("Applications", "Expected salary"),
    ("Applications", "Offer salary tracking"),
    ("Applications", "Rejection reason"),
    ("Applications", "Application timeline"),
    ("Applications", "Application status history"),
    ("Applications", "Resume per application"),
    ("Applications", "Cover letter per application"),

    # ============================================================
    # 08 — INTERVIEWS — 10
    # ============================================================

    ("Interviews", "Interview scheduling"),
    ("Interviews", "Interview stages"),
    ("Interviews", "Interview notes"),
    ("Interviews", "Interview questions"),
    ("Interviews", "Interview feedback"),
    ("Interviews", "Interview rating"),
    ("Interviews", "Interview completion tracking"),
    ("Interviews", "Technical interview preparation"),
    ("Interviews", "Follow-up reminders"),
    ("Interviews", "Mock interview data model"),

    # ============================================================
    # 09 — RESUME — 10
    # ============================================================

    ("Resume", "Multiple resume versions"),
    ("Resume", "Default resume"),
    ("Resume", "Resume file storage"),
    ("Resume", "Resume text storage"),
    ("Resume", "Resume metadata"),
    ("Resume", "Job-specific resume selection"),
    ("Resume", "Resume skill gap readiness"),
    ("Resume", "ATS-ready metadata"),
    ("Resume", "Resume version history"),
    ("Resume", "Resume application linking"),

    # ============================================================
    # 10 — COVER LETTER — 10
    # ============================================================

    ("Cover Letter", "Cover letter storage"),
    ("Cover Letter", "Job-specific cover letters"),
    ("Cover Letter", "Resume-aware cover letters"),
    ("Cover Letter", "Cover letter versions"),
    ("Cover Letter", "Generated cover letters"),
    ("Cover Letter", "Editable cover letters"),
    ("Cover Letter", "Application cover letter linking"),
    ("Cover Letter", "Company personalization data"),
    ("Cover Letter", "Role personalization data"),
    ("Cover Letter", "Reusable cover letter history"),

    # ============================================================
    # 11 — COMPANIES — 10
    # ============================================================

    ("Companies", "Company profiles"),
    ("Companies", "Company following"),
    ("Companies", "Company blacklist"),
    ("Companies", "Company notes"),
    ("Companies", "Company website"),
    ("Companies", "Company industry"),
    ("Companies", "Company location"),
    ("Companies", "Company size"),
    ("Companies", "Company job aggregation"),
    ("Companies", "Company skill demand"),

    # ============================================================
    # 12 — PREFERENCES — 10
    # ============================================================

    ("Preferences", "Career preferences"),
    ("Preferences", "Preferred job titles"),
    ("Preferences", "Preferred locations"),
    ("Preferences", "Preferred job types"),
    ("Preferences", "Preferred skills"),
    ("Preferences", "Remote preference"),
    ("Preferences", "Minimum salary"),
    ("Preferences", "Maximum salary"),
    ("Preferences", "Preferred companies"),
    ("Preferences", "Scoring priorities"),

    # ============================================================
    # 13 — RECOMMENDATIONS — 10
    # ============================================================

    ("Recommendations", "Recommended job feed"),
    ("Recommendations", "Similar job discovery"),
    ("Recommendations", "Recommendation reasons"),
    ("Recommendations", "Recommendation seen state"),
    ("Recommendations", "Recommendation saved state"),
    ("Recommendations", "Recommendation dismissal"),
    ("Recommendations", "Skill-based recommendations"),
    ("Recommendations", "Goal-based recommendations"),
    ("Recommendations", "Fresh opportunity recommendations"),
    ("Recommendations", "Recommendation refresh"),

    # ============================================================
    # 14 — AUTOMATION — 10
    # ============================================================

    ("Automation", "Background source sync"),
    ("Automation", "Background match refresh"),
    ("Automation", "Automatic expiration"),
    ("Automation", "Automatic deduplication"),
    ("Automation", "Automatic skill extraction"),
    ("Automation", "Automatic company normalization"),
    ("Automation", "Automatic location classification"),
    ("Automation", "Automatic salary parsing"),
    ("Automation", "Automatic recommendation refresh"),
    ("Automation", "Analytics snapshots"),

    # ============================================================
    # 15 — ANALYTICS — 10
    # ============================================================

    ("Analytics", "Job dashboard metrics"),
    ("Analytics", "Application conversion rate"),
    ("Analytics", "Interview rate"),
    ("Analytics", "Offer rate"),
    ("Analytics", "Rejection analysis"),
    ("Analytics", "Skill demand analytics"),
    ("Analytics", "Salary analytics"),
    ("Analytics", "Remote job analytics"),
    ("Analytics", "Source analytics"),
    ("Analytics", "Company analytics"),

]


# ============================================================
# CONTRACT
# ============================================================

EXPECTED_FEATURE_COUNT = 150


# Defensive validation
actual_count = len(FEATURES)

if actual_count != EXPECTED_FEATURE_COUNT:
    raise RuntimeError(
        "Jobs Opportunity feature catalog must contain "
        f"{EXPECTED_FEATURE_COUNT} features, "
        f"but found {actual_count}."
    )


# ============================================================
# DUPLICATE VALIDATION
# ============================================================

if len(set(FEATURES)) != len(FEATURES):
    raise RuntimeError(
        "Jobs Opportunity feature catalog contains duplicate features."
    )


# ============================================================
# CATEGORY HELPERS
# ============================================================

FEATURE_CATEGORIES = tuple(
    dict.fromkeys(
        category
        for category, _ in FEATURES
    )
)


FEATURES_BY_CATEGORY = {
    category: [
        feature_name
        for feature_category, feature_name in FEATURES
        if feature_category == category
    ]
    for category in FEATURE_CATEGORIES
}


FEATURE_COUNT_BY_CATEGORY = {
    category: len(features)
    for category, features in FEATURES_BY_CATEGORY.items()
}


# ============================================================
# PUBLIC HELPERS
# ============================================================

def get_feature_count():
    return len(FEATURES)


def get_categories():
    return FEATURE_CATEGORIES


def get_features_by_category(category):
    return FEATURES_BY_CATEGORY.get(category, [])


def get_feature_catalog():
    return [
        {
            "id": index + 1,
            "category": category,
            "name": name,
            "status": "available",
        }
        for index, (category, name) in enumerate(FEATURES)
    ]
