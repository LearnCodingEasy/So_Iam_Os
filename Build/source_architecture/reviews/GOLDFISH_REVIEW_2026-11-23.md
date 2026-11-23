# Goldfish Second-Pass Adversarial Review — 2026-11-23

**Review target:** documentation additions and source-grounded inventories generated from the supplied archive. **Method:** second-pass adversarial checklist against source paths and conservative evidence labels, performed within this review session; it is not a separate human/external reviewer. Static only. No external EGM plugin runtime was available in this execution, so this is an EGM-style Goldfish review, not a claim that Codex's plugin command ran.

## Review result

**Documentation package: conditionally accepted**

The new navigation and catalogue layer addresses the main orientation problem: a single Master Map, current archive baseline, app index, frontend route catalogue, backend catalogue, model relationship inventory, dependency map, feature registry, change workflow, and prioritized backlog now exist. The result is useful for source navigation, but it is not a complete semantic architecture or proof of working product behavior.

## Findings

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| G-01 | HIGH | Supplied archive omits `.git/` and `project_docs/`; cannot verify local working tree, previously modified paths, or user-facing docs. | OPEN — requires live checkout audit |
| G-02 | HIGH | Route and model inventories are static heuristics; they do not fully resolve nested routers, dynamic URL patterns, inherited models, serializers, permissions, or runtime behavior. | DOCUMENTED — runtime/source-trace phase remains |
| G-03 | MEDIUM | Historical docs still contain stale app and file counts. | MITIGATED — new baseline/master map supersede counts for this archive; historical files preserved |
| G-04 | MEDIUM | Feature registry rows are route/mount declarations, not end-to-end verified capabilities. | MITIGATED — conservative status labels and explicit evidence rules |
| G-05 | MEDIUM | Dependency map mixes confirmed model declarations with prior documented cross-domain hypotheses; edge types are labeled and cautioned. | PARTIAL — require exhaustive imports/service/API/task trace |
| G-06 | LOW | Per-app semantic guides are uneven: 17 legacy guides plus 9 newer app summaries, rather than one uniform depth. | OPEN — P1 app-by-app trace |
| G-07 | LOW | No tests/lint/build/runtime were run; therefore application defects cannot be certified fixed. | OPEN — separate approved verification phase |
| G-08 | MEDIUM | The `skills/` directory has `apps.py` but is not in `INSTALLED_APPS`; older docs incorrectly called it installed. Its files are placeholders; the active `Skill` model is in `learning`. | FIXED IN CURRENT DOCS — registration claims corrected; no code change made |

## Goldfish challenge checklist

- [x] Does the map clearly identify source-of-truth hierarchy?
- [x] Does it distinguish vision from implemented behavior?
- [x] Are archive omissions explicit?
- [x] Are source counts accompanied by counting rules?
- [x] Are model and route declarations prevented from implying working features?
- [x] Is there a repeatable EGM change lifecycle and owner approval gate?
- [ ] Are all API operations and contracts exhaustively traced?
- [ ] Are all app-to-app imports, service calls, events, and background tasks mapped?
- [ ] Are all feature paths runtime-tested?
- [ ] Is the live Git state and VuePress site reviewed?

## Additional source discrepancy resolved

The first pass initially treated all 26 app-like directories as installed. Rechecking the literal `INSTALLED_APPS` list showed only 25 registered apps. `skills/` is the exception and is documented as an unregistered placeholder package. It was not added to settings because the package has no implemented model/API and the active `Skill` model lives in `learning`; activation would be an unjustified source change.

## Final verdict

**Accept for project orientation and as the next documentation baseline, not as a complete implementation reference.** No source-code defect was changed or declared fixed because this pass did not execute the application or its tests. The remaining high/medium items are explicitly assigned in `PROJECT_NEXT_ACTIONS.md`.
