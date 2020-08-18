[![Create Release ePubs Badge](https://github.com/jayruin/web-epubs-public/workflows/Create%20Release%20ePubs/badge.svg)](https://github.com/jayruin/web-epubs-public/actions?query=workflow%3A%22Create+Release+ePubs%22)

# web-epubs

A collection of various documents for personal use, written in HTML, which are then compiled into ePubs.

## Quick Links

### Repository Links

- [Public repository](https://github.com/jayruin/web-epubs-public)
- [Private repository](https://github.com/jayruin/web-epubs-private)
- [Github Pages of this repository](https://jayruin.github.io/web-epubs-public)
- [Public Releases](https://github.com/jayruin/web-epubs-public/releases)
- [Private Releases](https://github.com/jayruin/web-epubs-private/releases)

### Latest Specs

- [EPUB 3.2 Specs](https://www.w3.org/publishing/epub3/epub-spec.html)

## Why HTML?

Markdown was also considered (easier to write and more human readable), however HTML has many advantages over Markdown:

- Different flavors of Markdown make it an inconsistent format to store documents in.
- Certain tags in HTML have no equivalent in Markdown (for instance `ruby`).
- No equivalent for MathML in Markdown.
- HTML is a more widespread file format; practically every smartphone, tablet, laptop, desktop, etc has a web browser.
- HTML has better compatibility with ePub.

## Why ePub?

PDF was also considered, however ePub has many advantages over PDF:

- ePub has support for reflowable documents. This means it can adapt to any screen size. Of course, ePub also has support for fixed-layout documents.
- High compatibility with HTML and web standards in general.
    - [W3C maintains the CSS standard](https://www.w3.org/Style/CSS/)
    - [W3C and WHATWG agreed to collaborate on a single version of HTML](https://www.w3.org/blog/news/archives/7753)
    - [IDPF who were maintaining the ePub standard have merged with W3C](https://www.w3.org/2017/01/pressrelease-idpf-w3c-combination.html.en)
- The XHTML files of ePubs can be deployed on the web (Github Pages) without any modification.
- Widespread support for ePub including ereaders, smartphones, tablets, laptops, desktops, etc. PDF is practically unreadable on smaller devices. Try reading a PDF on a 6 inch ereader!
- ePub converts to PDF fairly well, but the reverse is not true.

## Adding Content

### Minimal HTML

```html
<!DOCTYPE html>
<title>My Title</title>

<h1>My Header</h1>

<p>My content.</p>
```

### _metadata.json

Used to populate ePub metadata.

```json
{
    "title": "My Title",
    "author": "The Author",
    "languages": [
        "en",
        "some other language"
    ]
}
```

Optional parameters:

- `date` parameter is a string (defaults to date time now) which specifies the publication date. This parameter should be formatted as according to ePub specs.
- `css` parameter is an array of strings (defaults to empty array) which specifies the order in which css files should be linked. If this parameter is not specified, then css files will be linked in lexicographical order.
- `cover` parameter is a string (defaults to "img/cover.jpg") which specifies the relative path to the cover image. This image should be in a file format that is supported by the ePub specs.

### _nav.json

Used to construct ePub navigation document.

Contains an array of recursive `nav_node` objects, where each `nav_node` has a single key value pair mapping `href` to an array of `nav_node`.

Make sure `href` contains a file with `.xhtml` extension.

```json
[
    {
        "file_1.xhtml": [
            {
                "nested_file_1.xhtml": [
                    {
                        "nested_file_1.xhtml#my-id-1": []
                    },
                    {
                        "nested_file_2.xhtml#my-id-2": []
                    },
                    {
                        "nested_file_1.xhtml#my-id-3": []
                    }
                ]
            }
        ]
    }
]
```

## Building ePubs

Manually building:

```bash
python3 "./template_scripts/simple/main.py" "Hello World" "My Other Book"
python3 "./epub_scripts/build.py" "./epub/Hello World" "./epub/My Other Book"
```

There is also a GitHub Workflow `Create Release ePubs` found in `create-release-epubs.yml` which will automatically build ePubs when unzipped files are uploaded to `epub/`.

## Syncing ePubs

### Syncing with Calibre

```bash
python3 "./sync_scripts/sync_calibre.py" "Hello World" "My Other Book"
```