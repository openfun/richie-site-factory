# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Add nginx to the stack to test collectstatic

### Fixed

- Fix css build location after refactoring

## [0.9.4] - 2020-05-21

### Fixed

- Fix path to storage class following refactoring

## [0.9.3] - 2020-05-21

### Added

- Add translations for strings specific to fun-mooc

### Changed

- Upgrade richie to 2.0.0-beta.6.
- Disable "Contact Us" CTA from course detail.

### Fixed

- Refactor project to the classical Django structure to fix static files
- Correctly adjust hero-intro background to homepage mockup.
- Use the FunMooc help center link on "Contact Us" CTA in header.

## [0.9.2] - 2020-05-07

### Fixed

- With django storages S3 backend, `STATIC_URL` should not start with a "/"

## [0.9.1] - 2020-05-07

### Changed

- Upgrade to django-storages 1.9.1

### Fixed

- With the django storages S3 backend, `MEDIA_URL` should not start with a "/"

## [0.9.0] - 2020-05-06

### Changed

- Upgrade richie to 2.0.0-beta.5.
- Update "main.scss" file to import richie Sass sources to be able to
  override settings.
- Update project settings to add styleguide and missing new settings.
- Update project urls to add styleguide.
- Update layout color theme and logo to fit fun-mooc mockups.

## [0.8.0] - 2019-12-15

### Changed

- Upgrade richie to 1.16.1.

### Fixed

- Upgrade django-storages to fix static manifest storage bakend and media
  files upload.

## [0.7.1] - 2019-11-24

### Fixed

- Add missing user related urls and settings.

## [0.7.0] - 2019-11-23

### Changed

- Upgrade richie to 1.14.1.

## [0.6.0] - 2019-10-23

### Changed

- Upgrade richie to 1.12.0.

## [0.5.0] - 2019-10-08

### Changed

- Upgrade richie to 1.10.0,
- Make the superuser field readonly for non superusers.

### Fixed

- Make API calls work behind an htaccess by removing Basic Auth fallback.

## [0.4.3] - 2019-09-12

### Changed

- Let the Google sheet importer sort media files related to each organization
  or course in their specific folder in Django filer.

### Fixed

- Clean-up the content imported from the Google sheet with gimporter:
  * fix broken links by porting missing media files to Django filer,
  * make all urls relative (exit france-universite-numerique-mooc.fr),
  * replace old urls by new ones computed with DjangoCMS page slugs.

## [0.4.2] - 2019-09-06

### Added

- Create roles and permissions for organizations and courses imported via the
  Google sheet importer,
- Import blog posts from Google sheet fixtures,
- Import course licences from Google sheet fixtures.

### Changed

- Upgrade richie to 1.8.3.

## [0.4.1] - 2019-09-02

### Fixed

- Fix CKEditor static files to work with a CDN,
- Fix logo override by moving it to the same new location as in Richie.

## [0.4.0] - 2019-08-28

### Added

- Add a gimporter app to automatically transfer existing content on fun-mooc.fr
- Automate backend code assessment with a classical python toolkit (flake8,
  isort, black, pylint, bandit)

### Changed

- Disable the "unsorted uploads" directory on Django Filer,
- Upgrade richie to 1.8.0.

### Security

- Update `lodash` and related packages to safe versions.

## [0.3.0] - 2019-07-04

### Added

- Define CDN_DOMAIN setting from AWS CloudFront domain value

### Changed

- Upgrade richie to 1.5.0

### Fixed

- Configure `X_FRAME_OPTIONS` to `SAMEORIGIN` to allow DjangoCMS frontend admin
  frames display

### Security

- Update `fstream` to a safe version (>=1.0.12)

## [0.2.0] - 2019-05-07

### Changed

- Upgrade richie to 1.0.0-beta.8

### Fixed

- The `data/` directory and its subdirectories are now properly created while
  bootstrapping the project
- Remove unused ElasticSearchMixin in project settings

## [0.1.0] - 2019-04-18

### Added

- Design a Richie-based project for the future fun-mooc.fr front end
- Static and media files are stored in AWS S3 buckets and distributed _via_
  Amazon CloudFront

[unreleased]: https://github.com/openfun/fun-mooc/compare/v0.9.4...HEAD
[0.9.4]: https://github.com/openfun/fun-mooc/compare/v0.9.3...v0.9.4
[0.9.3]: https://github.com/openfun/fun-mooc/compare/v0.9.2...v0.9.3
[0.9.2]: https://github.com/openfun/fun-mooc/compare/v0.9.1...v0.9.2
[0.9.1]: https://github.com/openfun/fun-mooc/compare/v0.9.0...v0.9.1
[0.9.0]: https://github.com/openfun/fun-mooc/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/openfun/fun-mooc/compare/v0.7.1...v0.8.0
[0.7.1]: https://github.com/openfun/fun-mooc/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/openfun/fun-mooc/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/openfun/fun-mooc/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/openfun/fun-mooc/compare/v0.4.3...v0.5.0
[0.4.3]: https://github.com/openfun/fun-mooc/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/openfun/fun-mooc/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/openfun/fun-mooc/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/openfun/fun-mooc/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/openfun/fun-mooc/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/openfun/fun-mooc/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/openfun/fun-mooc/releases/tag/v0.1.0
