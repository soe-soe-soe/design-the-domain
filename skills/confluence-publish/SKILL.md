---
name: confluence-publish
description: Publishes the problem space to Confluence Cloud as a page tree – the domain map as a diagram, per subdomain its map, glossary, business objects and their functional requirements. One way, repository to Confluence. Use when the user wants the domain model in Confluence, wants Confluence updated after the model changed, or asks what would change there.
---

# Confluence publish

Paths `assets/…` and `scripts/…` are relative to this skill's base directory (named when the skill loads; `<base directory>` below). Scripts run from the project root.

Make the problem space readable in Confluence. The repository stays the source of truth: pages are
written from it, never read back into it. `scripts/confluence_publish.py`
builds the pages deterministically; you only check, show and sync them through the project's
Confluence connector (the Atlassian MCP).

**Project config.** Read `domain-model/config.md` in the project root before anything else; a name in
angle quotes is one of its keys. Without the file stop and tell the user, in
‹problem-space-language›, to fill in `domain-model/config.md` first (`/design-the-domain:domain-init`
does it with them). The keys of the section `## Confluence`:

| Key | Meaning |
|---|---|
| `confluence-space` | Key of the space the pages go into. `–`: stop and ask the user for it; write nothing. |
| `confluence-parent` | Title of the page the Domain Map page hangs under, or `–` for the top of the space. |
| `confluence-title-prefix` | Prefix of every page title (titles are unique per space), or `–`. |

## The page tree

```
Domain Map                         diagram of the subdomains (core, supporting, …) and their relationships
└─ <Subdomain>                     subdomain map diagram, business objects, relationships to other subdomains
   ├─ <Subdomain> – Glossary       the glossary of the subdomain
   └─ <Subdomain> / <Object>       one page per business object: its FRs as a table
      └─ FR-x-NNN: <title>         one page per active FR: rule and Gherkin scenarios
```

Planned FR changes (`planned/`) and user stories are not published. Every page carries the labels
`dtd`, `dtd-<kind>`, `sd-<subdomain>`; FR pages also `bo-<subdomain>-<object>`, the lower-cased FR id
and `status-<status>`.

## Steps

1. **Build.** Run `python3 <base directory>/scripts/confluence_publish.py build --out <scratch dir>`
   from the project root; use a scratch directory, not a folder of the repository. It writes
   `manifest.json`, one body per page (Confluence storage format) and the diagrams as SVG
   (needs `mmdc`, Mermaid CLI; env `MMDC` sets another command). Pass `--no-render` when `mmdc`
   is not there or the connector cannot upload attachments (step 3): the diagrams then stand in the
   pages as Mermaid code blocks. Show the user the warnings of the run, shortened: a link to no
   published page, a business object without a glossary section, a duplicate title.
2. **Compare.** For every page of `manifest.json`, in order (parents first), find the page in
   `confluence-space` by its content property `dtd-source` (= the manifest's `key`); if there is none,
   by title. Sort it into one of:
   - **new** – no page yet;
   - **unchanged** – the property `dtd-hash` equals the manifest's `sha256`, and the page's version
     equals the property `dtd-version`;
   - **update** – `dtd-hash` differs, the page's version equals `dtd-version`;
   - **edited in Confluence** – the page's version is higher than `dtd-version`: someone changed it
     there. It is not overwritten.
   - **orphan** – a page with `dtd-source` that the manifest no longer has (an FR or object was
     removed from the repository). Never deleted; reported.

   Show the user the result as a table (kind, title, state) and ask before writing anything.
3. **Sync.** Only on the user's yes, and only the new and update pages, in manifest order:
   create the page under its parent (the manifest's `parent` is the `key` of a page of the same
   manifest; `null` is `confluence-parent`, or the top of the space) or replace its body with the body
   file; add the labels; upload the page's attachments (replace a file of the same name); then set
   the properties `dtd-source` = `key`, `dtd-hash` = `sha256` and `dtd-version` = the version number
   the page has after this write. A page *edited in Confluence* is written only if the user says so
   for that page by name; the connector's version of it is then the one that is lost, say so.
4. **Report.** Per state the number of pages, the pages left alone and why, the orphans. Say
   plainly what was not done (a page skipped, a diagram published as code block).

The connector needs: search pages by title and by content property in a space, create a page with a
storage-format body under a parent, update a page's body with its version number, read and set content
properties, add labels, upload attachments. If it lacks one of them, say which and what that costs:
without attachment upload run step 1 with `--no-render`; without content properties find pages by title
only and do not detect pages edited in Confluence – then ask the user before every update.

## Interface

- **Call:** `design-the-domain:confluence-publish` (optional argument `plan`: steps 1 and 2 only, writes
  nothing to Confluence).
- **What you do:** build, compare, and after the user's yes create and update pages as above.
- **Result:** your last message, exactly in this form:

  ```
  Confluence: <space>
  - new: <n>, updated: <n>, unchanged: <n>
  - edited in Confluence, left alone: <title>, …
  - orphans: <title>, …
  ```
- **Guarantees:** writes nothing to the repository; writes to Confluence only after the user's yes;
  deletes no page; overwrites no page edited in Confluence without the user naming it.
