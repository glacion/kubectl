# Watcher

This is an automation script that does the following in order:

- Pulls new kubectl tags from `kubernetes/kubectl`
- Selects only the tags that start with `kubernetes` and have no prerelease and build semver annotations attached to them
- Pulls published images from `glacion/kubectl` from docker hub
- Dispatches events to [workflow](https://github.com/glacion/kubectl/blob/main/.github/workflows/build.yaml) via GitHub API

## Development

You need python and poetry installed.

Run `poetry install` to get dependencies.

## Contributing

- Make sure your code is properly formatted with [black](https://github.com/psf/black)
