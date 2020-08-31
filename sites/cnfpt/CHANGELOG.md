# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Link the "help" button in menu to a page holding this "reverse id"
- On the search page, keep only the Subjects and Availability filters

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

[unreleased]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.4.0...HEAD
[0.4.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.3.0...cnfpt-0.4.0
[0.3.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.2.0...cnfpt-0.3.0
[0.2.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.1.0...cnfpt-0.2.0
[0.1.0]: https://github.com/openfun/richie-site-factory/releases/tag/cnfpt-0.1.0
