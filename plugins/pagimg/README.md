# python -m plugins.pagimg *COMMAND*

Tools for paginated images. Each page is assumed to be comprised of a single image. Useful for scanned books or comics.

The corresponding EPUB type to build/pack/check with is `pagimg`. This corresponds to fixed-layout (pre-paginated) EPUB3.

## arrange

Recursively rename files in directories in sort order.

* If all files have an integer filename (for example `1.jpg`, `10.jpg`), then they will be sorted based on that integer.
* Otherwise, sort based on lexicographical ordering of file names.

Renamed files will all have integer names, starting from `1` and left padded with `0`s to match the number of digits needed to represent the (largest) integer name of the last file.

Args:

* `-s`, `--suffixes`: list of files suffixes to process. If not specified, all files will be processed. For example, to process all images, one might use `--suffixes .jpg .png`.
* `directory` (positional): the path to the directory to process. Will recursively process all subdirectories as well.

## autonav

Automatically generate a `_nav` file based on directory structure. Since EPUB paths cannot contain spaces, all directory names should not have spaces (use underscore _ instead). The recursive sorting criteria is as follows:

* If all directory names start with a integer followed by _ (for example `1_notchapter2`, `2_chapter2`), then they will be sorted based on that integer.
* Otherwise, sort based on lexicographical ordering of directory names.
* Page files are assumed to have an integer only name and will be sorted based on that ordering. See the `arrange` command for assistance in meeting this criteria.

Each directory corresponds to a navigation tree node, with `href` to its first page. If it has no pages, its `href` will be to the `href` if its first subdirectory. Empty subdirectories (containing no pages) are ignored. The navigation tree node `text` is the name of the corresponding directory with underscores replaced with spaces (and leading integer stripped if sorted based on those integers).

Inherits global args from main app. Additional args:

* `--nav-format`: the file format of the `_nav` file. Should be one of:
    * `json` (default if not specified)
    * `yaml`