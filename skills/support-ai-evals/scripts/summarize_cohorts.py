"""Compute cumulative repeat-contact cohorts from explicitly reviewed local data."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta
import json
from pathlib import Path


def timestamp(value, field):
    if not isinstance(value, str):
        raise ValueError(f"{field}: expected ISO timestamp")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field}: invalid ISO timestamp") from exc
    if result.tzinfo is None:
        raise ValueError(f"{field}: timezone required")
    return result


def nonempty(obj, key):
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key}: nonempty string required")
    return value


def fields(obj, allowed, label):
    if not isinstance(obj, dict):
        raise ValueError(f"{label}: object required")
    extra = set(obj) - set(allowed)
    if extra:
        raise ValueError(f"{label}: unknown fields {sorted(extra)}")


def summarize(data):
    fields(data, ["as_of", "coverage_scope", "records"], "input")
    as_of = timestamp(data.get("as_of"), "as_of")
    scope = nonempty(data, "coverage_scope")
    records = data.get("records")
    if not isinstance(records, list):
        raise ValueError("records: list required")
    normalized, originals, versions = [], set(), set()
    for r in records:
        fields(r, ["conversation_id", "account_id", "definition_version", "resolved_at",
                   "observed_through", "coverage", "returns", "confirmed_success_at"], "record")
        cid, aid = nonempty(r, "conversation_id"), nonempty(r, "account_id")
        if cid in originals:
            raise ValueError(f"duplicate original conversation: {cid}")
        originals.add(cid)
        versions.add(nonempty(r, "definition_version"))
        resolved = timestamp(r.get("resolved_at"), "resolved_at")
        through = timestamp(r.get("observed_through"), "observed_through")
        if not resolved <= through <= as_of:
            raise ValueError("require resolved_at <= observed_through <= as_of")
        coverage = r.get("coverage")
        if coverage not in ("complete", "partial", "unknown"):
            raise ValueError("invalid coverage")
        success = None
        if r.get("confirmed_success_at") is not None:
            success = timestamp(r["confirmed_success_at"], "confirmed_success_at")
            if not resolved <= success <= through:
                raise ValueError("confirmed success outside observed interval")
        returns = r.get("returns", [])
        if not isinstance(returns, list):
            raise ValueError("returns: list required")
        events = {}
        for event in returns:
            fields(event, ["event_id", "conversation_id", "account_id", "occurred_at",
                           "match", "reason"], "return")
            eid = nonempty(event, "event_id")
            nonempty(event, "conversation_id")
            if nonempty(event, "account_id") != aid:
                raise ValueError("return account does not match original account")
            nonempty(event, "reason")
            when = timestamp(event.get("occurred_at"), "occurred_at")
            if not resolved < when <= through:
                raise ValueError("return outside observed interval")
            match = event.get("match")
            if match not in ("confirmed", "uncertain", "unrelated"):
                raise ValueError("invalid match status")
            if eid in events and events[eid][2] != event:
                raise ValueError(f"conflicting duplicate event: {eid}")
            events[eid] = (when, match, event)
        normalized.append((resolved, through, coverage, success, list(events.values())))
    if len(versions) > 1:
        raise ValueError("mixed definition versions: split the cohorts before comparison")

    windows = {}
    for days in (7, 30):
        stats = dict(originals=len(records), mature=0, immature=0,
                     mature_incomplete_coverage=0, eligible=0,
                     confirmed_recurrence_originals=0, uncertain_match_originals=0,
                     possible_recurrence_originals=0, confirmed_return_events=0,
                     independently_confirmed_outcomes=0)
        for resolved, through, coverage, success, events in normalized:
            end = resolved + timedelta(days=days)
            if end > as_of:
                stats["immature"] += 1
                continue
            stats["mature"] += 1
            if coverage != "complete" or through < end:
                stats["mature_incomplete_coverage"] += 1
                continue
            stats["eligible"] += 1
            confirmed = sum(1 for when, match, _ in events if when <= end and match == "confirmed")
            uncertain = any(when <= end and match == "uncertain" for when, match, _ in events)
            stats["confirmed_recurrence_originals"] += bool(confirmed)
            stats["uncertain_match_originals"] += uncertain
            stats["possible_recurrence_originals"] += bool(confirmed or uncertain)
            stats["confirmed_return_events"] += confirmed
            stats["independently_confirmed_outcomes"] += success is not None and success <= end
        denominator = stats["eligible"]
        stats["no_observed_confirmed_return"] = denominator - stats["confirmed_recurrence_originals"]
        for name, count in [("confirmed_recurrence_rate", stats["confirmed_recurrence_originals"]),
                            ("possible_recurrence_upper_bound", stats["possible_recurrence_originals"])]:
            stats[name] = count / denominator if denominator else None
        windows[str(days)] = stats
    return dict(as_of=as_of.isoformat(), coverage_scope=scope,
                definition_version=next(iter(versions), None), windows=windows,
                interpretation="Cumulative windows; counts may overlap. No observed return is not proof of success.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = summarize(json.loads(args.input.read_text()))
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
