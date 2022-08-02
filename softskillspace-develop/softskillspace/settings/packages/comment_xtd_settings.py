from softskillspace.utils.settings import get_env_variable

COMMENTS_APP = "django_comments_xtd"

#  To help obfuscating comments before they are sent for confirmation.
COMMENTS_XTD_SALT = (b"Timendi causa est nescire. "
                     b"Aequam memento rebus in arduis servare mentem.")

# Source mail address used for notifications.
COMMENTS_XTD_FROM_EMAIL = get_env_variable(
    "ADMIN_EMAIL_ADDRESS", "lekan@softskillspace.me"
)

# Contact mail address to show in messages.
COMMENTS_XTD_CONTACT_EMAIL = COMMENTS_XTD_FROM_EMAIL

COMMENTS_XTD_MAX_THREAD_LEVEL = 1  # default is 0

# default is ('thread_id', 'order')
COMMENTS_XTD_LIST_ORDER = ("-thread_id", "order")

COMMENTS_XTD_APP_MODEL_OPTIONS = {
    "default": {
        "allow_flagging": False,
        "allow_feedback": False,
        "show_feedback": False,
        "who_can_post": "users",  # Valid values: 'all', users'
    }
}
