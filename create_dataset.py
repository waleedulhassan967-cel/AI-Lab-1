import json
from pathlib import Path

rows = [
    ("late", "Late submission is normally penalized. Illness extensions require medical evidence before the deadline. Late submissions without prior extension approval incur a 10% daily grade deduction penalty up to 5 days maximum.",
     "Illness extensions require medical evidence before the deadline."),
    ("password", "Reset a forgotten password using the recovery link on the IT services self-service portal. Never share recovery codes or account passwords with anyone including IT support personnel.",
     "Reset a forgotten password using the recovery link."),
    ("assignment", "Upload assignments through the learning portal before midnight on the due date. Submit the final file as a PDF document. File sizes must not exceed 50 megabytes.",
     "Upload assignments through the learning portal."),
    ("contractor", "Contractors can work remotely only if the signed contract permits it. Employee rules do not apply to contractors. Access permissions are reviewed every quarter.",
     "Contractors can work remotely only if the signed contract permits it."),
    ("printer", "For blank printer pages, check ink levels and run the cleaning utility. Print a test page afterwards. Contact hardware support if the issue persists after two attempts.",
     "For blank printer pages, check ink levels and run the cleaning utility.")
]

docs = {doc: text for doc, text, evidence in rows}
evidence = {doc: e for doc, text, e in rows}

questions = [
    ("What is required for illness extensions?", "late", "dev"),
    ("How do I reset a forgotten password?", "password", "dev"),
    ("Where do I upload assignments?", "assignment", "dev"),
    ("Can contractors work remotely?", "contractor", "dev"),
    ("What do I do for blank printer pages?", "printer", "test"),
    ("How can I recover my login access?", "password", "test"),
    ("How should I hand in my coursework?", "assignment", "test"),
    ("What proof is needed when I was ill?", "late", "test"),
    ("What are tomorrow's flight prices?", None, "test"),
    ("Who won the football match?", None, "test")
]

queries = [dict(query=q, doc=doc, evidence=evidence[doc] if doc else None, split=split)
           for q, doc, split in questions]

for name, data in [("corpus.json", docs), ("queries.json", queries)]:
    p = Path(name)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Created {name}")
