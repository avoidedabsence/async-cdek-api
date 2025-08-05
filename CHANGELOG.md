# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2025-08-05

### Added
- get_approximate_city method for /v2/location/suggest/cities API endpoint
- CityFromSearch as a response model for endpoint above
- Debug mode for APIClient

### Fixed
- Fixed enum issues for CountryCode
- APIClient methods were made private

## [0.1.1] & [0.1.2] - 2025-08-04

### Added
- Small changes to README and bugfixesa

## [0.1.0] - 2025-08-04

### Added
- Initial release of pycdek
- Asynchronous CDEK API client with full endpoint coverage
- Order management (create, track, update)
- Tariff calculation and comparison
- Location and delivery point lookup
- Courier services
- Label and document printing
- Webhook management
- Type-safe Pydantic models
- Automatic OAuth token management
- Comprehensive error handling
- Complete documentation and examples

[0.1.0]: https://github.com/avoidedabsence/async-cdek-api/releases/tag/v0.1.0
[0.1.1]: https://github.com/avoidedabsence/async-cdek-api/releases/tag/v0.1.1
[0.1.2]: https://github.com/avoidedabsence/async-cdek-api/releases/tag/v0.1.2
[0.1.5]: https://github.com/avoidedabsence/async-cdek-api/releases/tag/v0.1.5
