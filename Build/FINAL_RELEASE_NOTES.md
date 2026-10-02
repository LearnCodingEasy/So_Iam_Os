# SO_IAM_OS — Final Release Notes

## Main architecture retained

- Django + DRF backend
- Vue 3 + Pinia frontend
- PrimeVue UI system
- AI providers
- Codex project-intelligence foundation
- Automation workflow engine
- Learning / Knowledge / Jobs / Tasks / Goals / Social / Notifications
- Existing migrations and development database

## New operational guarantees

The project now has explicit local/production environment configuration, a dependency manifest, source validation scripts, and release verification documentation.

## Final local validation command

```bash
./scripts/verify_release.sh
```

On Windows PowerShell, use the commands in `LOCAL_SETUP.md`.
