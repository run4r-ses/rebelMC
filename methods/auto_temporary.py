__METHOD_name__ = "In-memory Patching"
__METHOD_icon__ = "AUTO_FIX_HIGH"
__METHOD_description__ = "Automatically patches Store DLL from game, and injects it back. Most of the code is based off BEAMinject (now called BeaMC)."

from .utils.log import MethodLogger
from .utils import maxrm_mcpatch
import os
import json
import subprocess
import librosewater.module
import librosewater.process

def runcmd(args):
    try:
        return subprocess.check_output(args, stderr=subprocess.STDOUT, errors="ignore")
    except subprocess.CalledProcessError:
        pass

def main(config, log_path):
    logger = MethodLogger(log_path)
    logger.info(f"Starting patch (using MaxRM patches v{maxrm_mcpatch.__version__})")

    # Get game install
    if config['use_preview']:
        package_name = "Microsoft.MinecraftWindowsBeta"
        gamename = "Minecraft Preview"
    else:
        package_name = "Microsoft.MinecraftUWP"
        gamename = "Minecraft"
    payload = f'powershell.exe -c "Get-AppxPackage -name {package_name} | ' \
        'ForEach-Object { @($_.Version, $_.PackageFamilyName, ' \
        '(Join-Path $_.InstallLocation (Get-AppxPackageManifest $_).' \
        'Package.Applications.Application.Executable)) ' \
        '| ConvertTo-Json }"'
    try:
        mcinstall = json.loads(runcmd(payload))
    except TypeError:
        logger.error(f"Error while getting {gamename} install") 
        return 1
    except json.JSONDecodeError:
        logger.error(f"{gamename} not found")
        return 1
    logger.debug(f"Found {gamename} version {mcinstall[0]}")

    # Wait for game
    if config['start_game']:
        logger.info(f"Launching {gamename}")
        runcmd(f'powershell.exe explorer.exe shell:AppsFolder\\{mcinstall[1]}!App')
    logger.info(f"Waiting for {gamename} to launch")
    mcapp = os.path.basename(mcinstall[2])
    try:
        PID, process_handle = librosewater.process.wait_for_process(mcapp)
    except librosewater.exceptions.QueryError:
        logger.error(f"Couldn't wait for {gamename} (likely OS error)")
        return 1
    logger.debug(f"Found {gamename} at PID {PID}")

    # Get module address
    logger.info("Waiting for module")
    try:
        module_address, _ = librosewater.module.wait_for_module(process_handle, "Windows.ApplicationModel.Store.dll")
    except librosewater.exceptions.ProcessClosedError:
        logger.error(f"Minecraft process was closed while waiting for module")
        return 1
    logger.debug(f"Found module at {hex(module_address)}")

    # Dump module to variable
    logger.info("Dumping module and patching")
    try:
        data = librosewater.module.dump_module(process_handle, module_address)
    except librosewater.exceptions.ReadWriteError:
        logger.error(f"Couldn't dump module, did Minecraft close?")
        return 1
    try:
        arch = maxrm_mcpatch.check_machine(data[1])
    except NotImplementedError:
        logger.error("Couldn't find patches for platform, may be unsupported")
        return 1
    # The reason why we don't check error here is because
    # it's guaranteed to be one of the supported architectures
    # by the patches. The check is there for external usage of
    # the Max-RM hex patches.
    new_data = maxrm_mcpatch.patch_module(arch, data[1])

    logger.info(f"Injecting module ({len(new_data)} bytes total)")
    try:
        librosewater.module.inject_module(process_handle, module_address, new_data)
    except librosewater.exceptions.ReadWriteError:
        logger.error(f"Couldn't inject module, did Minecraft close?")
        return 1

    logger.info("Patching complete")
    return 0
