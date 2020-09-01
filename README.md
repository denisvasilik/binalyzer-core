# Binalyzer Core

This repository implements Binalyzer's core features. Functionality that is not
central to Binalyzer's concept is added through its extension mechanism.

Features:

* Template Engine
* Template Providers
* Template Transformations
* Data Binding System
* Data Providers
* Data Converter
* Extension Mechanism

## Repositories

Binalyzer spans accross several GitHub repositories:

* [binalyzer]
* [binalyzer-core]
* [binalyzer-cli]
* [binalyzer-template-provider]
* [binalyzer-data-provider]
* [binalyzer-rest]
* [binalyzer-lsp]
* [binalyzer-docker]
* [binalyzer-wasm]

[binalyzer]: https://github.com/denisvasilik/binalyzer
[binalyzer-core]: https://github.com/denisvasilik/binalyzer-core
[binalyzer-cli]: https://github.com/denisvasilik/binalyzer-cli
[binalyzer-template-provider]: https://github.com/denisvasilik/binalyzer-template-provider
[binalyzer-data-provider]: https://github.com/denisvasilik/binalyzer-data-provider
[binalyzer-rest]: https://github.com/denisvasilik/binalyzer-rest
[binalyzer-lsp]: https://github.com/denisvasilik/binalyzer-lsp
[binalyzer-docker]: https://github.com/denisvasilik/binalyzer-docker
[binalyzer-wasm]: https://github.com/denisvasilik/binalyzer-wasm

## Documentation

Documentation is available from [binalyzer.readthedocs.io].

[binalyzer.readthedocs.io]: https://binalyzer.readthedocs.io/en/latest/

## Get in touch

- Report bugs, suggest features or view the source code [on GitHub].
- For contributions refer to [the contributors guide].

[on GitHub]: https://github.com/denisvasilik/binalyzer

## Continuous Integration (CI)

This repository contains a `.travis.yml` and a `ci` folder which both are used
for CI.

### Pre-Commit Hooks

This repository provides `pre-commit` and `pre-push` hooks. They are installed
using the following commands:

```console
~$ pre-commit install -t pre-commit
~$ pre-commit install -t pre-push
```

The following command runs the hooks and checks all files.

```console
~$ pre-commit run --all-files --hook-stage push
```

# License

Licensed under the MIT license ([LICENSE-MIT] or http://opensource.org/licenses/MIT).

[the contributors guide]: CONTRIBUTING.md
[LICENSE-MIT]: LICENSE.rst
