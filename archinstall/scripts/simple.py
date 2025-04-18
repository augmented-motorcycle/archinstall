from pathlib import Path
from archinstall.default_profiles.desktops.openbox import OpenboxProfile
from archinstall.lib.args import ArchConfig, arch_config_handler
from archinstall.lib.configuration import ConfigurationOutput
from archinstall.lib.disk.filesystem import FilesystemHandler
from archinstall.lib.disk.utils import disk_layouts
from archinstall.lib.global_menu import GlobalMenu
from archinstall.lib.hardware import GfxDriver
from archinstall.lib.installer import Installer
from archinstall.lib.models.device_model import DiskLayoutConfiguration
from archinstall.lib.models.network_configuration import NetworkConfiguration, NicType
from archinstall.lib.models.audio_configuration import Audio, AudioConfiguration
from archinstall.lib.models.profile_model import ProfileConfiguration
from archinstall.lib.output import debug, error
from archinstall.tui import Tui


def ask_questions() -> None:
	print("_________ Asking questions...")
	sleep(6)

	with Tui():
		global_menu = GlobalMenu(arch_config_handler.config)
		global_menu.disable_all()

		global_menu.set_enabled('disk_config', True)
		global_menu.set_enabled('users', True)
		global_menu.set_enabled('swap', True)
		global_menu.set_enabled('__config__', True)

		global_menu.run()


def perform_installation(mountpoint: Path) -> None:
	"""
	Performs the installation steps on a block device.
	Only requirement is that the block devices are
	formatted and setup prior to entering this function.
	"""
	config: ArchConfig = arch_config_handler.config

	if not config.disk_config:
		error("No disk configuration provided")
		return

	disk_config: DiskLayoutConfiguration = config.disk_config
	disk_encryption = config.disk_encryption

	with Installer(
		mountpoint,
		disk_config,
		disk_encryption=disk_encryption,
		kernels=config.kernels
	) as installation:
		# Mount all the drives to the desired mountpoint
		# This *can* be done outside of the installation, but the installer can deal with it.
		if disk_config:
			installation.mount_ordered_layout()

		# to generate a fstab directory holder. Avoids an error on exit and at the same time checks the procedure
		target = Path(f"{mountpoint}/etc/fstab")
		if not target.parent.exists():
			target.parent.mkdir(parents=True)

	# For support reasons, we'll log the disk layout post installation (crash or no crash)
	debug(f"Disk states after installing:\n{disk_layouts()}")


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

	if arch_config_handler.config.disk_config:
		fs_handler = FilesystemHandler(
			arch_config_handler.config.disk_config,
			arch_config_handler.config.disk_encryption
		)

		fs_handler.perform_filesystem_operations()

	perform_installation(arch_config_handler.args.mountpoint)

