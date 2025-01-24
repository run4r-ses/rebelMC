"""
Hex patterns for Minecraft patching
by Max-RM
"""
__version__ = "0.3.1"

import re
IMAGE_FILE_MACHINE_AMD64 = 0x8664 # x64
IMAGE_FILE_MACHINE_ARM = 0x1c0 # ARM little endian
IMAGE_FILE_MACHINE_ARMNT = 0x1c4 # ARM Thumb-2 little endian
IMAGE_FILE_MACHINE_ARM64 = 0xaa64 # ARM64 little endian
IMAGE_FILE_MACHINE_I386 = 0x14c # Intel 386 or later processors and compatible processors

def _c_h(pattern: str): return pattern.casefold().replace(" ", "")
def _ccm(pattern: str): return re.compile(_c_h(pattern))

PATCHES = {
    "amd64": [
        (
            _ccm(r"(39 9E C8 00 00 00) 0F 95 C1 (88 0F 8B)"),
            _c_h(r"\g<1> B1 00 90 \g<2>"), 0
        ),
        (
            _ccm(r"(FF EB 05) 8A 49 61 (88 0A 8B CB E8)"),
            _c_h(r"\g<1> B1 00 90 \g<2>"), 0
        )
    ],
    "i386": [
        (
            _ccm(r"(FF EB 08 39 77 74) 0F 95 C1 (88 08 8B)"),
            _c_h(r"\g<1> B1 00 90 \g<2>"), 0
        ),
        (
            _ccm(r"(FF EB 08 8B 4D 08) 8A 49 31 (88 08 8B)"),
            _c_h(r"\g<1> B1 00 90 \g<2>"), 0
        )
    ],
    "arm": [
        (
            _ccm(r"(05 E0 .. 3 .. 0B) B1 01 (23 00 E0 00 23 2B 70 20 46)"),
            _c_h(r"\g<1> B1 00 \g<2>"), 0
        ),
        (
            _ccm(r"(02 E0) 90 F8 .. 30 (0B 70 20 46)"),
            _c_h(r"\g<1> 4F F0 00 03 \g<2>"), 0
        )
    ],
    "arm64": [
        (
            _ccm(r"(FE 97 05 00 00 14 A8 .. A 40 B9 1F 01 00 71) E9 07 9F 1A (89 02 00 39 E0 03 13 2A)"),
            _c_h(r"\g<1> 09 00 80 52 \g<2>"), 0
        ),
        (
            _ccm(r"(FC 97 03 00 00 14 08) .. 41 39 (28 00 00 39 E0 03 13 2A)"),
            _c_h(r"\g<1> 00 80 52 \g<2>"), 1
        )
    ]
}

def check_machine(data: bytes):
    """
    Get the machine architecture from PE headers.

    This function extracts the machine architecture information from the 
    PE headers of the provided binary.

    :param data: The byte data representing the executable.
    :type data: bytes

    :return: A string representing the machine architecture, one of 
             "amd64", "i386", "arm", or "arm64".
    :rtype: str

    :raises NotImplementedError: If the architecture is unsupported.
    """
    COFF_offset = int.from_bytes(data[0x3C:0x40], "little")
    machine = int.from_bytes(data[COFF_offset + 4:COFF_offset + 6], "little")

    if machine == IMAGE_FILE_MACHINE_AMD64:
        return "amd64"
    elif machine == IMAGE_FILE_MACHINE_I386:
        return "i386"
    elif machine == IMAGE_FILE_MACHINE_ARM or machine == IMAGE_FILE_MACHINE_ARMNT:
        return "arm"
    elif machine == IMAGE_FILE_MACHINE_ARM64:
        return "arm64"
    else:
        raise NotImplementedError(f"Unsupported machine header {machine}")

def patch_module(architecture: str, dll_data: bytes) -> bytes:
    """
    Patch the Windows.ApplicationModel.Store module.

    This function applies architecture-specific patches to the 
    Windows.ApplicationModel.Store module based on the provided 
    architecture and DLL data.

    :param architecture: The architecture of the module.
    :type architecture: str
    :param dll_data: The Windows.ApplicationModel.Store module DLL 
                     as bytestring.
    :type dll_data: bytes

    :return: The patched DLL as bytestring.
    :rtype: bytes

    :raises NotImplementedError: If the architecture is unsupported.
    """
    dll_data = dll_data.hex()
    if architecture in PATCHES:
        for pattern, replace, count in PATCHES[architecture]:
            dll_data = pattern.sub(replace, dll_data, count)
    else:
        raise NotImplementedError(f"Unsupported architecture {architecture}")
    return bytes.fromhex(dll_data)
