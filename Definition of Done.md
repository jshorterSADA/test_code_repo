```markdown
# Definition of Done (DoD)

**Objective:** To ensure a shared understanding of what it means for a work item to be complete, ensuring high quality and minimizing technical debt before code reaches production.

> **The Golden Rule**
> A User Story is not "Done" until it is **shippable**. If the code is written but not tested, it is not Done. If it is tested but not documented, it is not Done.



---

## 1. Universal Criteria
*All items, regardless of size or complexity, must meet these baseline requirements.*

* [ ] **Acceptance Criteria Met:** All conditions listed in the [Issue Tracker] ticket are satisfied.
* [ ] **No Critical Bugs:** The feature introduces no P0 or P1 issues.
* [ ] **Clean Merge:** The branch is merged into `develop` (or `main` for hotfixes) without conflicts.
* [ ] **CI/CD Passed:** The build pipeline (linting, compiling, automated tests) is green.

---

## 2. Role-Specific Responsibilities

To achieve "Done," each discipline must sign off on their specific domain.

### 🎨 For Designers (UX/UI)
*Before the ticket can move to QA:*
* [ ] **Visual Review:** Implementation matches the [Design Tool] mockups (spacing, typography, colors).
* [ ] **Interaction Review:** Hover states, transitions, and animations behave as specified.
* [ ] **Mobile Responsiveness:** Layout adapts correctly to defined breakpoints (Mobile, Tablet, Desktop).
* [ ] **Assets:** All SVGs and images are optimized and accessible (alt tags defined).

### 💻 For Developers
*Before creating the Pull Request:*
* [ ] **Unit Tests:** Code coverage is maintained or increased (Target: >80%).
* [ ] **Code Cleanup:** No `console.log`, commented-out code, or unused imports.
* [ ] **Environment Variables:** No hardcoded secrets or keys; config variables added to the deployment manager.
* [ ] **Peer Review:** At least one approval from a senior engineer; all PR comments resolved.

### 🕵️ For Testers (QA)
*Before moving ticket to "Ready for Release":*
* [ ] **Functional Testing:** The "Happy Path" works as expected.
* [ ] **Negative Testing:** Edge cases and error states (e.g., bad network, invalid input) are handled gracefully.
* [ ] **Regression Check:** Existing features adjacent to this change still function correctly.
* [ ] **Browser Compatibility:** Verified on Chrome, Firefox, Safari, and Edge (latest versions).

### 👑 For Product Owners (PO)
*Final Verification:*
* [ ] **Business Value:** The feature solves the user problem as intended.
* [ ] **Demo:** The feature has been demonstrated in the Sprint Review (or distinct demo session).
* [ ] **Documentation:** User guides or release notes have been updated (if applicable).

---

## 3. Security & Performance (Non-Functional)
*Crucial for maintaining infrastructure integrity.*

| Check | Description |
| :--- | :--- |
| **Audit Logs** | Critical actions (deletes, edits, payments) generate a backend log. |
| **Load Time** | Feature does not degrade page load speed (Lighthouse score > 90). |
| **Security Scan** | `npm audit` or SAST tools show no high-severity vulnerabilities. |
| **Data Privacy** | No PII (Personally Identifiable Information) is leaked in logs or URLs. |

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
> * **Acceptance Criteria** are specific to *one* story (e.g., "User can click the blue button").
> * **Definition of Done** applies to *every* story (e.g., "All buttons must have hover states").
```