# Software Licensing & Intellectual Property Standards

**Effective Date:** 2023-11-20
**Owner:** Legal & Engineering Leadership

This document defines the strict protocols regarding the creation, usage, and protection of software assets within this repository. It serves as a binding guideline for all employees, contractors, and third-party vendors contributing to the Core Number Addition Service.

---

## 1. The Core Mandate

All code, architecture, designs, documentation, and algorithms contained within this repository are the exclusive property of **Your Organization**.

> **⛔ STRICT PROHIBITION**
>
> Your Organization Intellectual Property (IP) is **not to be used, reproduced, recreated, or distributed** in any other software projects, personal portfolios, public presentations, or AI training models without the **express written consent** of Your Organization Legal Council.

This includes, but is not limited to:
* Custom business logic and algorithms.
* UI/UX Design Systems and component libraries.
* Internal API schemas and data structures.
* Infrastructure as Code (Terraform/Helm) configurations.

---

## 2. Code Classification

To ensure compliance, we classify code into three distinct categories. You must understand which category your work falls under.

| Category | Definition | Usage Rights |
| :--- | :--- | :--- |
| **Proprietary** | Code written specifically for this project by our team. | **Strictly Internal.** No external sharing. |
| **Permissive OSS** | Open Source libraries (e.g., MIT, Apache 2.0, BSD). | Free to use, must preserve copyright headers. |
| **Copyleft / Viral** | Restrictive Open Source (e.g., GPL, AGPL). | **PROHIBITED.** Do not import these libraries. |

---

## 3. Open Source Compliance

While we leverage Open Source Software (OSS) to accelerate development, we must protect Your Organization's IP from "viral" licensing contamination.

### Approved Licenses
You may freely add dependencies that use the following licenses:
* MIT
* Apache 2.0
* BSD-3-Clause / BSD-2-Clause
* ISC

### Prohibited Licenses (The "Kill List")
**Do not** introduce dependencies with the following licenses without direct legal approval, as they may legally force us to open-source our proprietary code:
* **GPL (v2 or v3)** - General Public License
* **AGPL** - Affero General Public License
* **LGPL** - Lesser General Public License (Subject to dynamic linking rules)
* **CC-BY-SA** - Creative Commons ShareAlike

> [!WARNING]
> **Dependency Scanning**
> Our CI/CD pipeline runs a license audit on every Pull Request.
> `Error: Found restricted license (GPLv3) in package 'example-lib'. Build Failed.`

---

## 4. Acceptable Use Guidelines

### ✅ You Can:
* Use generic coding patterns (e.g., standard React hooks, factory patterns) in future projects, provided no proprietary business logic is included.
* Contribute bug fixes back to *external* Open Source libraries used in the project (e.g., fixing a typo in a React library), provided no Your Organization IP is revealed in the PR.

### ❌ You Cannot:
* **Copy/Paste:** Do not copy code blocks from this repo into personal GitHub Gists or StackOverflow questions.
* **AI Training:** Do not paste proprietary code into public LLMs (ChatGPT, Claude, etc.) unless "Data Privacy/Opt-out" is strictly enabled on your enterprise account.
* **Portfolios:** Do not showcase raw code or internal logic in public portfolios. Use high-level architectural diagrams only (subject to approval).

---

## 5. Third-Party & Contractor Protocols

For external partners and staff augmentation:

1.  **Work for Hire:** By default, all code written by contractors is considered "Work Made for Hire" and ownership transfers immediately to Your Organization upon creation.
2.  **Asset Return:** Upon contract termination, all local copies of repositories, documentation, and credentials must be permanently deleted from personal devices.
3.  **Clean Room Protocol:** If you are working on a similar feature for a different client, you must not reference or look at Your Organization's codebase while developing the new feature.

---

## 6. Requesting Exceptions

If you wish to open-source a specific module or present a technical case study at a conference:

1.  **Draft the Request:** Isolate the code/content in question.
2.  **Sanitization:** Ensure all specific business logic, keys, and client data are removed.
3.  **Submit for Approval:** Send a formal request to the Engineering Lead and Legal Department.
4.  **Wait for Written Consent:** **Do not act** until you have a signed authorization PDF.

---

*Disclaimer: This document is a summary of internal engineering standards and does not constitute a full legal contract. Refer to your Master Services Agreement (MSA) or Employment Contract for full legal terms.*