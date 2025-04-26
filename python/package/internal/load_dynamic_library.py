import ctypes, platform, os, sys
from pathlib import Path


package_dir = Path(__file__).parent.parent.resolve()
lib_path = os.path.join(package_dir, "dynamic_libs")

system = platform.system().lower()
arch = platform.machine().lower()

format_arch = ""
if sys.maxsize == 2**63 - 1:
    if arch in ("x86_64", "amd64"):
        format_arch = "amd64"
    elif arch in ("arm64", "aarch64"):
        format_arch = "arm64"
else:
    if arch in ("x86", "i686"):
        format_arch = "x86"


LIB = None

match system:
    case "windows":
        if format_arch == "amd64":
            LIB = ctypes.cdll.LoadLibrary(
                os.path.join(lib_path, "bedrock-world-operator_windows_amd64.dll")
            )
        elif format_arch == "x86":
            LIB = ctypes.cdll.LoadLibrary(
                os.path.join(lib_path, "bedrock-world-operator_windows_x86.dll")
            )
    case "darwin":
        if format_arch == "amd64":
            LIB = ctypes.cdll.LoadLibrary(
                os.path.join(lib_path, "bedrock-world-operator_macos_amd64.dylib")
            )
        elif format_arch == "arm64":
            LIB = ctypes.cdll.LoadLibrary(
                os.path.join(lib_path, "bedrock-world-operator_macos_arm64.dylib")
            )
    case _:
        if format_arch == "amd64":
            LIB = ctypes.cdll.LoadLibrary(
                os.path.join(lib_path, "bedrock-world-operator_linux_amd64.so")
            )
        elif format_arch == "arm64":
            if arch == "aarch64":
                LIB = ctypes.cdll.LoadLibrary(
                    os.path.join(lib_path, "bedrock-world-operator_android_arm64.so")
                )
            else:
                LIB = ctypes.cdll.LoadLibrary(
                    os.path.join(lib_path, "bedrock-world-operator_linux_arm64.so")
                )

if LIB is None:
    raise Exception(f"Your machine (system={system}, arch={arch}) is not supported.")
