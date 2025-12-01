
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
* [ ] **Unit Tests:** Code coverage is maintained or increased (Target: >80%). _(The `add_two_numbers` function requires unit tests to ensure correct behavior and error handling.)_
* [ ] **Code Cleanup:** No debug `print` statements, commented-out code, or unused imports are left in the final code.
* [ ] **Configuration Variables:** No hardcoded secrets or sensitive keys; configuration variables (e.g., default `correlation_ID` or other system parameters) are loaded from appropriate, secure sources (e.g., environment variables, config files). _(The current `correlation_ID` is hardcoded.)_
* [ ] **Peer Review:** At least one approval from a senior engineer; all PR comments resolved.

### 🕵️ For Testers (QA)
*Before moving ticket to "Ready for Release":*
* [ ] **Functional Testing:** The "Happy Path" works as expected (e.g., `add_two_numbers(1, 2)` successfully returns `3`).
* [ ] **Negative Testing:** Edge cases and error states (e.g., non-numeric inputs like `"a"`, `None`, or large numbers causing overflow) are handled gracefully, providing appropriate logging or raising informative exceptions. _(The `add_two_numbers` function needs robust error handling for invalid input types.)_
* [ ] **Regression Check:** Existing features adjacent to this change still function correctly.
* [ ] **Platform Compatibility:** If applicable, verified on specified Python versions or operating system environments.

### 👑 For Product Owners (PO)
*Final Verification:*
* [ ] **Business Value:** The feature solves the user problem as intended.
* [ ] **Demo:** The feature has been demonstrated in the Sprint Review (or distinct demo session).
* [ ] **Documentation:** Code comments (docstrings), logging standards, or external documentation (e.g., API specifications, user guides) have been updated (if applicable). _(The `add_two_numbers` function includes a docstring, which should be maintained and kept accurate.)_

---

## 3. Security & Performance (Non-Functional)
*Crucial for maintaining infrastructure integrity.*

| Check | Description |
| :--- | :--- |
| **Audit Logs** | Critical actions (e.g., function calls, conversions, errors, results) generate appropriate logs with correlation IDs for traceability and debugging. _(The `add_two_numbers` function already implements correlation ID logging for info and error messages.)_ |
| **Performance Impact** | Feature does not degrade overall system performance or introduce unnecessary computational overhead. For simple functions like `add_two_numbers`, efficiency is assumed, but for more complex logic, profiling may be needed. |
| **Security Scan** | Python package audits (e.g., `pip-audit` or similar tools) or Static Application Security Testing (SAST) tools show no high-severity vulnerabilities introduced by new or updated dependencies. |
| **Data Privacy** | No PII (Personally Identifiable Information) or sensitive data is leaked in logs, outputs, or error messages. |

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
> *   **Definition of Done** applies to *every* story (e.g., "All functions must have proper error handling and logging").
