---
type: llm
focus: trace
weight: 1
---

backend/tests/domain/permits/facade/test_facade.py contains a test marked @pytest.mark.story("US-0044") whose act step calls PermitsFacade.get_rejected_evidences and whose assertion checks that call's result; arranging data through repositories or fixtures is fine, reading the result through a repository or SQL is not
