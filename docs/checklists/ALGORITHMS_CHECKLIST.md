# ALGORITHMS_CHECKLIST.md

| Algorithm Name               | Description                                                | File Name                                          | Line Numbers | Logging Integration |
|---                           |---                                                         |---                                                 |---           |---                  |
| Majority-Vote Consensus      | Selection of the best variant for pure-prompt scaffolding. | protocols/scaffolding_generation_protocol.md       | 37-43        | None                |
| AST Static Analysis          | Parsing and audit of markdown or code structures.          | toolkits/dependency/audit_engine.py                | N/A          | structured_logger   |
| Multi-Objective Optimization | Pareto-front delta calculation for impact evaluation.      | toolkits/dependency/benchmark_evaluator.py         | N/A          | structured_logger   |
| Monte-Carlo Execution        | Statistical pass/fail determination for flaky tests.       | toolkits/dependency/testing_sandbox.py             | N/A          | structured_logger   |
| Width-Padding Alignment      | Spooled text buffering for markdown table formatting.      | toolkits/dependency/table_formatter.py             | N/A          | None                |
| Directed Graph Crawling      | Import statement traversal for dependency visualization.   | toolkits/audit_onboarding/dependency_visualizer.py | N/A          | None                |
| Weighted Routing             | Priority-based message dispatch for the communication bus. | frontend/communication_bus.py                      | 387, 428-438 | structured_logger   |
