import importlib.util
import os

try:
    importlib.util.find_spec("gi.repository.Gtk")
except ImportError:
    GTK_AVAILABLE = False
else:
    GTK_AVAILABLE = True

print(GTK_AVAILABLE)

# wayland - sway - console - gtk
print(os.environ.get("XDG_SESSION_TYPE"))

print(os.environ.get("DISPLAY"))