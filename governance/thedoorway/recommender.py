# governance/thedoorway/recommender.py

class ProtocolRecommender:
    """
    Intelligence Layer for the Doorway Protocol.
    Analyzes drift and structural status to recommend specific governance protocols.
    """

    def recommend(self, drift: dict) -> list:
        """Schedules specific SEQ files based on detected workspace drift."""
        recs = []
        if drift.get("new"):
            recs.append(
                {
                    "id": "SEQ-SUBSTRATE-HEALTH",
                    "reason": f"New directories detected ({', '.join(drift['new'][:2])}). Verify architectural alignment.",
                }
            )
        if drift.get("unowned"):
            recs.append(
                {
                    "id": "SEQ-SUBSTRATE-HYGIENE",
                    "reason": "Unowned folders found. Update FOLDER_OWNERSHIP.md to prevent logic bloat.",
                }
            )
        return recs
