---
name: aegissec-wordpress-review
description: Security review of WordPress plugins, themes and sites to the AegisSec standard — nonces and CSRF, capability checks, sanitisation and validation, output escaping, prepared SQL, REST and AJAX authorisation, file uploads and path traversal, secrets, plus vulnerable plugin and theme versions. Use when the user asks to audit, review or harden a WordPress plugin, theme, WooCommerce extension or WordPress site, or to check PHP code for WordPress security issues before release.
license: MIT
metadata:
  author: ymmiah
  package: aegissec
  version: "1.0.0"
---

# WordPress security review

Reviewing code the user owns or supplies is `DEFENSIVE`. Testing a live site they do not control, or attacking one, is `ASSESSMENT` and needs **aegissec-scope-check** first.

## 1. Inventory

List WordPress, plugin and theme versions, and PHP and database versions where known. For a site: admin users and roles, MFA and login protection, update state, abandoned components. Run **aegissec-vuln-scan** on any `composer.lock` or `package-lock.json`. For third-party plugins and themes, check their versions against WordPress vulnerability sources the user has access to, citing the source for each match.

## 2. Map the attack surface

Find every entry point before reading logic:

```bash
grep -rnE "add_action\(\s*'(wp_ajax_|wp_ajax_nopriv_|admin_post_|admin_post_nopriv_)|register_rest_route|add_shortcode|add_menu_page|add_submenu_page|\\\$_(GET|POST|REQUEST|COOKIE|FILES|SERVER)" --include=*.php .
```

`nopriv` AJAX and `admin_post_nopriv` hooks, and REST routes, are reachable without login: review them first.

## 3. Check each entry point

| Check | Look for | Vulnerable when |
| --- | --- | --- |
| **CSRF** | `wp_verify_nonce`, `check_admin_referer`, `check_ajax_referer` | A state-changing action has no nonce check |
| **Authorisation** | `current_user_can( 'specific_cap' )`; REST `permission_callback` | No capability check; `is_admin()` used as auth (it is not); `permission_callback => '__return_true'` on write routes |
| **Input** | `sanitize_text_field`, `absint`, `sanitize_email`, `wp_unslash`, allow-lists | Raw `$_POST`/`$_GET` reaching logic, options, meta or the database |
| **Output** | `esc_html`, `esc_attr`, `esc_url`, `wp_kses_post`, `esc_js` | Data echoed unescaped (escape late, at output) |
| **SQL** | `$wpdb->prepare` with placeholders | Variables concatenated into SQL; `esc_sql` alone; `LIKE` without `$wpdb->esc_like` |
| **Files** | `wp_handle_upload`, `wp_check_filetype_and_ext`, `realpath` checks | User-controlled paths (`../`), executable uploads, `include` of user input |
| **Secrets and config** | Keys, tokens or passwords in code; debug output | Credentials committed; `WP_DEBUG_DISPLAY` on in production |
| **Dangerous sinks** | `unserialize`, `eval`, `extract`, `call_user_func` with user input, `wp_remote_get` with user URLs (SSRF) | Reachable with attacker input |

Also check: cron and scheduled tasks, multisite capability differences, and that uninstall removes plugin data and options.

## 4. Report

Use **aegissec-finding-report**. For each issue give file:line, the exact entry point, who can reach it (unauthenticated, subscriber, editor, admin), and a code-level fix with a WordPress API example. Mark issues **confirmed** (traced end to end) or **potential**. Group by severity and end with a hardening checklist covering headers, TLS, backups, logging, updates and least-privilege roles.

## Offer to fix

Offer to fix the issues as a pull request: one class of issue per commit, without changing working behaviour beyond the fix, and with tests where the project has them. The user reviews and merges.
