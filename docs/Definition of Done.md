# Definition of Done (DoD)

**Objective:** To ensure a shared understanding of what it means for a work item to be complete, ensuring high quality and minimizing technical debt before code reaches production.

> **The Golden Rule**
> A User Story is not "Done" until it is **shippable**. If the code is written but not tested, it is not Done. If it is tested but not documented, it is not Done.

---

## 1. Universal Criteria
*All items, regardless of size or complexity, must meet these baseline requirements.*

*   [x] **Acceptance Criteria Met:** All conditions listed in the Jira/Linear ticket are satisfied.
*   [x] **No Critical Bugs:** The feature introduces no P0 or P1 issues. This includes ensuring robust error handling for unexpected inputs (e.g., non-numeric types for `add_two_numbers`).
*   [x] **Clean Merge:** The branch is merged into `develop` (or `main` for hotfixes) without conflicts.
*   [x] **CI/CD Passed:** The build pipeline (linting, static analysis, automated tests) is green. For Python projects, this includes checks like Flake8/Black for linting, Pylint for static analysis, and Pytest for unit/integration tests.

---

## 2. Role-Specific Responsibilities

To achieve "Done," each discipline must sign off on their specific domain.

### 🎨 For Designers (UX/UI)
*Before the ticket can move to QA:*
*Note: This section is primarily applicable for features with a user-facing interface. For purely backend utility functions like `add_two_numbers`, these checks are generally not relevant.*
*   [ ] **Visual Review:** Implementation matches the Figma/Sketch mockups (spacing, typography, colors).
*   [ ] **Interaction Review:** Hover states, transitions, and animations behave as specified.
*   [ ] **Mobile Responsiveness:** Layout adapts correctly to defined breakpoints (Mobile, Tablet, Desktop).
*   [ ] **Assets:** All SVGs and images are optimized and accessible (alt tags defined).

### 💻 For Developers
*Before creating the Pull Request:*
*   [x] **Unit Tests:** New features or changes must have corresponding unit tests, ensuring code coverage is maintained or increased (Target: >80%). For new components or utility functions like `add_two_numbers`, comprehensive unit tests are mandatory to cover happy paths and edge cases (e.g., string inputs, non-numeric inputs).
*   [x] **Code Cleanup:** No `print()` statements (use `logging` instead), commented-out code, or unused imports. All `logging.info` messages should be clear and utilize the `correlation_ID`.
*   [x] **Environment Variables:** No hardcoded secrets or keys; configuration variables (like `correlation_ID` if it were to vary per environment) and sensitive data are managed through environment variables or a secure configuration management system.
*   [x] **Peer Review:** At least one approval from a senior engineer; all PR comments resolved.

### 🕵️ For Testers (QA)
*Before moving ticket to "Ready for Release":*
*   [x] **Functional Testing:** The function's "Happy Path" (e.g., `add_two_numbers(1, 2)`) works as expected according to specifications.
*   [x] **Negative Testing:** Edge cases and error states (e.g., `add_two_numbers('a', 2)`, `add_two_numbers(None, 5)`) are handled gracefully and as per specification (e.g., returning an error, raising a specific exception).
*   [x] **Regression Check:** Existing features adjacent to this change still function correctly.
*   [ ] **Browser Compatibility:** Verified on Chrome, Firefox, Safari, and Edge (latest versions). *Applicable only for features with a web UI.*

### 👑 For Product Owners (PO)
*Final Verification:*
*   [x] **Business Value:** The feature solves the user problem as intended.
*   [x] **Demo:** The feature has been demonstrated in the Sprint Review (or distinct demo session).
*   [ ] **Documentation:** User guides or release notes have been updated (if applicable). This includes API documentation for functions like `add_two_numbers` if exposed externally.

---

## 3. Security & Performance (Non-Functional)
*Crucial for maintaining infrastructure integrity.*

| Check | Description |
| :--- | :--- |
| **Audit Logs** | Critical actions (e.g., function calls for sensitive operations) generate meaningful backend logs with traceable `correlation_ID`s, as demonstrated in `add_two_numbers`. |
| **Load Time** | Feature does not degrade page load speed (Lighthouse score > 90). *Primarily applicable for UI features or services with direct performance impact.* |
| **Security Scan** | `pip-audit`, Bandit, or SAST (Static Application Security Testing) tools show no high-severity vulnerabilities. |
| **Data Privacy** | No PII (Personally Identifiable Information) or sensitive operational data is leaked in logs (`correlation_ID`s are for tracing, not user identification), URLs, or directly exposed. |

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
> *   **Acceptance Criteria** are specific to *one* story (e.g., "User can click the blue button"). For `add_two_numbers`, an AC might be: "The function successfully adds two positive integers."
> *   **Definition of Done** applies to *every* story (e.g., "All functions must have comprehensive unit tests and utilize structured logging with `correlation_ID`s").