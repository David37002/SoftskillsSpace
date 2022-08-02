from softskillspace.utils.settings import get_env_variable

DEFAULT_FILE_STORAGE = "storages.backends.dropbox.DropBoxStorage"

DROPBOX_OAUTH2_TOKEN = get_env_variable("DROPBOX_ACCESS_TOKEN", "xxxx-xxxx")

DROPBOX_ROOT_PATH = "/Public"
