import copy
import importlib.util
from pathlib import Path
import unittest

PATH = Path(__file__).resolve().parents[1] / "skills/support-ai-evals/scripts/summarize_cohorts.py"
spec = importlib.util.spec_from_file_location("cohorts", PATH)
cohorts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cohorts)


def record(cid="a", resolved="2026-10-01T00:00:00Z"):
    return dict(conversation_id=cid, account_id="account", definition_version="v1",
                resolved_at=resolved, observed_through="2026-11-01T00:00:00Z",
                coverage="complete", returns=[])


def event(eid="e", when="2026-10-08T00:00:00Z", match="confirmed"):
    return dict(event_id=eid, conversation_id="followup", account_id="account",
                occurred_at=when, match=match, reason="Reviewed same issue")


def data(*records):
    return dict(as_of="2026-11-01T00:00:00Z", coverage_scope="Test channel", records=list(records))


class CohortTests(unittest.TestCase):
    def test_mature_boundaries_and_immature_exclusion(self):
        result = cohorts.summarize(data(record(), record("b", "2026-10-25T00:00:00Z"),
                                        record("c", "2026-10-30T00:00:00Z")))["windows"]
        self.assertEqual((result["7"]["eligible"], result["7"]["immature"]), (2, 1))
        self.assertEqual((result["30"]["eligible"], result["30"]["immature"]), (1, 2))

    def test_returns_count_original_once_and_windows_are_cumulative(self):
        r = record()
        r["returns"] = [event(), event("later", "2026-10-20T00:00:00Z")]
        result = cohorts.summarize(data(r))["windows"]
        self.assertEqual(result["7"]["confirmed_return_events"], 1)
        self.assertEqual(result["30"]["confirmed_return_events"], 2)
        self.assertEqual(result["30"]["confirmed_recurrence_originals"], 1)

    def test_identical_duplicate_event_is_deduplicated(self):
        r = record()
        r["returns"] = [event(), copy.deepcopy(event())]
        self.assertEqual(cohorts.summarize(data(r))["windows"]["30"]["confirmed_return_events"], 1)

    def test_uncertainty_and_success_can_overlap_with_recurrence(self):
        r = record()
        r["confirmed_success_at"] = "2026-10-02T00:00:00Z"
        r["returns"] = [event(match="uncertain")]
        w = cohorts.summarize(data(r))["windows"]["7"]
        self.assertEqual(w["confirmed_recurrence_rate"], 0)
        self.assertEqual(w["possible_recurrence_upper_bound"], 1)
        self.assertEqual(w["independently_confirmed_outcomes"], 1)
        self.assertEqual(w["uncertain_match_originals"], 1)

    def test_incomplete_coverage_and_no_denominator(self):
        r = record()
        r["coverage"] = "partial"
        w = cohorts.summarize(data(r))["windows"]["30"]
        self.assertEqual(w["mature_incomplete_coverage"], 1)
        self.assertIsNone(w["confirmed_recurrence_rate"])

    def test_observation_must_reach_window(self):
        r = record()
        r["observed_through"] = "2026-10-20T00:00:00Z"
        w = cohorts.summarize(data(r))["windows"]
        self.assertEqual(w["7"]["eligible"], 1)
        self.assertEqual(w["30"]["eligible"], 0)

    def test_invalid_inputs_rejected(self):
        samples = []
        r = record(); r["account_id"] = ""; samples.append(data(r))
        r = record(); r["resolved_at"] = "2026-10-01"; samples.append(data(r))
        r = record(); r["coverage"] = "probably"; samples.append(data(r))
        r = record(); r["returns"] = [event()]; r["returns"][0]["account_id"] = "other"; samples.append(data(r))
        r = record(); r["returns"] = [event(), event(match="uncertain")]; samples.append(data(r))
        r = record(); r["returns"] = [event(when="2026-11-02T00:00:00Z")]; samples.append(data(r))
        r = record("b"); r["definition_version"] = "v2"; samples.append(data(record(), r))
        samples.append(data(record(), record()))
        r = record(); r["sucess"] = True; samples.append(data(r))
        for sample in samples:
            with self.subTest(sample=sample), self.assertRaises(ValueError):
                cohorts.summarize(sample)

    def test_empty_input_does_not_invent_a_rate(self):
        w = cohorts.summarize(data())["windows"]["7"]
        self.assertEqual(w["eligible"], 0)
        self.assertIsNone(w["confirmed_recurrence_rate"])


if __name__ == "__main__":
    unittest.main()
