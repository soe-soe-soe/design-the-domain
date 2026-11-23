# implement-the-domain – solution and test space skills

> **Status: scaffold (refactoring 011).** The skills were moved here from `design-the-domain`. They
> are not published and not tested in this form. They need `design-the-domain` enabled: story status
> and glossary code names go through its interfaces (see its README, section Interfaces). Open points:
> `refactorings/011-split-design-and-implement.md`, section "Solution space (open)".

- `solution-definition` places a story's scenarios into bounded contexts, aggregates and building
  blocks and builds a shell without behaviour; `/implement-the-domain:solution-init` plans the
  migration of existing code into that structure.
- `test-definition` writes red scenario, interface, migration and journey tests against the shell;
  `/implement-the-domain:implement-story` runs placement, tests, implementation, review and closing
  for one story.
- Craft skills `tdd`, `code-review`, `codebase-design`, based on
  [mattpocock/skills](https://github.com/mattpocock/skills) (MIT, see
  [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)).

It works on the problem space `design-the-domain` writes (stories, FRs, glossaries under
`domain-model/`) and reads the same `domain-model/config.md`, with its own part from [assets/config.md](assets/config.md).

Load the working copy with `claude --plugin-dir implement-the-domain`.
