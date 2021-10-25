# python -m plugins.ghrelease

Creates GitHub releases. This plugin is used by the GitHub workflow [Create Release EPUBS](https://github.com/jayruin/web-epubs/actions/workflows/release.yml) and there should be no need to run it manually.

For each EPUB type under `docs/`, it will do the following:

1. Pack expanded EPUBs
2. Run EPUBCheck on packaged EPUBs
3. Create a GitHub release (corresponding to that specific EPUB type) which will contain the `.epub` files as well as the EPUBCheck results in `.txt` files

Finally, it will also create a `epubcheck.summary.json` file with the total number of fatals, errors and warnings encountered and create a final GitHub release for that summary file.