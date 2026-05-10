from fastapi import APIRouter, Depends

from src.api.auth.auth import require_admin
from src.db.connection import get_connection

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get('/')
def get_my_audit_log(user: dict = Depends(require_admin)):
  """Returns the last 100 actions performed by the currently logged-in supervisor."""
  supervisor_id = user['sub']

  with get_connection() as conn:
    with conn.cursor() as cur:
      cur.execute(
        """
        SELECT audit_id, action, target_type, target_id, target_name, timestamp
        FROM audit_logs
        WHERE supervisor_id = %s
        ORDER BY timestamp DESC
        LIMIT 100
        """,
        (supervisor_id,),
      )
      rows = cur.fetchall()

  return [
    {
      "audit_id":    str(row[0]),
      "action":      row[1],
      "target_type": row[2],
      "target_id":   str(row[3]),
      "target_name": row[4],
      "timestamp":   row[5].isoformat(),
    }
    for row in rows
  ]
