# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.13.0] - 2022-03-07

### Changed

- Upgrade richie to 2.13.0

## [1.12.0] - 2022-01-04

### Changed

- Upgrade richie to 2.11.0

### Fixed

- Upgrade stylesheets to handle new modal styles.

## [1.11.0] - 2021-12-27

### Changed

- Upgrade richie to 2.10.0

## [1.10.0] - 2021-11-03

### Changed

- Upgrade richie to 2.9.1

## [1.9.0] - 2021-10-07

### Changed

- Upgrade richie to 2.8.2

## [1.8.0] - 2021-09-30

### Added

- Set Django Check SEO up

### Changed

- Upgrade richie to 2.8.1
- Rename `LTI_TEST_*` settings to `LTI_*` as "TEST" does not make sense here

## [1.7.1] - 2021-06-08

### Fixed

- Upgrade richie to 2.7.1 to fix LTI consumer when logged-in OpenEdX

## [1.7.0] - 2021-06-04

### Changed

- Upgrade richie to 2.7.0

## [1.6.0] - 2021-05-03

### Changed

- Upgrade richie to 2.6.0

## [1.5.0] - 2021-04-22

### Changed

- Upgrade richie to 2.5.0

## [1.4.0] - 2021-04-07

### Changed

- Upgrade richie to 2.4.0
- Rename `fallback` cache to `memory_cache`

## [1.3.0] - 2021-03-25

### Changed

- Upgrade richie to 2.3.3

### Fixed

- Add missing stylesheet to patch CMS
- Add missing stylesheet for the LTI consumer plugin

## [1.2.0] - 2021-03-23

### Changed

- Upgrade richie to 2.3.0

## [1.1.0] - 2021-03-05

### Added

- Use custom views to handle errors (400, 403, 404, 500)
- Enable LTIConsumerPlugin on `course_teaser` placeholder

## [1.0.0] - 2021-02-05

### Changed

- Upgrade richie to 2.1.0
- Set `CMS_PAGETREE_DESCENDANTS_LIMIT` setting to control pagetree search node
  foldability according to its child node count

## [0.10.0] - 2021-01-14

### Changed

- Upgrade richie to 2.0.1

### Fixed

- Fix Sentry SDK initialization environment and release parameters

### Added

- Use a custom RedisCacheWithFallback cache to prevent denial of service
  when Redis is down

## [0.9.2] - 2020-12-14

### Fixed

- Fix translation (MOOCs -> MOOC)

## [0.9.1] - 2020-12-09

### Fixed

- Include version in CMS cache prefix to bust cache when deploying new version

## [0.9.0] - 2020-12-07

### Changed

- Upgrade richie to 2.0.0-beta.22

## [0.8.0] - 2020-11-30

### Changed

- Upgrade richie to 2.0.0-beta.21
- Unpin Django now that django-admin-style 2.0.2 supports
  the latest version 3.1.3
- Return a 403 response when user tries to upload a file in unsorted folder

## [0.7.2] - 2020-11-15

### Fixed

- Pin Django to 3.1.1 because the `/admin/cms/page` layout is broken with
  Django>=3.1.2

## [0.7.1] - 2020-11-12

### Fixed

- Fix AWS media storage backend after upgrade to DjangoCMS 3.8.0

## [0.7.0] - 2020-11-12

### Changed

- Upgrade richie to 2.0.0-beta.20
- Override search labels to mention MOOC

## [0.6.0] - 2020-10-08

### Added

- Add middleware from richie.core to limit the browser cache TTL

### Changed

- Upgrade richie to 2.0.0-beta.15
- Change aside glimpse title color accordingly to feedback

### Removed

- Remove monkey patch that enabled cms page cache for non-staff users
- Remove Django cache middlewares from the settings

## [0.5.2] - 2020-09-10

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

[unreleased]: https://github.com/openfun/richie-site-factory/compare/cnfpt-1.13.0...HEAD
[1.13.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-1.12.0...cnfpt-1.13.0
[1.12.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-1.11.0...cnfpt-1.12.0
[1.11.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-1.10.0...cnfpt-1.11.0
[1.10.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-1.9.0...cnfpt-1.10.0
[1.9.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-1.8.0...cnfpt-1.9.0
[1.8.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-1.7.1...cnfpt-1.8.0
[1.7.1]: https://github.com/openfun/richie-site-factory/compare/cnfpt-1.7.0...cnfpt-1.7.1
[1.7.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-1.6.0...cnfpt-1.7.0
[1.6.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-1.5.0...cnfpt-1.6.0
[1.5.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-1.4.0...cnfpt-1.5.0
[1.4.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-1.3.0...cnfpt-1.4.0
[1.3.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-1.2.0...cnfpt-1.3.0
[1.2.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-1.1.0...cnfpt-1.2.0
[1.1.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-1.0.0...cnfpt-1.1.0
[1.0.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.10.0...cnfpt-1.0.0
[0.10.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.9.2...cnfpt-0.10.0
[0.9.2]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.9.1...cnfpt-0.9.2
[0.9.1]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.9.0...cnfpt-0.9.1
[0.9.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.8.0...cnfpt-0.9.0
[0.8.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.7.2...cnfpt-0.8.0
[0.7.2]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.7.1...cnfpt-0.7.2
[0.7.1]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.7.0...cnfpt-0.7.1
[0.7.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.6.0...cnfpt-0.7.0
[0.6.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.5.2...cnfpt-0.6.0
[0.5.2]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.5.1...cnfpt-0.5.2
[0.5.1]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.5.0...cnfpt-0.5.1
[0.5.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.4.0...cnfpt-0.5.0
[0.4.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.3.0...cnfpt-0.4.0
[0.3.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.2.0...cnfpt-0.3.0
[0.2.0]: https://github.com/openfun/richie-site-factory/compare/cnfpt-0.1.0...cnfpt-0.2.0
[0.1.0]: https://github.com/openfun/richie-site-factory/releases/tag/cnfpt-0.1.0
