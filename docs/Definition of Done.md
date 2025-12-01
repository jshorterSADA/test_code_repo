
# Definition of Done (DoD)

**Objective:** To ensure a shared understanding of what it means for a work item to be complete, ensuring high quality and minimizing technical debt before code reaches production.

> **The Golden Rule**
> A User Story is not "Done" until it is **shippable**. If the code is written but not tested, it is not Done. If it is tested but not documented, it is not Done.

---

## 1. Universal Criteria
*All items, regardless of size or complexity, must meet these baseline requirements.*

* [ ] **Acceptance Criteria Met:** All conditions listed in the Jira/Linear ticket are satisfied.
* [ ] **No Critical Bugs:** The feature introduces no P0 or P1 issues.
* [ ] **Clean Merge:** The branch is merged into `develop` (or `main` for hotfixes) without conflicts.
* [ ] **CI/CD Passed:** The build pipeline (linting, compiling, automated tests) is green.

---

## 2. Role-Specific Responsibilities

To achieve "Done," each discipline must sign off on their specific domain.

### 💻 For Developers
*Before creating the Pull Request:*
* [ ] **Unit Tests:** Code coverage is maintained or increased (Target: >80%). _(Note: The current `addNums.py` file lacks dedicated unit tests, which should be prioritized for future development to meet this DoD.)_
* [ ] **Code Cleanup:** No `console.log`, commented-out code, or unused imports. _(The `addNums.py` file is generally clean in this regard, with logging used appropriately.)_
* [ ] **Environment Variables:** No hardcoded secrets or keys; config variables added to the deployment manager. _(The `correlation_ID` in `addNums.py` is currently hardcoded and should ideally be configurable or generated dynamically for production systems.)_
* [ ] **Peer Review:** At least one approval from a senior engineer; all PR comments resolved.

### 🕵️ For Testers (QA)
*Before moving ticket to "Ready for Release":*
* [ ] **Functional Testing:** The "Happy Path" works as expected (e.g., `add_two_numbers(1, 2)` returns `3`).
* [ ] **Negative Testing:** Edge cases and error states (e.g., non-numeric inputs like `add_two_numbers('a', 2)`) are handled gracefully, and appropriate errors or defaults are returned/logged. _(Currently, `add_two_numbers` will raise a `ValueError` for non-integer inputs, which should be explicitly tested. The docstring implies graceful handling, but the implementation does not currently catch these conversion errors internally.)_
* [ ] **Regression Check:** Existing features adjacent to this change still function correctly.

### 👑 For Product Owners (PO)
*Final Verification:*
* [ ] **Business Value:** The feature solves the user problem as intended.
* [ ] **Demo:** The feature has been demonstrated in the Sprint Review (or distinct demo session).
* [ ] **Documentation:** User guides or release notes have been updated (if applicable). _(The `add_two_numbers` function includes a docstring, which is a good starting point for internal documentation.)_

---

## 3. Security & Performance (Non-Functional)
*Crucial for maintaining infrastructure integrity.*

| Check | Description |
| :--- | :--- |
| **Audit Logs** | Critical actions (e.g., function calls, input conversions, results) generate backend logs with a `correlation_ID` for traceability. _(The `add_two_numbers` function successfully logs its operations with a provided correlation ID, meeting this aspect.)_ |
| **Load Time** | Feature does not degrade application performance. For simple utility functions like `add_two_numbers`, ensure minimal overhead. |
| **Security Scan** | Python dependency scans (`pip-audit`, `safety`, `bandit`) or SAST tools show no high-severity vulnerabilities. |
| **Data Privacy** | No PII (Personally Identifiable Information) is processed, leaked in logs or URLs. For utility functions like `add_two_numbers`, ensure only non-sensitive data (e.g., numerical inputs) is handled. |

---

## 4. Exception Handling
**What happens if a story is NOT Done at Sprint end?**

If a User Story fails to meet the DoD by the end of the Sprint:
1.  **Do not** demonstrate it at the Sprint Review.
2.  **Do not** push it to the release branch.
3.  **Move it** to the next Sprint (rollover) or back to the Backlog.
4.  **Retrospective:** Discuss *why* it wasn't finished (e.g., estimation error, blocking dependency).

> [!TIP]
> **"Done" vs. "Acceptance Criteria"**
> *   **Acceptance Criteria** are specific to *one* story (e.g., "User can click the blue button").
> *   **Definition of Done** applies to *every* story (e.g., "All buttons must have hover states").
