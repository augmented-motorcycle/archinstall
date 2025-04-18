from typing import override

from archinstall.default_profiles.profile import GreeterType, ProfileType
from archinstall.default_profiles.xorg import XorgProfile


class OpenboxProfile(XorgProfile):
	def __init__(self) -> None:
		super().__init__('Openbox', ProfileType.WindowMgr)

	@property
	@override
	def packages(self) -> list[str]:
		return [
			"openbox",
			"obconf",               # Openbox configuration GUI
			"polybar",                # Lightweight panel
			"lxappearance",         # GTK theme configuration
			"xfce4-terminal",       # Terminal emulator
			"thunar",               # File manager
			"gvfs",                 # Virtual filesystem support (mounting)
			"feh",                  # Wallpaper setter
			"network-manager-applet",
			"pavucontrol",          # Audio control
			"xorg-xinit",           # xinit for starting sessions
			"xorg-server",          # X server
			"xorg-xrandr",          # Display settings
			"xterm",                # Fallback terminal
			"xdg-utils",            # XDG standard tools
			"ttf-dejavu",           # Fonts
			"inter-font",
			"leafpad",              # Lightweight text editor
			"volumeicon",           # System tray volume icon
		]

	@property
	@override
	def default_greeter_type(self) -> GreeterType:
		return GreeterType.Lightdm
