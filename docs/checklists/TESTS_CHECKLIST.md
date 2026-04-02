# TESTS_CHECKLIST.md

| Test Name            | Description                                             | File Name                                           | Line Numbers | Logging Integration     |
|---                   |---                                                      |---                                                  |---           |---                      |
| memory_scaffold_test | Unit tests for fact retention and recall.               | activation_demonstration/memory_scaffold_example.py | 138-144      | INFO; structured_logger |
| empirical_testing    | Matrix of unit/integration/E2E tests for new scaffolds. | protocols/empirical_testing_protocol.md             | N/A          | structured_logger       |
| auto_test_suite      | Heuristic regression tests for newly generated files.   | toolkits/audit_onboarding/auto_test_generator.py    | N/A          | None                    |
| adversarial_suite    | Isolated sandbox testing for robustness assessment.     | toolkits/dependency/testing_sandbox.py              | N/A          | structured_logger       |
| benchmark_regression | Comparative analysis of codebase state across sessions. | toolkits/dependency/benchmark_evaluator.py          | N/A          | structured_logger       |
| schema_validation    | Pydantic-based payload integrity checks for frontend.   | frontend/schemas.py                                 | 641-673      | None                    |
