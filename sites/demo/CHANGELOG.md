# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Define missing EDX_USER_PROFILE_TO_DJANGO setting

## [2.0.0-beta.14.4] - 2020-09-08

### Fixed

- Add missing courses API url pattern

### Changed

- Bump lodash from 4.17.14 to 4.17.20

## [2.0.0-beta.14.3] - 2020-09-08

### Fixed

- set SOCIAL_AUTH_REDIRECT_IS_HTTPS to True in settings

## [2.0.0-beta.14.2] - 2020-09-04

### Fixed 

- Activate SSO connection with Open edX Hawthorn

## [2.0.0-beta.14.1] - 2020-09-04

### Fixed

- Declare missing social urls.

## [2.0.0-beta.14] - 2020-09-04

### Changed

- Upgrade richie to 2.0.0-beta.14 (LMS bridge and language dropdown)
- Set public english language

### Fixed

- Add i18n messages compilation in the DockerFile so translations are ready

## [2.0.0-beta.11] - 2020-08-20

### Changed

- Upgrade richie to 2.0.0-beta.11
- Enable Django CMS page cache for non-staff users
- Enable cache for content and sessions

### Fixed

- Fix translation overrides by configuring the specific "locale" directory

## [2.0.0-beta.8] - 2020-06-17

### Changed

- Upgrade richie to 2.0.0-beta.8

### Fixed

- Add missing factory-boy dependency to allow generating the demo site

## [2.0.0-beta.7] - 2020-06-08

First demo image for richie to 2.0.0-beta.7

[unreleased]: https://github.com/openfun/richie-site-factory/compare/demo-2.0.0-beta.14.4...HEAD
[2.0.0-beta.14.4]: https://github.com/openfun/richie-site-factory/compare/demo-2.0.0-beta.14.3...demo-2.0.0-beta.14.4
[2.0.0-beta.14.3]: https://github.com/openfun/richie-site-factory/compare/demo-2.0.0-beta.14.2...demo-2.0.0-beta.14.3
[2.0.0-beta.14.2]: https://github.com/openfun/richie-site-factory/compare/demo-2.0.0-beta.14.1...demo-2.0.0-beta.14.2
[2.0.0-beta.14.1]: https://github.com/openfun/richie-site-factory/compare/demo-2.0.0-beta.14...demo-2.0.0-beta.14.1
[2.0.0-beta.14]: https://github.com/openfun/richie-site-factory/compare/demo-2.0.0-beta.11...demo-2.0.0-beta.14
[2.0.0-beta.11]: https://github.com/openfun/richie-site-factory/compare/demo-2.0.0-beta.8...demo-2.0.0-beta.11
[2.0.0-beta.8]: https://github.com/openfun/richie-site-factory/compare/demo-2.0.0-beta.7...demo-2.0.0-beta.8
[2.0.0-beta.7]: https://github.com/openfun/richie-site-factory/releases/tag/demo-2.0.0-beta.7
