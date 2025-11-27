# mreider.com

This is my personal website, now built with [Hugo](https://gohugo.io).

Previously built with [Krems](https://github.com/mreider/krems), I've migrated to Hugo to take advantage of its larger ecosystem and active development.

## Building Locally

To build the site locally:

```bash
hugo --buildFuture --minify -d docs
```

To run the development server:

```bash
hugo server --buildFuture
```

## Deployment

The site is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the main branch. The workflow builds the site with Hugo and publishes to the `gh-pages` branch.