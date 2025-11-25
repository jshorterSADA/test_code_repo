# Branching Strategy for the Product Quality Alert System

## 1. Introduction

This document outlines the branching strategy employed for the Product Quality Alert System codebase. A clear branching strategy is crucial for managing concurrent development, ensuring code stability, facilitating releases, and maintaining a high quality product. This strategy aims to provide a consistent and predictable workflow for all contributors.

The primary goal is to maintain a stable `main` branch reflecting the production state, while enabling agile development of new features and timely resolution of issues.

## 2. Core Branches

The following are the two core branches that form the foundation of our branching model:

*   **`main` (Production Branch)**
    *   **Purpose:** This branch contains the production-ready code. All code pushed to `main` must be stable, fully tested, and deployable.
    *   **Ownership:** Only maintainers or automated processes are permitted to merge directly into `main`.
    *   **Workflow:** Merges into `main` typically originate from `release` branches or `hotfix` branches. Each merge should correspond to a new version release.
    *   **Protection:** `main` is a protected branch; direct commits are forbidden. All changes must come via Pull Requests.

*   **`develop` (Integration Branch)**
    *   **Purpose:** This branch serves as an integration point for ongoing development. It accumulates new features and bug fixes that are not yet ready for production.
    *   **Ownership:** All feature branches are merged into `develop`.
    *   **Workflow:** `develop` is branched from `main` at the start of a major development cycle. It is the target for merging `feature` and `bugfix` branches.
    *   **Protection:** `develop` is a protected branch; direct commits are highly discouraged. All changes should come via Pull Requests.

## 3. Supporting Branches

Supporting branches are short-lived branches used to assist in the development of new features, bug fixes, or release preparations. They are always merged back into one of the core branches and then deleted.

### 3.1. Feature Branches

*   **Purpose:** To develop new features or significant enhancements in isolation.
*   **Naming Convention:** `feature/<JIRA-ID>-<short-description>`
    *   *Examples:* `feature/AITD-123-new-sentiment-model`, `feature/AITD-456-add-alert-notifications`
*   **Workflow:**
    1.  Branch off from `develop`.
    2.  Work on the feature, committing regularly.
    3.  Once complete and tested, submit a Pull Request to merge into `develop`.
    4.  Upon successful merge and deployment to staging/test environments, the feature branch is deleted.
*   **Best Practices:** Keep feature branches small and focused. Rebase frequently from `develop` to avoid large merge conflicts.

### 3.2. Bugfix Branches

*   **Purpose:** To address non-critical bugs found during development or in staging environments. These bugs are not urgent enough for a `hotfix`.
*   **Naming Convention:** `bugfix/<JIRA-ID>-<short-description>`
    *   *Examples:* `bugfix/AITD-789-pubsub-decode-error`, `bugfix/AITD-901-jira-description-format`
*   **Workflow:**
    1.  Branch off from `develop`.
    2.  Implement the fix, committing regularly.
    3.  Once fixed and tested, submit a Pull Request to merge into `develop`.
    4.  Upon successful merge, the bugfix branch is deleted.

### 3.3. Hotfix Branches

*   **Purpose:** To quickly address critical bugs in the `main` (production) branch. These fixes are deployed immediately.
*   **Naming Convention:** `hotfix/<JIRA-ID>-<short-description>`
    *   *Examples:* `hotfix/AITD-001-jira-api-down`, `hotfix/AITD-002-critical-log-error`
*   **Workflow:**
    1.  Branch off directly from `main`.
    2.  Implement the urgent fix, committing regularly.
    3.  Once fixed and thoroughly tested, submit a Pull Request to merge into `main`.
    4.  After merging into `main`, the changes *must also be merged into `develop`* to ensure the fix is included in the next release.
    5.  Upon successful merge into both `main` and `develop`, the hotfix branch is deleted.
*   **Tagging:** A version tag (e.g., `v1.0.1`) must be created on `main` upon completion of a hotfix.

### 3.4. Release Branches

*   **Purpose:** To prepare a new production release. This involves minor bug fixes, final polishing, and release-specific tasks (e.g., updating version numbers, generating changelogs).
*   **Naming Convention:** `release/<version-number>`
    *   *Examples:* `release/v1.0.0`, `release/v1.1.0`
*   **Workflow:**
    1.  Branch off from `develop` when `develop` has all the necessary features for the upcoming release.
    2.  No new features are added to release branches. Only bug fixes and release preparations are allowed.
    3.  Once the release branch is stable and ready, it is merged into `main`.
    4.  A version tag (e.g., `v1.0.0`) is created on `main` at the point of the merge.
    5.  The release branch *must also be merged back into `develop`* to carry forward any bug fixes made during the release preparation.
    6.  After merging into both `main` and `develop`, the release branch is deleted.

## 4. Pull Requests (PRs) and Code Reviews

All merges into `main` and `develop` *must* be done via Pull Requests (PRs). This ensures:

*   **Code Review:** At least one (and preferably two) peer code reviews are conducted to maintain code quality, catch potential issues, and share knowledge.
*   **Automated Checks:** Integration with CI/CD pipelines to run automated tests, linting, and other quality checks before merging.
*   **Traceability:** A clear record of changes, discussions, and approvals.

**PR Requirements:**
*   Clear title and description outlining the changes.
*   Link to relevant JIRA tickets.
*   Automated tests must pass.
*   At least one approval from a designated reviewer.

## 5. Tagging

*   **Purpose:** To mark specific points in the `main` branch history as significant (e.g., releases, hotfixes).
*   **Convention:** Tags follow Semantic Versioning (e.g., `v1.0.0`, `v1.0.1`, `v2.0.0`).
*   **Workflow:** Tags are created on the `main` branch after a successful release or hotfix merge.

## 6. Commit Message Guidelines

Clear and consistent commit messages are vital for understanding the history of the codebase.

*   **Format:** `Type(Scope): Subject`
    *   `Type`: `feat` (new feature), `fix` (bug fix), `docs` (documentation), `style` (formatting), `refactor` (code refactoring), `test` (adding tests), `chore` (maintenance, build process changes).
    *   `Scope` (Optional): The area of the codebase affected (e.g., `cloud-function`, `addnums`, `logging`, `jira`).
    *   `Subject`: A concise description of the change, in the imperative mood, starting with a capital letter, and not ending with a period.
*   **Body (Optional):** Provide a more detailed explanation of *why* the change was made and *what* it accomplishes. Link to JIRA tickets (e.g., `Ref: AITD-123`).
*   **Example:**
    ```
    feat(cloud-function): Implement JIRA ticket creation for alerts

    This commit introduces the `create_product_quality_ticket` function
    to automate JIRA ticket creation based on Pub/Sub alerts.
    It integrates with Secret Manager for JIRA API key retrieval and
    formats the ticket description comprehensively.

    Ref: AITD-123
    ```

## 7. Conclusion

Adhering to this branching strategy ensures a streamlined and robust development process for the Product Quality Alert System. It enables parallel development, provides a clear path for production releases, and facilitates rapid responses to critical issues, all while maintaining a high standard of quality and collaboration.