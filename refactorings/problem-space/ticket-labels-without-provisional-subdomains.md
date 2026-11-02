# Ticket labels without provisional subdomains

## Goal

The ticket template no longer knows provisional subdomains: every subdomain of the domain map
gets its own label.

## Why

Provisional subdomains were removed from pts (`skills/problem-fr-writer/decision-records/004-type-folders-and-processes.md`
context, layout of `problem-fr-writer`, domain-map template without the column `Status`). The
ticket template, merged in from the ticket sync, still maps "a provisional subdomain" to its
host's label – a rule for a concept that no longer exists, and nothing in the domain map can tell
a writer which subdomain is the host.

## Current state

- `templates/ticket.md`, row `Labels`: "one per subdomain of the story's FRs …; a provisional
  subdomain takes its host's label."
- No other skill or template mentions provisional subdomains (`problem-story-writer` uses
  "provisional" only for a Then step, which is unrelated).

## Target state

- The clause "a provisional subdomain takes its host's label" is gone; each subdomain of
  `‹domain-map›` – including one of type `open` – maps to the label of its own name. A label
  missing in the ticket system follows the existing *Missing label* rule.
- Projects that still have provisional subdomains (the pilot project: Ausschreibung, Bau) drop them as
  described in their own refactoring before relying on the labels.

## Before starting

- Check the eval cases of the ticket sync for a provisional subdomain in their fixtures or
  graders and adjust them with the template.
