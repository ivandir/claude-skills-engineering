---
name: scaffold-endpoint
description: Scaffold a new API endpoint following the team's conventions (handler, service function, tests, spec). Use when asked to add a new API endpoint or route to a service.
---

# scaffold-endpoint

Add an endpoint the way the team already adds them — not the way a generic tutorial does.

> **Customize this skill.** The steps below are generic. Replace the `TODO(team)` lines with your framework, paths and spec tooling before rolling it out; a scaffold skill that doesn't match your repo is worse than none.

**Inputs:** HTTP method + path, request/response shape, auth requirement, and the business behavior in one or two sentences. Ask for anything missing.
**Output:** the minimal set of files/changes for a working, tested endpoint.

## Procedure

1. **Find a reference.** Locate the most similar existing endpoint and mirror its structure. State which one you used.
2. **Spec first.** Update the API spec (TODO(team): `openapi.yaml`) with the new path, schemas and error responses. Additive only — if this changes an existing contract, stop and ask.
3. **Handler.** Add a thin handler: validate input, call the service function, map the result/errors. TODO(team): handler location and framework idiom.
4. **Service function.** Put business logic in the service layer (TODO(team): `services/`). No framework types in service code.
5. **Auth.** Apply the same authn/authz mechanism as sibling endpoints. If unsure which scope applies, ask — do not default to "public".
6. **Tests.** Add an integration test hitting the real router and unit tests for the service function, including validation failure and unauthorized cases.
7. **Run** `TODO(team): test command` and report results.

## Rules

- Do not add dependencies, change CI, or run migrations as part of scaffolding.
- Do not invent fields the user didn't specify; list assumptions at the end.
- Keep the diff small enough to review in one sitting.
