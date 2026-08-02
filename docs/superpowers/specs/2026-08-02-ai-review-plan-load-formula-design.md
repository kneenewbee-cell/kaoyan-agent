# AI Review Plan Load Formula And Prompt Design

## Purpose

The AI review planner should stop treating every question as the same unit of work. A daily plan must keep the user's workload steady, while still respecting that a single-choice question, a proof question, a wrong question, and an unfinished practice sheet have very different effort.

This design adds a deterministic local load model before the AI call. The AI should choose and explain tasks from precomputed candidates; it should not guess timing, invent question splits, or mutate practice sheets.

## Decisions

1. Keep user-facing practice sheets intact.
2. Compute workload from the questions inside each task.
3. Split oversized practice sheets only at the planning-segment layer.
4. Balance days by `load_units` and `estimated_minutes`, not raw task count.
5. Send compact load-aware candidates to the AI prompt.
6. Validate AI output against the provided candidates and local load rules.

The system still recommends a planning mode first, explains why, and lets the user switch modes manually. There is no weekday/weekend distinction in this version.

## Non-Goals

This design does not introduce a new database engine, real multi-user permission changes, natural-language material retrieval, or a broad `qa/` refactor. It does not change the original practice-sheet entity into many new practice sheets.

## Load Formula

Per-question load:

```text
question_load_units =
  clamp(question_type_weight * state_weight * difficulty_weight, 0.55, 2.8)
```

Task load:

```text
task_load_units =
  sum(question_load_units) + task_overhead_units
```

Estimated time:

```text
estimated_minutes =
  round(task_load_units * 7.2)
```

The first version should store these constants together instead of scattering magic numbers through the planner.

### Question Type Weights

```text
true_false:      0.8
single_choice:   1.0
choice:          1.0
fill_blank:      1.1
solution:        1.8
proof:           2.2
comprehensive:   2.5
unknown:         1.0
```

### State Weights

```text
mastered_review:       0.65
unstarted:             1.0
learning:              1.0
draft_unanswered:      1.08
pending_review:        1.2
favorite_unmastered:   1.15
wrong:                 1.4
repeat_wrong:          1.6
unknown:               1.0
```

### Difficulty Weights

```text
easy:       0.85
medium:     1.0
unknown:    1.0
hard:       1.25
very_hard:  1.45
```

Difficulty is not reliable enough to be a primary filter yet. Unknown difficulty should stay neutral.

### Task Overhead

```text
single_question:       0 units
practice_set:          4 minutes / 7.2
continue_draft:        4 minutes / 7.2
topic_review:          8 minutes / 7.2
review_batch:          3 minutes / 7.2
```

Overhead represents task switching, opening the sheet, checking context, and marking progress. It should be small enough that question composition remains the main signal.

## Practice Sheet Model

Practice sheets remain whole at the source-data layer:

```text
practice_set_id
title
question_ids
created_from_filter
created_by_user
order
status
```

Planning creates segments that point back to the original sheet:

```text
plan_segment_id
parent_practice_set_id
part_index
part_count
planned_question_ids
load_units
estimated_minutes
status
```

The UI should present the parent title plus segment position:

```text
Limit Practice Sheet - Part 1/4
Limit Practice Sheet - Part 2/4
```

Completing a segment updates the included question attempts and rolls up progress to the original practice sheet, for example `18/40 completed`.

## Split Rules

Let:

```text
daily_target_units = constraints.daily_minutes / 7.2
```

Rules:

```text
if task_load_units <= daily_target_units * 1.15:
  keep as one planning item

if task_load_units > daily_target_units * 1.15 and the item has question_ids:
  split by question order into planning segments near daily_target_units

if the parent task exceeds the whole plan capacity:
  schedule only the segments that fit this plan
  mark remaining segments as later_pending

if the user explicitly chooses "finish whole sheet":
  allow the whole sheet, but show an overload warning
```

Splitting does not delete or rewrite the original practice sheet.

## Candidate Payload To AI

The AI prompt should receive compact candidates, not full question text. Each candidate or segment should include:

```text
candidate_id
candidate_type
title
source_ids
question_count
question_type_mix
state_mix
difficulty_mix
load_units
estimated_minutes
priority_score
splittable
parent_practice_set_id
part_index
part_count
mode_fit_reason
```

Full question text, answers, and explanations are not needed for planning. They should be loaded later only for solving or explanation flows.

## Prompt Changes

The AI planning prompt should be rewritten around these constraints:

1. Use `load_units` and `estimated_minutes` from candidates as the source of truth.
2. Keep each day's total estimated minutes close to `constraints.daily_minutes`.
3. Keep daily workload steady across all days; do not balance by raw task count alone.
4. Only output candidate IDs and source IDs that appear in the provided context.
5. Do not invent question IDs, practice sheets, dates, or task types.
6. Do not split practice sheets yourself. Use precomputed segment candidates.
7. Preserve `parent_practice_set_id`, `part_index`, and `part_count` when a selected item is a segment.
8. Follow `constraints.mode` and `policy.intent`.
9. If the selected mode lacks enough data, keep the requested days but return empty or light items with a warning that suggests the recommended mode.
10. The output is a draft only and must not claim it has written review tasks.

The output JSON should include segment metadata:

```json
{
  "plan_id": "...",
  "model": "...",
  "days": [
    {
      "date": "YYYY-MM-DD",
      "items": [
        {
          "type": "draft_attempts",
          "title": "Limit Practice Sheet - Part 1/4",
          "reason": "This segment is close to today's target load and should continue the original practice sheet.",
          "estimated_minutes": 58,
          "load_units": 8.1,
          "source_ids": ["candidate_or_segment_id"],
          "parent_practice_set_id": "practice_set_...",
          "part_index": 1,
          "part_count": 4
        }
      ]
    }
  ],
  "warnings": []
}
```

## Local Validation

The local normalizer should remain stricter than the model:

1. Reject items whose `source_ids` are not present in context.
2. Reject items whose candidate type is disabled by mode policy.
3. Recompute `load_units` and `estimated_minutes` from candidate lookup.
4. Rebalance days by recomputed load.
5. Deduplicate by segment ID, not only by parent practice sheet ID.
6. Allow multiple segments from the same parent sheet if they have different `plan_segment_id` values.
7. Prevent a later segment from being scheduled before an earlier unfinished segment unless the user explicitly changes order.

## Frontend Behavior

The planning UI should show:

```text
mode recommendation + reason
user-selectable mode switcher
daily minutes
daily raw question count
daily load bar
practice sheet segment label
remaining parent-sheet progress
overload warnings
```

The UI should not imply that a segmented plan created separate practice sheets. It should show the parent sheet and the current part.

## Test Coverage

Add tests for:

1. Type/state/difficulty load calculation.
2. Unknown difficulty staying neutral.
3. Oversized practice sheet segmentation.
4. Parent practice sheet remains intact after segmentation.
5. Multiple segments from the same parent are allowed when segment IDs differ.
6. AI output cannot invent candidates.
7. AI output cannot schedule disabled mode types.
8. Rebalancing uses recomputed load, not model-estimated minutes.
9. Short-budget users do not receive oversized daily segments.
10. Large practice sheets that exceed the whole cycle leave later pending segments.

## Migration Path

1. Add the load calculator and segmentation helpers behind local planner utilities.
2. Enrich AI candidates with load fields and segment metadata.
3. Update the prompt.
4. Update normalization and validation.
5. Update frontend labels for load and practice-sheet parts.
6. Extend evaluator personas to include real segment metrics.

The first implementation should keep existing APIs compatible by making new fields additive.
