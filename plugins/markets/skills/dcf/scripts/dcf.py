#!/usr/bin/env python3
"""DCF calculator (stdlib only).

Usage:
  python dcf.py --fcf 100,110,121 --wacc 0.10 --g 0.025 --net-debt 50 --shares 10
  python dcf.py --selftest

FCF are the explicit forecast years (year 1..N). Terminal value uses Gordon growth
on the last forecast year. --mid-year discounts flows (and the Gordon terminal value)
at t-0.5.
"""
import argparse
import sys


def dcf(fcf, wacc, g, net_debt=0.0, shares=None, mid_year=False):
    if wacc <= g:
        raise ValueError("WACC must be greater than g")
    n = len(fcf)
    shift = 0.5 if mid_year else 0.0
    pv_flows = sum(f / (1 + wacc) ** (t - shift) for t, f in enumerate(fcf, start=1))
    terminal = fcf[-1] * (1 + g) / (wacc - g)
    pv_terminal = terminal / (1 + wacc) ** (n - shift)
    ev = pv_flows + pv_terminal
    equity = ev - net_debt
    return {
        "pv_flows": pv_flows,
        "pv_terminal": pv_terminal,
        "ev": ev,
        "equity": equity,
        "per_share": equity / shares if shares else None,
        "terminal_share": pv_terminal / ev,
    }


def sensitivity(fcf, wacc, g, net_debt, shares, mid_year, step=0.01):
    """Rows = WACC -step/base/+step, columns = g -step/base/+step."""
    rows = []
    for w in (wacc - step, wacc, wacc + step):
        row = []
        for gg in (g - step, g, g + step):
            try:
                r = dcf(fcf, w, gg, net_debt, shares, mid_year)
                row.append(r["per_share"] if shares else r["equity"])
            except ValueError:
                row.append(None)
        rows.append((w, row))
    return rows


def selftest():
    # flat FCF of 100, WACC 10%, g 0: a 100/0.10 perpetuity, so EV must be exactly 1000
    r = dcf([100] * 5, 0.10, 0.0)
    assert abs(r["ev"] - 1000) < 1e-9, r
    assert abs(r["terminal_share"] - 620.9213230591552 / 1000) < 1e-9, r
    r = dcf([100] * 5, 0.10, 0.0, net_debt=200, shares=40)
    assert abs(r["equity"] - 800) < 1e-9 and abs(r["per_share"] - 20) < 1e-9, r
    try:
        dcf([100], 0.05, 0.05)
    except ValueError:
        pass
    else:
        raise AssertionError("wacc<=g must raise")
    print("selftest ok")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--fcf", help="comma separated free cash flows, year 1..N")
    p.add_argument("--wacc", type=float)
    p.add_argument("--g", type=float)
    p.add_argument("--net-debt", type=float, default=0.0)
    p.add_argument("--shares", type=float, help="diluted shares, same unit scale as FCF")
    p.add_argument("--mid-year", action="store_true")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        return selftest()
    if not (a.fcf and a.wacc is not None and a.g is not None):
        p.error("--fcf, --wacc and --g are required")
    fcf = [float(x) for x in a.fcf.split(",")]
    r = dcf(fcf, a.wacc, a.g, a.net_debt, a.shares, a.mid_year)
    print(f"PV of forecast flows : {r['pv_flows']:,.2f}")
    print(f"PV of terminal value : {r['pv_terminal']:,.2f}  ({r['terminal_share']:.0%} of EV)")
    print(f"Enterprise value     : {r['ev']:,.2f}")
    print(f"Equity value         : {r['equity']:,.2f}")
    if r["per_share"] is not None:
        print(f"Per share            : {r['per_share']:,.2f}")
    label = "per share" if a.shares else "equity value"
    print(f"\nSensitivity ({label}); rows=WACC, columns=g")
    gs = [a.g - 0.01, a.g, a.g + 0.01]
    print("WACC \\ g  " + "".join(f"{x:>11.1%}" for x in gs))
    for w, row in sensitivity(fcf, a.wacc, a.g, a.net_debt, a.shares, a.mid_year):
        print(f"{w:>8.1%}  " + "".join(f"{v:>11,.2f}" if v is not None else f"{'n/a':>11}" for v in row))
    if r["terminal_share"] > 0.75:
        print("\nWARNING: terminal value is over 75% of EV; the result rests on far-future assumptions.")


if __name__ == "__main__":
    sys.exit(main())
