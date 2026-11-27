# FR types

The type stands as a DDD term in the FR header. It decides the building block in the solution
space (skill `solution-definition`, table in `‹structure›`), and
through it the test level; the problem space names no test level.

| Type | Folder | Sign in the AC (phrases in English; read them in `‹problem-space-language›`) | Example |
|---|---|---|---|
| Invariant | `invariants/` | "may only", "never", permitted transitions | evidence status only via permitted transitions |
| Domain Service | `domain-services/` | "counts as", "results from", "is calculated" | overdue deadline, problem signals, IRR, phase from the application status |
| Policy | `policies/` | "when X happens, then …" across a subdomain boundary; "daily", "every Monday", "at 6 am" (scheduled) | deadline done → entry in the evidence history; daily deadline reminder |
| Command | `commands/` | user creates, changes, deletes, advances | create a project, tick off a deadline |
| Query | `queries/` | what a view or API returns: selection, visibility, order | deadlines on the start page, team overview |
| Anti-Corruption Layer | `acl/` | a foreign system: Auth0, ALKIS, e-mail delivery | organisation name from Auth0 |
| Data Migration | `data-migrations/` | "existing … count as / become … after the change": what happens to data that already exists | existing evidences without a validity date count as unlimited |

The folder lies below the business object, or directly below the subdomain for an FR without
one, and is created with its first FR.

## Boundaries

- **Calculated value in a view:** if the Then step checks a calculated value ("shows 2
  problem signals"), the AC belongs to the Domain Service, even if the value appears in a view.
  Query only for what the view itself decides: which entries, who sees what, in which order.
- **Domain event:** an event is no FR. That it occurs is a scenario of the triggering
  Command; each reaction to it is an FR of its own of type Policy.
- **Existing data:** a scenario about data stored before the change is a Data Migration, even if
  the rule it carries over has an FR of another type. The new rule stays in that FR; the Data
  Migration FR says only what the existing data becomes.
- **Scheduled reaction:** what happens at a time rather than on an event ("daily", "on the
  first of the month") is a Policy with `Trigger: schedule`; it may stay inside its subdomain. The
  time itself ("06:00", "on working days") is part of the rule.
- **Process:** every Policy belongs to exactly one process – the chain from a trigger (a
  Command or a schedule) through the policies it sets off. The process file stands in the same
  `policies/` folder (`process.md`).
- **Out of scope:** non-functional requirements (performance, availability, security, audit)
  and UI/UX (layout, wording, interaction) get no FR; design-the-domain does not model them.
- **Plain create, change, delete:** one Command FR per business object ("Manage deadline"), with
  scenarios for validations and permissions only; not one FR per endpoint or per field. A command
  with a rule of its own (a status transition, a calculation) is an FR of its own.
- **One FR, one rule.** Two rules that can change independently are two FRs, even if one
  story touches both.
