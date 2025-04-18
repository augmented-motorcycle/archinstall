from archinstall.default_profiles.desktops.openbox import OpenboxProfile
from archinstall.lib.args import arch_config_handler
from archinstall.lib.configuration import ConfigurationOutput
from archinstall.lib.global_menu import GlobalMenu
from archinstall.lib.hardware import GfxDriver
from archinstall.lib.models.network_configuration import NetworkConfiguration, NicType
from archinstall.lib.models.audio_configuration import Audio, AudioConfiguration
from archinstall.lib.models.profile_model import ProfileConfiguration
from archinstall.tui import Tui


def ask_questions() -> None:
	with Tui():
		global_menu = GlobalMenu(arch_config_handler.config)
		global_menu.disable_all()

		global_menu.set_enabled('disk_config', True)
		global_menu.set_enabled('users', True)
		global_menu.set_enabled('swap', True)
		global_menu.set_enabled('__config__', True)

		global_menu.run()


def simple() -> None:
	ask_questions()

	arch_config_handler.config.profile_config = ProfileConfiguration(OpenboxProfile(), GfxDriver.AllOpenSource, None)
	arch_config_handler.config.audio_config = AudioConfiguration(Audio.PIPEWIRE)
	arch_config_handler.config.hostname = 'augmented-machine'
	arch_config_handler.config.network_config = NetworkConfiguration(NicType.NM)
	arch_config_handler.config.packages = ['polybar']

	config = ConfigurationOutput(arch_config_handler.config)
	config.write_debug()
	config.save()
