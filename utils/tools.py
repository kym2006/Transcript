import logging

log = logging.getLogger(__name__)


def perm_format(perm):
    return perm.replace("_", " ").replace("guild", "server").title()
