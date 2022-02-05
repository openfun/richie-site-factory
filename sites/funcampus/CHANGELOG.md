# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Upgrade richie to 2.12.0

## [1.16.0] - 2022-01-04

### Changed

- Link footer logo to our new institutional site
- Upgrade richie to 2.11.0

### Fixed

- Upgrade stylesheets to handle new modal styles.

## [1.15.0] - 2021-12-27

### Changed

- Upgrade richie to 2.10.0

## [1.14.0] - 2021-11-03

### Changed

- Upgrade richie to 2.9.1

## [1.13.0] - 2021-10-07

### Changed

- Upgrade richie to 2.8.2

## [1.12.0] - 2021-09-30

### Added

- Set Django Check SEO up

### Changed

- Upgrade richie to 2.8.1
- Rename `LTI_TEST_*` settings to `LTI_*` as "TEST" does not make sense here

## [1.11.0] - 2021-06-04

### Changed

- Upgrade richie to 2.7.0

## [1.10.0] - 2021-05-03

### Changed

- Upgrade richie to 2.6.0

## [1.9.0] - 2021-04-22

### Changed

- Upgrade richie to 2.5.0

## [1.8.0] - 2021-04-07

### Changed

- Upgrade richie to 2.4.0
- Rename `fallback` cache to `memory_cache`

## [1.7.0] - 2021-03-25

### Changed

- Upgrade richie to 2.3.3

### Fixed

- Add missing stylesheet to patch CMS
- Add missing stylesheet for the LTI consumer plugin

## [1.6.0] - 2021-03-23

### Changed

- Upgrade richie to 2.3.0

## [1.5.0] - 2021-03-05

### Added

- Use custom views to handle errors (400, 403, 404, 500)
- Enable LTIConsumerPlugin on `course_teaser` placeholder

## [1.4.0] - 2021-02-05

### Changed

- Upgrade richie to 2.1.0
- Set `CMS_PAGETREE_DESCENDANTS_LIMIT` setting to control pagetree search node
  foldability according to its child node count

## [1.3.0] - 2021-01-14

### Changed

- Upgrade richie to 2.0.1

### Fixed

- Fix Sentry SDK initialization environment and release parameters

### Added

- Use a custom RedisCacheWithFallback cache to prevent denial of service
  when Redis is down

## [1.2.1] - 2020-12-09

### Fixed

- Include version in CMS cache prefix to bust cache when deploying new version

## [1.2.0] - 2020-12-07

### Changed

- Upgrade richie to 2.0.0-beta.22

## [1.1.0] - 2020-11-30

### Changed

- Upgrade richie to 2.0.0-beta.21
- Unpin Django now that django-admin-style 2.0.2 supports
  the latest version 3.1.3
- Return a 403 response when user tries to upload a file in unsorted folder

## [1.0.1] - 2020-11-15

### Fixed

- Pin Django to 3.1.1 because the `/admin/cms/page` layout is broken with
  Django>=3.1.2

## [1.0.0] - 2020-11-12

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

[unreleased]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.16.0...HEAD
[1.16.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.15.0...funcampus-1.16.0
[1.15.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.14.0...funcampus-1.15.0
[1.14.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.13.0...funcampus-1.14.0
[1.13.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.12.0...funcampus-1.13.0
[1.12.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.11.0...funcampus-1.12.0
[1.11.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.10.0...funcampus-1.11.0
[1.10.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.9.0...funcampus-1.10.0
[1.9.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.8.0...funcampus-1.9.0
[1.8.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.7.0...funcampus-1.8.0
[1.7.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.6.0...funcampus-1.7.0
[1.6.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.5.0...funcampus-1.6.0
[1.5.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.4.0...funcampus-1.5.0
[1.4.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.3.0...funcampus-1.4.0
[1.3.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.2.1...funcampus-1.3.0
[1.2.1]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.2.0...funcampus-1.2.1
[1.2.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.1.0...funcampus-1.2.0
[1.1.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.0.1...funcampus-1.1.0
[1.0.1]: https://github.com/openfun/richie-site-factory/compare/funcampus-1.0.0...funcampus-1.0.1
[1.0.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-0.6.0...funcampus-1.0.0
[0.6.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-0.5.0...funcampus-0.6.0
[0.5.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-0.4.1...funcampus-0.5.0
[0.4.1]: https://github.com/openfun/richie-site-factory/compare/funcampus-0.4.0...funcampus-0.4.1
[0.4.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-0.3.1...funcampus-0.4.0
[0.3.1]: https://github.com/openfun/richie-site-factory/compare/funcampus-0.3.0...funcampus-0.3.1
[0.3.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-0.2.0...funcampus-0.3.0
[0.2.0]: https://github.com/openfun/richie-site-factory/compare/funcampus-0.1.0...funcampus-0.2.0

[0.1.0]: https://github.com/openfun/richie-site-factory/compare/ 185f9deff5c4dd79e21f4f42c2acd1d17c73c293...funcampus-0.1.0
