# [1.1.0](https://github.com/Maquina-Digital/evolution-client-py-sdk/compare/v1.0.2...v1.1.0) (2025-11-15)


### Features

* add Makefile for project management and CI testing setup ([dd7ee49](https://github.com/Maquina-Digital/evolution-client-py-sdk/commit/dd7ee49059224b0125146f3756b8b343862e2132))

## [1.0.2](https://github.com/Maquina-Digital/evolution-client-py-sdk/compare/v1.0.1...v1.0.2) (2025-11-15)


### Bug Fixes

* adjust message payload format ([0e9aa8d](https://github.com/Maquina-Digital/evolution-client-py-sdk/commit/0e9aa8d78f2d88ca5ae25fda7e9f1c7bf63f3474))
* trigger release test ([520d7e9](https://github.com/Maquina-Digital/evolution-client-py-sdk/commit/520d7e917b6f5dcdfa735da955d058f5601be402))
* trigger release test ([ab819a0](https://github.com/Maquina-Digital/evolution-client-py-sdk/commit/ab819a0768c0549478b7c8e8f99e4202be574591))
* trigger release test2 ([a3a3f82](https://github.com/Maquina-Digital/evolution-client-py-sdk/commit/a3a3f82bbbc66c72376567e800c824bed1fb5744))
* trigger release test3 ([e2a662a](https://github.com/Maquina-Digital/evolution-client-py-sdk/commit/e2a662a65e1501070e9ca1abfce6f74ef45fe9b6))

## [1.0.1](https://github.com/Maquina-Digital/evolution-client-py-sdk/compare/v1.0.0...v1.0.1) (2025-11-10)


### Bug Fixes

* Update workflow for automatic semantic release ([b2a55d3](https://github.com/Maquina-Digital/evolution-client-py-sdk/commit/b2a55d346db21ebf157b602647f4990b2eaa910c))

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
