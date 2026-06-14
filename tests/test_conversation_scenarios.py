from __future__ import annotations

import json
import unittest
from pathlib import Path


class ConversationScenarioDefinitionsTest(unittest.TestCase):
    def test_multiturn_scenarios_cover_required_followup_shapes(self) -> None:
        path = Path(__file__).with_name("conversation_scenarios.json")
        scenarios = json.loads(path.read_text(encoding="utf-8"))
        names = {item["name"] for item in scenarios}
        self.assertIn("concept_to_exam_to_three_layer_step_followup", names)
        self.assertIn("parallel_root_followup", names)
        self.assertIn("omitted_parameter_inheritance", names)

        deep = next(item for item in scenarios if item["name"] == "concept_to_exam_to_three_layer_step_followup")
        self.assertGreaterEqual(deep["expected"].count("explain_math_step"), 3)

        parallel = next(item for item in scenarios if item["name"] == "parallel_root_followup")
        self.assertGreaterEqual(len(parallel["turns"]), 4)

        omitted = next(item for item in scenarios if item["name"] == "omitted_parameter_inheritance")
        self.assertIn("x=1", omitted["turns"][-1])


if __name__ == "__main__":
    unittest.main()
