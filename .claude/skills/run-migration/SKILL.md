---
name: run-migration
description: Review, apply and verify a database migration with a rollback plan. Use only when the user explicitly asks to run or prepare a migration.
disable-model-invocation: true
---

# run-migration

Apply a schema migration without surprises. Migrations change **shared state** that is hard to undo, so this skill reviews first, targets non-production by default, and confirms before running.

> **Customize.** Set `TODO(team)`: migration tool and commands (Alembic, Flyway, Prisma, Rails, Liquibase…), how to point at each environment, and the backup procedure.

**Inputs:** the migration (file or "the pending ones") and the target environment. Default target is local/dev; **production requires the user to name it explicitly.**
**Output:** a risk review and rollback plan before running, then a result report (applied versions, verification, rollback path).

## Procedure

1. **Identify the tool and pending migrations.** List them (`TODO(team): status command`). Read each migration fully.
2. **Review for risk.** Flag, with the reason:
   - Destructive: `DROP TABLE/COLUMN`, `TRUNCATE`, type narrowing, data-losing `UPDATE/DELETE`.
   - Locking: `ALTER TABLE` rewrites, adding a `NOT NULL` column with a default on a large table, non-concurrent index creation.
   - Compatibility: does the *currently deployed* application version still work against the new schema (expand → migrate → contract)?
   - Reversibility: is there a working down/rollback? If not, say so and propose one.
   - Data volume: estimate rows touched; flag long-running backfills.
3. **Rollback plan.** State exactly how to undo it (down migration, or restore from backup) and whether data would be lost.
4. **Dry run.** Use the tool's dry-run / SQL-preview mode, or run against a fresh local database and a copy of the schema. Report the result.
5. **Confirm.** Show target environment, migrations to apply, risks and rollback. Wait for explicit approval naming the environment.
6. **Apply.** Run the migration. Capture output.
7. **Verify.** Check the migration version table, run a smoke query on changed tables, and run the relevant tests. Report.

## Rules

- Never run against a production or shared database without explicit, environment-named approval.
- Never edit a migration that has already been applied anywhere; add a new one.
- Never disable foreign keys, constraints or transactions to make a migration pass.
- If a required backup does not exist, stop and say so.
- Do not print connection strings or credentials.
