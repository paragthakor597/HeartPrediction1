import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

BASE = Path(__file__).parent
load_dotenv(BASE / ".env")

DATABASE_URL = os.environ["DATABASE_URL"]

mcp = FastMCP("heart-db")


@mcp.tool()
def saved_predictions(limit: int = 20) -> str:
    """Neon database mein save hui heart predictions dikhata hai — kis user ko risk mila aur kisko nahi."""
    limit = max(1, min(limit, 50))

    try:
        with psycopg.connect(DATABASE_URL) as conn:
            rows = conn.execute(
                """
                SELECT p.id, u.username, p.result, p.age, p.sex, p.created_at
                FROM heart_heartprediction p
                LEFT JOIN auth_user u ON u.id = p.user_id
                ORDER BY p.created_at DESC
                LIMIT %s
                """,
                (limit,),
            ).fetchall()
    except Exception as e:
        return f"Database se data nahi mil paya: {e}"

    if not rows:
        return "Abhi tak koi prediction save nahi hui."

    lines = ["ID | USER | RESULT | AGE | SEX | CREATED AT"]
    for pid, username, result, age, sex, created in rows:
        who = username or "guest"
        status = "Risk Detected" if result == 1 else "No Risk"
        gender = "Male" if sex == "M" else "Female"
        lines.append(f"#{pid} | {who} | {status} | {age} | {gender} | {created}")
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()