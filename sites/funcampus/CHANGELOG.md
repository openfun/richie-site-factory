# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Fix AWS media storage backend after upgrade to DjangoCMS 3.8.0

## [0.6.0] - 2020-11-12

### Changed

- Clarify call-to-action on the "contact us" button
- Upgrade richie to 2.0.0-beta.20
- Display course duration in course glimpse footer

## [0.5.0] - 2020-10-08

### Added

- Add middleware from richie.core to limit the browser cache TTL

### Changed

- Upgrade richie to 2.0.0-beta.15

### Removed

- Remove monkey patch that enabled cms page cache for non-staff users
- Remove Django cache middlewares from the settings

## [0.4.1] - 2020-09-25

### Fixed

- Hide site in the english language until it is ready

## [0.4.0] - 2020-09-23

### Added

- Add link to the LMS dashboard as a button in the header

## [0.3.1] - 2020-09-17

### Fixed

- Rename "help" button to "contact us" in site header
- Add link to contact form on the "contact us" button on the course detail page

## [0.3.0] - 2020-09-16

### Added

- Override `course_detail` template to add a message above subheader CTA.

### Changed

- Link the "help" button in menu to a page holding this "reverse id"
- Upgrade richie to 2.0.0-beta.14
- Hide licences block on the course detail pages
- Change aside glimpse title color accordingly to feedback
- Customize filters visible on the search page
- Customize social networks links

### Fixed

- Add i18n messages compilation in the DockerFile so translations are ready

## [0.2.0] - 2020-08-20

### Changed

- Upgrade richie to 2.0.0-beta.11
- Update theme to fit to requirements (primary and secondary color change,
  logo, favicon).
- Enable cache for content and sessions
- Enable Django CMS page cache for non-staff users

### Fixed

- Fix translation overrides by configuring the specific "locale" directory

## [0.1.0] - 2020-07-23

- First `funcampus` image

[unreleased]: https://github.com/openfun/richie-site-factory/compare/funcampus-0.6.0...HEAD
[0.6.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-0.5.0...funcampus-0.6.0
[0.5.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-0.4.1...funcampus-0.5.0
[0.4.1]: https://github.com/openfun/richie-site-factory/compare/funcampus-0.4.0...funcampus-0.4.1
[0.4.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-0.3.1...funcampus-0.4.0
[0.3.1]: https://github.com/openfun/richie-site-factory/compare/funcampus-0.3.0...funcampus-0.3.1
[0.3.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-0.2.0...funcampus-0.3.0
[0.2.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-0.1.0...funcampus-0.2.0

[0.1.0]: https://github.com/openfun/richie-site-factory/compare/ 185f9deff5c4dd79e21f4f42c2acd1d17c73c293...funcampus-0.1.0
