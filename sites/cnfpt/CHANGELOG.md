# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Fix parler languages that must be in sync with CMS languages

## [0.5.1] - 2020-09-10

### Changed

- Upgrade richie to 2.0.0-beta.14
- Bump elliptic from 6.5.1 to 6.5.3
- Bump lodash from 4.17.14 to 4.17.20

### Fixed

- Set SOCIAL_AUTH_REDIRECT_IS_HTTPS to True in settings
- Add missing courses API url pattern
- The banner search title should be white

## [0.5.0] - 2020-08-31

### Added

- Add a new section "Audience" to the course detail page
- Activate SSO connection with Open edX Hawthorn

### Changed

- Rewordings via translations overrides
- Upgrade richie to 2.0.0-beta.13 (LMS bridge and language dropdown)
- Link the "help" button in menu to a page holding this "reverse id"
- On the search page, keep only the Subjects and Availability filters

### Removed

- Remove the main section and contact button on the course detail page header

### Fixed

- Reinstate English in development environment to allow generating demo site
- Add i18n messages compilation in the DockerFile so translations are ready

## [0.4.0] - 2020-08-20

### Changed

- Add translations for new strings
- Deactivate english language
- Upgrade richie to 2.0.0-beta.11
- Enable Django CMS page cache for non-staff users
- Enable cache for content and sessions

### Fixed

- Fix translation overrides by configuring the specific "locale" directory

## [0.3.0] - 2020-06-17

### Changed

- Upgrade richie to 2.0.0-beta.8

## [0.2.0] - 2020-06-08

### Changed

- Upgrade richie to 2.0.0-beta.7

## [0.1.0] - 2020-06-08

Initial release

[unreleased]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.5.1...HEAD
[0.5.1]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.5.0...cnfpt-0.5.1
[0.5.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.4.0...cnfpt-0.5.0
[0.4.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.3.0...cnfpt-0.4.0
[0.3.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.2.0...cnfpt-0.3.0
[0.2.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.1.0...cnfpt-0.2.0
[0.1.0]: https://github.com/openfun/richie-site-factory/releases/tag/cnfpt-0.1.0
