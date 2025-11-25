# Branching Strategy

This document outlines the Git branching strategy employed for the codebase, ensuring a structured, collaborative, and efficient development workflow. The strategy is designed to support continuous integration and continuous delivery (CI/CD) practices, particularly for components deployed as cloud functions, while maintaining stability for production systems.

## 1. Core Principles

*   **Clarity and Consistency:** Provide clear guidelines for branch creation, naming, and merging to minimize confusion and maintain code integrity.
*   **Isolation:** Isolate ongoing development work, features, and fixes to prevent interference and regressions in stable environments.
*   **Reproducibility:** Enable easy recreation of any release version or hotfix application.
*   **Automation:** Integrate seamlessly with automated testing, building, and deployment processes.

## 2. Main Branches

Two primary branches form the core of the development history:

### 2.1 `main` (Production Ready)

*   **Purpose:** This branch reflects the latest stable, production-ready code. Commits to `main` should always be deployable.
*   **Access:** Direct commits to `main` are strictly forbidden. All changes must originate from other branches via pull requests that have undergone review and testing.
*   **Lifecycle:** Long-lived. Protected branch.
*   **Examples:** The `cloud_function_jira_processor` at the commit point of `main` is the version actively running in production.

### 2.2 `develop` (Integration Branch)

*   **Purpose:** This branch serves as an integration point for all new features and approved changes. It represents the upcoming release.
*   **Access:** Direct commits to `develop` are strictly forbidden. All changes must come from feature branches via pull requests.
*   **Lifecycle:** Long-lived. Protected branch.
*   **Examples:** All new development on the `add_two_numbers` utility or enhancements to the `cloud_function_jira_processor` would first integrate here.

## 3. Supporting Branches

Supporting branches are temporary branches used to facilitate parallel development, isolate features, and prepare for releases or urgent fixes.

### 3.1 Feature Branches

*   **Purpose:** To develop new features, enhancements, or significant refactorings. Each feature branch should address a single, well-defined task or user story.
*   **Origin:** Always branch off `develop`.
*   **Naming Convention:** `feature/<descriptive-name>` (e.g., `feature/add-sentiment-analysis-to-alerts`, `feature/handle-float-strings-in-addnums`).
*   **Merging:** Merge back into `develop` via a pull request after successful code review and testing. These merges should typically use a `--no-ff` (no fast-forward) merge to preserve history.
*   **Lifecycle:** Short-lived, deleted after merging.

### 3.2 Release Branches

*   **Purpose:** To prepare a new production release. This involves final testing, bug fixing specific to the release, and updating release-specific documentation (e.g., `PRODUCT_QUALITY_ALERT_STATUS.md` for a release status update).
*   **Origin:** Always branch off `develop` when `develop` contains the desired features for the next release.
*   **Naming Convention:** `release/<version-number>` (e.g., `release/1.0.0`, `release/2025.11.13`).
*   **Merging:**
    1.  Merge into `main` after all release-specific fixes are complete and release criteria are met. This merge should create a release tag.
    2.  Merge back into `develop` to ensure `develop` contains all release fixes.
*   **Lifecycle:** Short-lived, deleted after merging into `main` and `develop`.

### 3.3 Hotfix Branches

*   **Purpose:** To quickly address critical bugs in `main` (production) without waiting for the next scheduled release.
*   **Origin:** Always branch off `main`.
*   **Naming Convention:** `hotfix/<descriptive-name>` (e.g., `hotfix/fix-jira-api-credential-error`, `hotfix/log-injection-vulnerability`).
*   **Merging:**
    1.  Merge into `main` after successful code review and testing. This merge should create a new patch release tag.
    2.  Merge back into `develop` to ensure the fix is included in the next regular release.
*   **Lifecycle:** Short-lived, deleted after merging into `main` and `develop`.

## 4. Workflow Overview

1.  **Start a new feature/enhancement:**
    *   Create a feature branch from `develop`: `git checkout develop && git pull && git checkout -b feature/my-new-feature`
    *   Develop the feature, including any updates to utilities like `addNums.py` or the Cloud Function `main.py`.
    *   Test thoroughly (e.g., using `demo_log_examples.py` for `addNums.py` or local testing for `cloud_function_jira_processor`).
    *   Commit changes regularly to the feature branch.

2.  **Integrate a feature:**
    *   Open a pull request from `feature/my-new-feature` to `develop`.
    *   Request code reviews.
    *   Ensure all automated tests pass.
    *   Once approved, merge the pull request.
    *   Delete the feature branch.

3.  **Prepare for a release:**
    *   When `develop` is stable enough and contains desired features, create a release branch from `develop`: `git checkout develop && git pull && git checkout -b release/1.0.0`
    *   Perform final testing, documentation updates (e.g., `PRODUCT_QUALITY_ALERT_STATUS.md`, `README.md` for `cloud_function_jira_processor`), and minor bug fixes on the release branch.

4.  **Deploy to production (Release):**
    *   Open a pull request from `release/1.0.0` to `main`.
    *   Once approved, merge the pull request and immediately tag `main` with the version number (e.g., `v1.0.0`).
    *   Deploy the `main` branch to production (e.g., using `deploy.sh` for `cloud_function_jira_processor`).
    *   Merge the `release/1.0.0` branch back into `develop` to propagate any release-specific fixes.
    *   Delete the release branch.

5.  **Address a critical production bug (Hotfix):**
    *   Create a hotfix branch from `main`: `git checkout main && git pull && git checkout -b hotfix/critical-bug-fix`
    *   Implement the fix.
    *   Test thoroughly (e.g., using `test_jira_status.py` for JIRA issues).
    *   Open a pull request from `hotfix/critical-bug-fix` to `main`.
    *   Once approved, merge the pull request and immediately tag `main` with the new patch version (e.g., `v1.0.1`).
    *   Deploy the `main` branch to production.
    *   Merge `hotfix/critical-bug-fix` back into `develop`.
    *   Delete the hotfix branch.

## 5. Merge Strategy

*   **Feature to `develop`:** Use a standard merge commit (`--no-ff`) to preserve the history of feature branches.
*   **Release to `main`:** Use a standard merge commit (`--no-ff`) to create clear release points.
*   **Hotfix to `main`:** Use a standard merge commit (`--no-ff`).
*   **Release/Hotfix to `develop`:** Use a standard merge commit (`--no-ff`).

Squash merges are generally discouraged for feature branches to maintain granular history, but may be considered for very small, single-commit fixes. Rebase is generally avoided on shared branches to prevent rewriting history.

## 6. Automation and CI/CD

This branching strategy is designed to integrate tightly with CI/CD pipelines:

*   **Feature Branches:** Trigger unit and integration tests upon push.
*   **`develop` Branch:** Trigger comprehensive test suites, build artifacts, and potentially deploy to a staging environment (e.g., a test instance of `cloud_function_jira_processor`).
*   **`main` Branch:** Trigger full test suites, build production-ready artifacts, and automatically deploy to the production environment.
*   **Pull Requests:** Mandatory for all merges to `main` and `develop`, enforcing code review and automated checks.

By following these guidelines, the team ensures a consistent, high-quality, and efficient development process for all components of the system.