<!-- CHANGELOG.md -->
# Changelog

All notable changes to this project will be documented in this file.

This project follows [Conventional Commits](https://www.conventionalcommits.org/) and uses **semantic-release** to:
- infer version bumps from commit messages,
- generate release notes,
- create Git tags and GitHub Releases automatically.

## [Unreleased]

- Pending changes

---

### Commit message guide (quick reference)

- **feat:** A new feature (triggers **minor** version bump)
- **fix:** A bug fix (triggers **patch** version bump)
- **perf:** Performance improvements (patch)
- **refactor:** Code change that neither fixes a bug nor adds a feature
- **docs:** Documentation only changes
- **test:** Adding or fixing tests
- **chore:** Build process or auxiliary tool changes
- **BREAKING CHANGE:** in body or **feat!:**/**fix!:** in header triggers **major** bump

**Examples**
- `feat: add delete_message endpoint`
- `fix: handle 429 retry with backoff`
- `feat!: drop deprecated send_media_old`
- `docs: update README with install instructions`

---

> The first time semantic-release runs on `main`, it will replace this section with a versioned entry (e.g. `1.0.1`) and append release notes automatically.
v 1.0.0