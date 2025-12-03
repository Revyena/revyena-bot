import psutil
import sys

class InformationUtilities:
    @staticmethod
    def get_python_info():
        return {
            "python_version": sys.version.split(" ")[0],
            "implementation": sys.implementation.name,
            "executable": sys.executable,
            "platform": sys.platform
        }

    @staticmethod
    def get_hardware_usage_info():
        ram = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        divide_amount = 1_000_000_000  # Convert bytes to gigabytes
        return {
            "ram_total": round(ram.total / divide_amount, 2),
            "ram_used": round(ram.used / divide_amount, 2),
            "ram_used_percent": round((ram.used / ram.total) * 100, 2),
            "disk_total": round(disk_usage.total / divide_amount, 2),
            "disk_used": round(disk_usage.used / divide_amount, 2),
            "disk_free": round(disk_usage.free / divide_amount, 2),
            "disk_free_percent": round(disk_usage.free / disk_usage.total * 100, 2)
        }