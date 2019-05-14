# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Define CDN_DOMAIN settings with cloudfront domain value.

## [0.2.0] - 2019-05-07

### Changed

- Upgrade richie to 1.0.0-beta.8

### Fixed

- The `data/` directory and its subdirectories are now properly created while
  bootstrapping the project

## [0.1.0] - 2019-04-18

### Added

- Design a Richie-based project for the future fun-mooc.fr front end
- Static and media files are stored in AWS S3 buckets and distributed _via_
  Amazon CloudFront

[unreleased]: https://github.com/openfun/fun-mooc/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/openfun/fun-mooc/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/openfun/fun-mooc/releases/tag/v0.1.0
