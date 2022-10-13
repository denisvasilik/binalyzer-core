# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.4] - 13.10.2022

- Fix usage of relative offset references

## [v1.0.3] - 06.09.2021

- Invalidate DOM cache on `count_property` or `count` assignment:
  - Ensure template copy is referenced by Binalyzer object
  - Rename `_invalidate_dom` to `invalidate` and make it publicly available

## [v1.0.2] - 18.08.2021

- Added auto-sizing for the text attribute:
  - If `sizing` is set to `auto` and the `size` property is not set explicitly,
    the `text` property's length determines the template's size.
- Added data extension:
  - If a template's size is greater than the data, the backed data will be
    extended up to the template's size using a default byte value of `0x00`.

## [v1.0.1] - 22.07.2021

- Added the `text` property:
    - The `text` property has been added to provide a way of storing static
      binary data with a template.

## [v1.0.0] - 28.04.2021

- Initial release

[v1.0.0]: https://github.com/denisvasilik/binalyzer-core/tree/v1.0.0
[v1.0.1]: https://github.com/denisvasilik/binalyzer-core/tree/v1.0.1
[v1.0.2]: https://github.com/denisvasilik/binalyzer-core/tree/v1.0.2
[v1.0.3]: https://github.com/denisvasilik/binalyzer-core/tree/v1.0.3
[v1.0.4]: https://github.com/denisvasilik/binalyzer-core/tree/v1.0.4
