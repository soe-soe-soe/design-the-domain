# DR 004: FRs in a folder per type, every policy in a process, schedules are policies

**Status:** Accepted · **Date:** 2026-11-01

## Context

FRs of all types lay side by side below a business object. Policies stood alone: which chain of
reactions a policy belonged to was nowhere written down. Scheduled behaviour (cron) had no type.

## Decision

- Below a business object (or directly below the subdomain) each FR type has its own folder –
  `invariants/`, `domain-services/`, `policies/`, `commands/`, `queries/`, `acl/`,
  `data-migrations/` – created with its first FR. `planned/` lies inside the type folder.
- Every Policy belongs to exactly one process. The process file (`assets/process.md`) stands in
  the `policies/` folder where the chain starts; policies of other subdomains link it.
- A scheduled reaction is a Policy with `Trigger: schedule`; it may stay inside its subdomain.
- Non-functional requirements and UI/UX are out of scope of design-the-domain.

## Considered alternatives

- **Type only in the header:** a folder listing shows nothing of the shape of a business
  object. Rejected.
- **Processes in a folder of their own per subdomain:** separates the process from the policies
  it consists of. Rejected.
- **Own FR type for scheduled jobs:** differs from a Policy only in its trigger. Rejected.
