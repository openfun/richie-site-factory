# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Upgrade richie to 1.9.0,
- Make the superuser field readonly for non superusers.

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

[unreleased]: https://github.com/openfun/fun-mooc/compare/v0.4.3...HEAD
[0.4.3]: https://github.com/openfun/fun-mooc/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/openfun/fun-mooc/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/openfun/fun-mooc/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/openfun/fun-mooc/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/openfun/fun-mooc/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/openfun/fun-mooc/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/openfun/fun-mooc/releases/tag/v0.1.0
