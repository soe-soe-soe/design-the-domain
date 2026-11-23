# Refactoring 006: lifecycle of a business object in the problem space

Status: Proposed · Date: 2026-11-17

## Goal

The problem space states the lifecycle of every business object that has one: its states and the
transitions between them, so that the solution space can be derived from it without a decision
that is really a business one.

## Why

The subdomain map (planned, see below) holds business objects, their relationships and
attributes. What an object may become over time is not stored anywhere in a structured way: states
sit in the values of a status attribute, transitions in the scenarios of commands and invariants,
and only whoever reads all FRs of the business object sees the whole.

## Where a lifecycle belongs

- **A business object** (aggregate root) has a lifecycle: the states of its instances and the
  transitions between them, each caused by a command or a domain event.
- **A subdomain** has none in this sense. What spans several business objects is a **process**
  (`assets/process.md`, the chain of policies); that is where "after A happens, B follows" is
  stated already.
- **Entities inside an aggregate** are governed by their root; their states are part of the
  root's lifecycle unless the business names them separately.

## Current state

- No place for states and transitions. `assets/glossary.md` lists a status as a Value with its
  enumeration values; `assets/functional-requirement-types.md` knows commands and invariants.
- The subdomain map is not built yet; this refactoring builds on it.

## Target state (to decide)

- The lifecycle stands in the subdomain map of the subdomain, one per business object, as a
  state diagram (Mermaid `stateDiagram-v2`) next to the class diagram of that object.
- States use terms of the glossary (the enumeration values of the status Value); a transition
  names its command or domain event by its glossary term, never a rule: the rule stays in the FR.
- Open: is the lifecycle derived from the FRs (and only checked), or maintained by the writers like
  the rest of the map? `domain-init` can read it from status enumerations and
  guards in the code; `functional-requirement` decides it with the "consistency" case.
- Open: `requirements.py check` could verify that every command named in a transition exists as an
  FR of type Command.

## Before starting

- The subdomain map with relationships and attributes exists and is used by
  `domain-init`, `functional-requirement` and the ground read of `requirement`.
- Decide whether a business object without a status (no states) simply has no lifecycle section.
