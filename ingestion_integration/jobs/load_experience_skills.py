# ingestion_integration/jobs/load_experience_skills.py
from ingestion_integration.lib.fs import stream_collection
from ingestion_integration.lib.pg import get_conn
from typing import List, Dict

def _clean_skills(val) -> List[str]:
    if val is None:
        return []
    if not isinstance(val, list):
        val = [val]
    out = []
    for s in val:
        if s is None:
            continue
        t = str(s).strip()
        if t:
            out.append(t)
    return out

def run():
    # Gather skills per experience from Firestore
    exp_to_skills: Dict[str, List[str]] = {}
    for snap in stream_collection("experiences"):
        d = snap.to_dict() or {}
        exp_id = snap.id
        skills = _clean_skills(d.get("skillsToLearn"))
        # We will also clear rows when skills list is empty to stay in sync
        exp_to_skills[exp_id] = skills

    if not exp_to_skills:
        print("[INFO] No experiences found.")
        return

    exp_ids = list(exp_to_skills.keys())

    with get_conn() as conn:
        with conn.cursor() as cur:
            # 1) Clear existing rows for these experiences to keep idempotency
            #    Use a VALUES table to delete in bulk
            cur.execute("""
                DELETE FROM dim_experience_skill des
                USING (SELECT UNNEST(%s::text[]) AS experience_id) AS t
                WHERE des.experience_id = t.experience_id;
            """, (exp_ids,))

            # 2) Insert current skills
            rows = []
            for eid, skills in exp_to_skills.items():
                for sk in skills:
                    rows.append((eid, sk))

            if rows:
                args_str = ",".join(["(%s,%s)"] * len(rows))
                # Flatten rows for execute call
                flat = [v for row in rows for v in row]
                cur.execute(
                    f"""
                    INSERT INTO dim_experience_skill(experience_id, skill)
                    VALUES {args_str}
                    ON CONFLICT (experience_id, skill) DO NOTHING;
                    """,
                    flat
                )
                print(f"[OK] Upserted {len(rows)} experience-skill row(s).")
            else:
                print("[INFO] No skills to insert after cleanup.")

        conn.commit()

if __name__ == "__main__":
    run()