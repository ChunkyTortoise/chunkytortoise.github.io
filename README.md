# ChunkyTortoise Portfolio

Personal portfolio site for Cayman Roden (AI Engineer), built with Tailwind CSS and deployed via GitHub Pages.

**Live site**: [chunkytortoise.github.io](https://chunkytortoise.github.io)

## What this site demonstrates

- **Working CI** - the [cmux interop demo](demos/cmux-interop/) ships 8 fail-closed controls exercised by [GitHub Actions](.github/workflows/cmux-interop-demo.yml) on every change
- **Technical writing** - [blog posts](https://chunkytortoise.github.io/blog.html) on testing LLM systems and contract testing with pact-python v3, with real metrics from production AI work
- **Honest numbers** - 500+ verified tests across published projects, tracked against a metrics source-of-truth; claims on the site are reconciled to that ledger

## Repo layout

| Path | Contents |
|---|---|
| `index.html`, `about.html`, `projects.html`, `blog.html` | Core landing pages (search-indexed) |
| `blog/` | Long-form writeups with verified metrics |
| `demos/cmux-interop/` | Runnable Python demo with its own test suite and CI workflow |
| `resume/` | Linked resume PDF |
| other top-level pages | Retired routes, stubbed with noindex redirects to the homepage |

## Local development

```bash
npm install          # installs tailwindcss (dev dependency)
npm run build:css    # rebuilds tw.css from tw-input.css
```

The cmux interop demo tests run independently:

```bash
cd demos/cmux-interop && make test   # 8 controls, python3 unittest
```

CI: [![cmux interop safety fixtures](https://github.com/ChunkyTortoise/chunkytortoise.github.io/actions/workflows/cmux-interop-demo.yml/badge.svg)](https://github.com/ChunkyTortoise/chunkytortoise.github.io/actions/workflows/cmux-interop-demo.yml)

## Support this project

If this work is useful, consider [sponsoring development](https://github.com/sponsors/ChunkyTortoise) - see [SPONSORS.md](SPONSORS.md).
