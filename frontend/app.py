"""
KiezMove frontend entry point.

The frontend will provide the user interface for the KiezMove
moving-in concierge.

It will communicate with the FastAPI backend rather than
accessing the database directly.

Frontend responsibilities:
- Collect information about the user's move.
- Display the user's personalized moving plan.
- Show task status and progress.
- Allow the user to complete or update tasks.

Backend responsibilities remain in backend/app/.
"""