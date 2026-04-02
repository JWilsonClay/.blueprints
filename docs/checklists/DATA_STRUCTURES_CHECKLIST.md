# DATA_STRUCTURES_CHECKLIST.md

| Data Structure Name | Description                                                | File Name                                           | Line Numbers | Logging Integration                         |
|---                  |---                                                         |---                                                  |---           |---                                          |
| store               | List for retaining simple string-based "facts".            | activation_demonstration/memory_scaffold_example.py | 129          | INFO on remember(); structured_logger       |
| subscribers         | Defaultdict(list) mapping channels to callbacks.           | frontend/communication_bus.py                       | 386          | None                                        |
| message_queue       | PriorityQueue for ordered asynchronous message processing. | frontend/communication_bus.py                       | 387          | None                                        |
| replay_buffer       | List tracking the last 1000 messages for session sync.     | frontend/communication_bus.py                       | 389          | None                                        |
| feedback_history    | Deque(maxlen=1000) for cross-agent learning signals.       | frontend/feedback_aggregator.py                     | 541          | Info on update_session(); structured_logger |
| connected           | List of active WebSocket client objects.                   | frontend/realtime_collaborator.py                   | 597          | None                                        |
| findings            | List of dictionaries extracted from the audit AST.         | toolkits/dependency/audit_engine.py                 | N/A          | None                                        |
| audit_state         | Shared JSON payload for cross-protocol grounding.          | toolkits/dependency/AUDIT_STATE_PAYLOAD.json        | N/A          | None                                        |
