import os, ctypes, platform
from pathlib import Path

LIB = None

package_dir = Path(__file__).parent.parent.resolve()
lib_path = os.path.join(package_dir, "dynamic_libs")

system = platform.system().lower()
arch = platform.machine().lower()

match system:
    case "windows":
        if arch == "amd64":
            LIB = ctypes.cdll.LoadLibrary(
                os.path.join(lib_path, "bedrock-world-operator_windows_amd64.dll")
            )
        elif arch == "x86_64":
            LIB = ctypes.cdll.LoadLibrary(
                os.path.join(lib_path, "bedrock-world-operator_windows_x86.dll")
            )
    case "darwin":
        if arch == "amd64":
            LIB = ctypes.cdll.LoadLibrary(
                os.path.join(lib_path, "bedrock-world-operator_macos_amd64.dylib")
            )
        elif arch == "arm64":
            LIB = ctypes.cdll.LoadLibrary(
                os.path.join(lib_path, "bedrock-world-operator_macos_arm64.dylib")
            )
    case _:
        if arch == "aarch64":
            LIB = ctypes.cdll.LoadLibrary(
                os.path.join(lib_path, "bedrock-world-operator_android_arm64.so")
            )
        elif arch == "amd64":
            LIB = ctypes.cdll.LoadLibrary(
                os.path.join(lib_path, "bedrock-world-operator_linux_amd64.so")
            )
        elif arch == "arm64":
            LIB = ctypes.cdll.LoadLibrary(
                os.path.join(lib_path, "bedrock-world-operator_linux_arm64.so")
            )

if LIB is None:
    raise FileNotFoundError("Your machine is not supported.")
