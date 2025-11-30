# Definition of Done (DoD)

**Objective:** To ensure a shared understanding of what it means for a work item to be complete, ensuring high quality and minimizing technical debt before code reaches production.

> **The Golden Rule**
> A User Story is not "Done" until it is **shippable**. If the code is written but not tested, it is not Done. If it is tested but not documented, it is not Done.

---

## 1. Universal Criteria
*All items, regardless of size or complexity, must meet these baseline requirements.*

*   [ ] **Acceptance Criteria Met:** All conditions listed in the Jira/Linear ticket are satisfied.
*   [ ] **No Critical Bugs:** The feature introduces no P0 or P1 issues.
*   [ ] **Clean Merge:** The branch is merged into `develop` (or `main` for hotfixes) without conflicts.
*   [ ] **CI/CD Passed:** The build pipeline (linting, automated tests) is green.

---

## 2. Role-Specific Responsibilities

To achieve "Done," each discipline must sign off on their specific domain.

### 💻 For Developers
*Before creating the Pull Request:*
*   [ ] **Unit Tests:** Code coverage is maintained or increased (Target: >80%).
*   [ ] **Code Cleanup:** No `print()` statements used for logging (use the `logging` module as implemented), commented-out code, or unused imports.
*   [ ] **Environment Variables:** No hardcoded secrets or keys; configuration variables (e.g., `correlation_ID` for production environments) are dynamically loaded or added to the deployment manager. The `correlation_ID` should not be hardcoded in the source file as `correlation_ID = "..."`.
*   [ ] **Peer Review:** At least one approval from a senior engineer; all PR comments resolved.

### 🕵️ For Testers (QA)
*Before moving ticket to "Ready for Release":*
*   [ ] **Functional Testing:** The "Happy Path" works as expected (e.g., `add_two_numbers(1, 2)` returns `3`).
*   [ ] **Negative Testing:** Edge cases and error states (e.g., `add_two_numbers('a', 2)`, `add_two_numbers(None, 2)`) are handled gracefully, preventing unexpected crashes or `ValueError` exceptions when attempting `int()` conversion.
*   [ ] **Regression Check:** Existing features adjacent to this change still function correctly.

### 👑 For Product Owners (PO)
*Final Verification:*
*   [ ] **Business Value:** The feature solves the user problem as intended.
*   [ ] **Demo:** The feature has been demonstrated in the Sprint Review (or distinct demo session).
*   [ ] **Documentation:** User guides or release notes have been updated (if applicable). The function's docstring is clear and up-to-date.

---

## 3. Security & Performance (Non-Functional)
*Crucial for maintaining infrastructure integrity.*

| Check | Description |
| :--- | :--- |
| **Audit Logs** | Critical actions (e.g., function calls, input values, results) generate a backend log with an appropriate `correlation_ID` for traceability, following the `correlation_ID:ID message` format for errors and `ID - message` for info. |
| **Performance** | Basic operations do not introduce significant latency. For calculation functions, response times are within acceptable limits. |
| **Security Scan** | `pip audit` or SAST (Static Application Security Testing) tools show no high-severity vulnerabilities in dependencies or custom code. |
| **Data Privacy** | No PII (Personally Identifiable Information) is leaked in logs, URLs, or return values. |

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