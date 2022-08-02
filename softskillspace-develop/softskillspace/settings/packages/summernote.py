import django

SUMMERNOTE_THEME = "lite"

ALLOWED_TAGS = [
    "a",
    "abbr",
    "acronym",
    "b",
    "blockquote",
    "br",
    "code",
    "div",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "i",
    "img",
    "li",
    "ol",
    "p",
    "span",
    "strike",
    "strong",
    "sub",
    "sup",
    "table",
    "tbody",
    "td",
    "thead",
    "tr",
    "u",
    "ul",
]

STYLES = [
    "background-color",
    "font-size",
    "line-height",
    "color",
    "font-family"]

ATTRIBUTES = {
    "*": [
        "style",
        "align",
        "title",
    ],
    "a": [
        "href",
    ],
}

SUMMERNOTE_CONFIG = {
    "summernote": {
        "width": "100%",
        "height": 400,
        "toolbr": [
            ["style", ["style"]],
            ["font", ["bold", "underline", "clear"]],
            ["fontname", ["fontname"]],
            ["color", ["color"]],
            ["para", ["ul", "ol", "paragraph"]],
            ["table", ["table"]],
            ["insert", ["link", "picture", "video"]],
            ["view", ["fullscreen", "codeview", "help"]],
        ],
    }
}
SUMMERNOTE_THEME = "lite"

if django.VERSION >= (3, 0):
    X_FRAME_OPTIONS = "SAMEORIGIN"
