# WordPress Security Review

1. Inventory WordPress/core/plugins/themes and update state.
2. Review admin users, roles, MFA and login protections.
3. Review custom PHP for nonce, capability, sanitisation, validation and escaping.
4. Review REST/AJAX endpoints for authentication/authorisation and CSRF protections.
5. Review uploads, filesystem permissions, secrets, database access and cron.
6. Check headers, TLS, backups, logging and update/recovery process.
7. Remove abandoned components and reduce attack surface.
