import logging
from django.conf import settings

fmt = getattr(settings, "LOG_FORMAT", None)
lvl = getattr(settings, "LOG_LEVEL", logging.DEBUG)

logging.basicConfig(filename="example.log", encoding="utf-8", level=logging.DEBUG)
logging.debug(
    "Logging started on %s for %s" % (logging.root.name, logging.getLevelName(lvl))
)
