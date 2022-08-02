# STRIPE
from softskillspace.utils.settings import get_env_variable

STRIPE_SECRET_KEY = get_env_variable(
    "STRIPE_SECRET_KEY",
    "sk_test_51KvKWuC54CaNIoroXBFl08c2XdTYYeezRIcvvRIOgJI7Y5t14PTl"
    + "kBd19LuChVmEVqBIAjv2Lq7mJWZLTAOSiMQK00eTHed6lk",
)

STRIPE_PUBLIC_KEY = get_env_variable(
    "STRIPE_PUBLIC_KEY",
    "pk_test_51KvKWuC54CaNIorosr8Tc7iFf4I80ofkaW8rPhqHBlsJenHRS"
    + "AqM3mlzpV84HXppc9Tye4Wwgn2LhuRiy8uqLEfi00B4SFKJBE",
)
