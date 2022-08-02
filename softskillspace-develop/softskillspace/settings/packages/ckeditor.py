from pathlib import Path

from softskillspace.utils.settings import get_env_variable

BASE_DIR = Path(__file__).resolve().parent.parent

# CKEDITOR_RESTRICT_BY_USER = True
# CKEDITOR_REQUIRE_STAFF = False
# CKEDITOR_CONFIGS = {
#     'default': {
#         'toolbar': 'full',
#         'height': 300,
#         'width': "100%",
#         'extraPlugins': ','.join([
#             'uploadimage',  # the upload image feature
#             # your extra plugins here
#             # 'Youtube',
#             # 'codesnippet',
#         ]),
#     },
# }

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 400,
        "width": "100%",
        "allowedContent": True,
        "uiColor": "#f0f0f0",
        # "extraPlugins": "uploadimage,link,iframe,colorbutton,youtube,codesnippet",
        "autoGrow_maxHeight": 800,
        "autoGrow_minHeight": 400,
        "removePlugins": "resize",
        "removeButtons": None,
        "external_plugin_resources": [("youtube", "/assets/js/youtube/", "plugin.js")],
    },
}

CKEDITOR_BASEPATH = "/assets/ckeditor/ckeditor/"

CKEDITOR_UPLOAD_PATH = get_env_variable(
    "MEDIA_ROOT", BASE_DIR / "softskillspace/uploads"
)

CKEDITOR_ALLOW_NONIMAGE_FILES = False
