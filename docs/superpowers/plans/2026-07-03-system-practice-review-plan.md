# System Practice And Review Plan

> Goal: implement two complete loops for the system question library only:
> "生成同类训练" and "加入复习规划".
>
> Scope guard: do not move or rewrite `data/raw`, do not change the materials ingest pipeline, and do not alter unrelated QA behavior.

## Decisions

- Store user-created practice sets and review tasks in the existing user layer under `data/users/{user_id}/system_library/`.
- Keep system questions read-only. Practice sets and review tasks only reference system question ids.
- Generate similar practice deterministically from metadata: topic overlap first, then same type/library bonuses. Do not call an LLM for live matching.
- Review planning is separate from mastery status. A question can be `learning` and also have a pending review task.
- First UI loop uses the system question drawer as the primary entry. Plan page shows pending/completed review tasks.

## API Shape

- `POST /api/materials/system/practice-sets`
- `GET /api/materials/system/practice-sets`
- `GET /api/materials/system/practice-sets/{practice_set_id}`
- `DELETE /api/materials/system/practice-sets/{practice_set_id}`
- `POST /api/materials/system/review-tasks`
- `GET /api/materials/system/review-tasks`
- `PATCH /api/materials/system/review-tasks/{review_task_id}`
- `DELETE /api/materials/system/review-tasks/{review_task_id}`

## Tasks

- [ ] Backend tests
  - [ ] Similar-question generation excludes the source question.
  - [ ] Similar-question generation ranks by shared topics and same type.
  - [ ] Mastered questions can be excluded from generated practice.
  - [ ] Practice sets persist under the user layer and can be listed/deleted.
  - [ ] Review tasks persist under the user layer and can be listed/updated/deleted.

- [ ] Backend implementation
  - [ ] Add a focused system practice/review service module.
  - [ ] Add a focused API router for practice sets and review tasks.
  - [ ] Include the router in the local web server without changing existing routes.

- [ ] Frontend tests
  - [ ] Remove aborted formula-note tests from the previous paused task.
  - [ ] Assert drawer actions use real practice/review handlers, not placeholder alerts.
  - [ ] Assert the practice modal exposes count, same-type, exclude-mastered, preview, and create action.
  - [ ] Assert the review modal exposes due date, priority, note, and save action.
  - [ ] Assert the plan page renders review task sections and task actions.

- [ ] Frontend implementation
  - [ ] Replace drawer placeholder actions for "生成同类训练" and "加入复习规划".
  - [ ] Add practice generation modal and created-practice-set panel.
  - [ ] Add review planning modal.
  - [ ] Add a simple review-plan workbench on the existing planning page.
  - [ ] Keep current system-library list, drawer, and tutor behavior unchanged.

- [ ] Verification
  - [ ] Run targeted backend tests.
  - [ ] Run targeted frontend/static tests.
  - [ ] Run compile checks for touched Python modules.
  - [ ] Smoke-test the local page if the server starts cleanly.

