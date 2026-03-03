# CLASSES_CHECKLIST.md

| Class Name        | Description                                       | File Name                                           | Line Numbers | Logging Integration                    |
|---                |---                                                |---                                                  |---           |---                                     |
| SimpleMemory      | Basic vector-like store for fact retention.       | activation_demonstration/memory_scaffold_example.py | 127-137      | INFO on memory; structured_logger      |
| CommunicationBus  | In-memory message dispatcher for frontend agents. | frontend/communication_bus.py                       | 384-438      | ERROR on validation; structured_logger |
| ProvenanceHeader  | Pydantic model for traceability metadata.         | frontend/schemas.py                                 | 644-649      | None                                   |
| DiscoveryPayload  | Requirements schema for Intake discoveries.       | frontend/schemas.py                                 | 650-654      | None                                   |
| SequencePayload   | Task list schema for Planning sequences.          | frontend/schemas.py                                 | 655-659      | None                                   |
| DebugEventPayload | Error context schema for Interactive fixes.       | frontend/schemas.py                                 | 660-665      | None                                   |
| SessionState      | Persistent storage schema for user context.       | frontend/schemas.py                                 | 666-672      | None                                   |
| AtomicFileWriter  | Context manager for idempotent file operations.   | toolkits/dependency/core_utils.py                   | N/A          | None                                   |
| AuditReport       | Results container for hallucination audits.       | toolkits/dependency/audit_engine.py                 | N/A          | None                                   |
