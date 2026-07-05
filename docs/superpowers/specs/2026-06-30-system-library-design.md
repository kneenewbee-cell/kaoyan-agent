# System Library Design

## Scope

The system library adds a read-only public question/knowledge library inside the existing `资料库` page.

First version scope:

- Keep the left navigation at four entries: `考研问答`, `资料库`, `复习规划`, `院校查询`.
- Rename the left navigation entry from `我的资料库` to `资料库`.
- Inside `资料库`, add a first-level switch: `我的资料` / `系统资料`.
- For `系统资料`, support subjects: `数学`, `政治`, `英语`, `408`, `其他`.
- For each subject, support content types: `习题` / `知识点`.
- Implement the first real data source for math questions from existing local `math1` question cards.
- Keep `difficulty` as a placeholder field only.

## Data Boundary

System content is public and read-only:

- question text
- answer
- explanation
- topics
- source metadata
- assets
- year
- question type
- library name

User state is separate and per user:

- `mastery_status`: `not_started`, `learning`, `mastered`
- `is_favorite`
- `in_wrong_book`
- `personal_note`
- future: `last_practiced_at`, `review_due_at`

The first frontend version may keep user state in browser memory. A persistent repository can be added later without changing the system question API.

## Layout

The `资料库` page becomes a fixed application shell:

- Left sidebar remains fixed.
- Main materials page does not scroll as a whole.
- The system question list scrolls inside its own region.
- The right question drawer scrolls inside its own region.
- Pagination appears below the question list.

System question list:

- Compact title: `资料库`.
- No explanatory helper text in the page header.
- Top-level switch: `我的资料` / `系统资料`.
- Subject switch: `数学`, `政治`, `英语`, `408`, `其他`.
- Content switch: `习题`, `知识点`.
- Filters: library name, year, topic, question type, personal status, keyword.
- Question cards show source, year/question number, type, status, and compact preview.
- `查看` opens the right drawer.
- Checkbox is only for batch actions.

Right drawer:

1. Drawer header with current question title and close button.
2. Mastery status.
3. Personal marks.
4. Question detail.
5. Folded `答案` and `解析` sections, Obsidian-style.
6. Personal note.
7. Actions: ask AI, generate similar exercise, add to plan, jump to knowledge point.

## Feature Closure

`查看`:

- Entry: question card action.
- Result: opens the right drawer for that question.
- Cancel: close drawer.
- Data: no data changes.

Mastery status:

- Entry: right drawer, list quick action, future batch action.
- Result: updates current user's `mastery_status`.
- Complete state: list status tag, drawer selected state, future statistics.
- Reverse: choose another mastery status.
- System layer: unchanged.

Favorite:

- Entry: list card, drawer personal marks.
- Result: toggles `is_favorite`.
- Complete state: list mark, drawer mark, favorite filter.
- Reverse: click again.
- System layer: unchanged.

Wrong book:

- Entry: list card, drawer personal marks, batch action.
- Result: toggles `in_wrong_book`.
- Complete state: list mark, drawer mark, wrong-book filter.
- Reverse: click again.
- System layer: unchanged.

Personal note:

- Entry: drawer note editor.
- Result: updates `personal_note`.
- Complete state: drawer text and `备注` mark.
- Reverse: clear note.
- System layer: unchanged.

Question answer/explanation:

- Entry: folded sections inside drawer question detail.
- Result: expands or collapses local display.
- Complete state: open fold state only.
- Reverse: collapse fold.
- System layer and user layer: unchanged.

## First Implementation Slice

The first implementation should ship the smallest useful vertical slice:

1. Backend read-only service and API for math system questions.
2. Backend static asset route for question images.
3. Frontend `资料库` switch between existing user materials and new system materials.
4. System question list with filtering, keyword search, pagination, and right drawer.
5. In-memory user state for mastery/favorite/wrong-book/note.

Out of scope for the first implementation:

- Persistent database for user state.
- Real multi-user permissions.
- Natural-language library assistant.
- Question editing.
- Difficulty labeling.
- Production knowledge-point pages.
