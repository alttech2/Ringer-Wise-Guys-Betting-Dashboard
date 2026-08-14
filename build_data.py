#!/usr/bin/env python3
"""Read wiseguys_tracker.xlsx (Best Bets tab) and emit data.json for the dashboard.

The spreadsheet is the source of truth. Edit + grade there, then run:
    python3 build_data.py
...and redeploy. The dashboard reads only the generated data.json at runtime.
"""
import json, datetime, sys
from pathlib import Path
import openpyxl

SRC = Path(__file__).parent / "wiseguys_tracker.xlsx"
OUT = Path(__file__).parent / "data.json"

def net_units(odds, result):
    """Net units on a 1u stake: profit on a win, -1 on a loss, 0 on a push."""
    if result == "P": return 0.0
    if result == "L": return -1.0
    if result == "W":
        o = int(str(odds).replace("+", "").replace(" ", ""))
        return round(o/100 if o > 0 else 100/abs(o), 2)
    return None  # ungraded

def main():
    wb = openpyxl.load_workbook(SRC, data_only=False)
    ws = wb["Best Bets"]
    headers = [c.value for c in ws[1]]
    idx = {h: i for i, h in enumerate(headers)}
    need = ["Date", "Host", "Bet", "Type", "Odds", "Result", "League"]
    for n in need:
        if n not in idx:
            sys.exit(f"Missing column '{n}' in Best Bets tab")

    bets, dates = [], []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or not row[idx["Date"]]:
            continue
        res = (row[idx["Result"]] or "").strip().upper()
        odds = str(row[idx["Odds"]]).strip()
        if res in ("W", "L", "P"):
            result, net = res, net_units(odds, res)
        elif res == "PENDING":
            result, net = "Pending", None   # published but not settled
        else:
            continue  # blank / ungraded
        bets.append({
            "date":   str(row[idx["Date"]]).strip(),
            "host":   str(row[idx["Host"]]).strip(),
            "type":   str(row[idx["Type"]]).strip(),
            "sport":  str(row[idx["League"]]).strip(),
            "bet":    str(row[idx["Bet"]]).strip(),
            "odds":   odds,
            "result": result,
            "net":    net,
        })
        dates.append(str(row[idx["Date"]]).strip())

    data = {
        "meta": {
            "generated": datetime.date.today().isoformat(),
            "range": f"{dates[0]}\u2013{dates[-1]}" if dates else "",
            "count": len(bets),
            "source": "wiseguys_tracker.xlsx",
        },
        "bets": bets,
    }
    OUT.write_text(json.dumps(data, indent=2))
    print(f"Wrote {OUT.name}: {len(bets)} best bets published ({data['meta']['range']})")

if __name__ == "__main__":
    main()
