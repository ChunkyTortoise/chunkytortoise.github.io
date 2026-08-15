# Fail-closed cmux interoperability fixtures

[![cmux interop safety fixtures](https://github.com/ChunkyTortoise/chunkytortoise.github.io/actions/workflows/cmux-interop-demo.yml/badge.svg)](https://github.com/ChunkyTortoise/chunkytortoise.github.io/actions/workflows/cmux-interop-demo.yml)

This dependency-free fixture suite models eight controls from a dated local
multi-model terminal campaign. It requires Python 3.12 or newer and no model
account, private socket, pane history, or raw run artifact.

```bash
make test
```

The fixtures cover exact title and executable matching, cwd and actor proof,
nonce and context binding, sealed input mutation, terminal partial dispatch,
surface UUID telemetry fallback, independent verifier selection, and immutable
successor recovery.

The fixture model is intentionally smaller than the private live driver. It
supports review of the stated controls, not claims about scale or comparative
performance.
