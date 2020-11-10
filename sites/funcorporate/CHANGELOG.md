# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Upgrade richie to 2.0.0-beta.20

## [0.8.1] - 2020-10-16

### Fixed

- Fix javascript build which was forgotten in Dockerfile and missing from image

## [0.8.0] - 2020-10-14

### Added

- Add a "Dashboard" button linking to OpenEdX

### Changed

- Allow several plugins in course description to relax limit on number of char
- Open contact form in a new tab
- Display course duration in course glimpse footer

## [0.7.0] - 2020-10-08

### Added

- Add middleware from richie.core to limit the browser cache TTL

### Changed

- Upgrade richie to 2.0.0-beta.15
- Customize slogan in footer

### Fixed

- Hide site in the english language until it is ready

### Removed

- Remove monkey patch that enabled cms page cache for non-staff users
- Remove Django cache middlewares from the settings

## [0.6.2] - 2020-09-17

### Changed

- Customize wording for "What you will learn" using translations

### Fixed

- Filter on "training domains", not on "categories" which is the root node
- Rename contact buttons in header and course page and point to Zendesk

## [0.6.1] - 2020-09-16

### Fixed

- Fix missing scss objects and components following richie upgrade

## [0.6.0] - 2020-09-16

### Added

- Override `course_detail` template to add a message above subheader CTA.
- Use the FunCorporate Zendesk link on "Contact Us" CTA in header.

### Changed

- Upgrade richie to 2.0.0-beta.14
- Hide licences block on the course detail pages
- Customize filters visible on the search page
- Customize social networks links

### Fixed

- Override .subheader .category-badge styles to fit fun-corporate mockups.
- Add i18n messages compilation in the DockerFile so translations are ready

## [0.5.0] - 2020-08-20

### Changed

- Upgrade richie to 2.0.0-beta.11
- Enable cache for content and sessions
- Enable Django CMS page cache for non-staff users

### Fixed

- Fix translation overrides by configuring the specific "locale" directory

## [0.4.0] - 2020-06-17

### Changed

- Upgrade richie to 2.0.0-beta.8

## [0.3.0] - 2020-06-08

### Changed

- Upgrade to richie 2.0.0-beta.7

## [0.2.2] - 2020-06-06

### Changed

- Upgrade to richie 2.0.0-beta.6

## [0.2.1] - 2020-05-07

### Fixed

- With django storages S3 backend, `STATIC_URL` should not start with a "/"

## [0.2.0] - 2020-05-07

### Changed

- Upgrade to django-storages 1.9.1
- Disable 'runs' and 'snapshot' blocks from course detail.
- Disable 'max-width' from '.course-detail\_\_wrapper'.
- Enable background and arc image for course detail primary group.

### Fixed

- DjangoCMS is not compatible with Django 3, force it in requirements

## [0.1.0] - 2020-04-21

### Changed

- Upgrade Terraform project to run with v0.12.24
- Upgrade Python requirements files to the last dependencies.
- Upgrade frontend "package.json" to the last dependencies.
- Update "main.scss" file to import richie Sass sources to be able to
  override settings.
- Update project settings to add styleguide and missing new settings.
- Update project urls to add styleguide and account views.
- Update layout color theme and logo to fit fun-corporate mockups.

[unreleased]: https://github.com/openfun/richie-site-factory/compare/funcorporate-0.8.1...HEAD
[0.8.1]: https://github.com/openfun/richie-site-factory/compare/funcorporate-0.8.0...funcorporate-0.8.1
[0.8.0]: https://github.com/openfun/richie-site-factory/compare/funcorporate-0.7.0...funcorporate-0.8.0
[0.7.0]: https://github.com/openfun/richie-site-factory/compare/funcorporate-0.6.2...funcorporate-0.7.0
[0.6.2]: https://github.com/openfun/richie-site-factory/compare/funcorporate-0.6.1...funcorporate-0.6.2
[0.6.1]: https://github.com/openfun/richie-site-factory/compare/funcorporate-0.6.0...funcorporate-0.6.1
[0.6.0]: https://github.com/openfun/richie-site-factory/compare/funcorporate-0.5.0...funcorporate-0.6.0
[0.5.0]: https://github.com/openfun/richie-site-factory/compare/funcorporate-0.4.0...funcorporate-0.5.0
[0.4.0]: https://github.com/openfun/richie-site-factory/compare/funcorporate-0.3.0...funcorporate-0.4.0
[0.3.0]: https://github.com/openfun/richie-site-factory/compare/funcorporate-0.2.2...funcorporate-0.3.0
[0.2.2]: https://github.com/openfun/richie-site-factory/releases/tag/funcorporate-0.2.2

# Deprecated repository

[0.2.1]: https://github.com/openfun/fun-corporate/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/openfun/fun-corporate/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/openfun/fun-corporate/releases/tag/v0.1.0
