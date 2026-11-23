# Rules

The domain language is German (terms, stories, glossaries), code and commits are English.
Backend in `backend/` (Python, pytest); `backend/core` is cross-cutting code shared by all contexts.

## Feature workflow

1. `/design-the-domain:requirement <Anforderung>` grills the requirement into stories; at the end
   every story is `ready` or `draft` with its deferred points.
2. A `ready` story is implemented next: `/implement-the-domain:implement-story US-NNNN`.
3. A `draft` story goes back into `/design-the-domain:requirement` once its deferred points are
   decided.

Commits follow Conventional Commits (`feat:`, `fix:`, `docs:`), one story per branch `story/US-NNNN`.
