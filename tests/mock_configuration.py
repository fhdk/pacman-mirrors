TEST_FILE = "core.db.tar.gz"
# http constants
MIRROR_MANAGER = "https://mirror-manager.manjaro.org/status.json"
# etc
CONFIG_FILE = "tests/mock/etc/pacman-mirrors.conf"
MIRROR_LIST = "tests/mock/etc/mirrorlist"
# pacman-mirrors
VAR_DIR = "tests/mock/var/"
CUSTOM_FILE = "tests/mock/var/custom-mirrors.json"
MIRROR_FILE = "tests/mock/var/status.json"
# repo constants
BRANCHES = ("stable", "testing", "unstable")
ARM_BRANCHES = ("arm-stable", "arm-testing", "arm-unstable")
PROTOCOLS = ("https", "http", "ftp")
METHODS = ("rank", "random")
SSL = ("True", "False")
REPO_ARCH = "/$repo/$arch"
