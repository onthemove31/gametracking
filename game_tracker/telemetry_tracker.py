import psutil
import GPUtil
import platform
import datetime
import sqlite3
import os
import logging

# Load environment variables
telemetry_db_path = os.getenv('TELEMETRY_DB_PATH', 'data/telemetry.db')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection for telemetry data
telemetry_conn = sqlite3.connect(telemetry_db_path)
telemetry_cursor = telemetry_conn.cursor()

# Create the telemetry table if it doesn't exist
telemetry_cursor.execute('''CREATE TABLE IF NOT EXISTS telemetry (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                timestamp TEXT NOT NULL,
                                cpu_name TEXT,
                                memory_total REAL,
                                num_cores INTEGER,
                                gpu_model TEXT,
                                gpu_vendor TEXT,
                                gpu_memory_total REAL,
                                gpu_driver_version TEXT)''')

def get_cpu_info():
    """
    Retrieves CPU information including model name.
    """
    cpu_name = platform.processor()
    if not cpu_name:  # Fallback for some systems
        cpu_name = os.popen("wmic cpu get name").read().strip().split("\n")[1]
    return cpu_name

def get_memory_info():
    """
    Retrieves total system memory.
    """
    return psutil.virtual_memory().total / (1024 ** 3)  # Convert bytes to GB

def get_gpu_info():
    """
    Retrieves GPU information including model name, vendor, memory, and driver version.
    Handles NVIDIA, AMD, and Intel GPUs.
    """
    gpus = GPUtil.getGPUs()
    if gpus:
        gpu = gpus[0]  # Assuming the first GPU for simplicity
        logging.info(f"GPU Detected: Model={gpu.name}, Vendor={gpu.driver}, MemoryTotal={gpu.memoryTotal} MB, Driver={gpu.driver}")
        gpu_info = {
            "model": gpu.name,
            "vendor": "NVIDIA" if "nvidia" in gpu.driver.lower() else "Unknown",
            "memory_total": gpu.memoryTotal,
            "driver_version": gpu.driver
        }
        return gpu_info

    # Fallback for non-NVIDIA GPUs (AMD, Intel)
    system = platform.system()
    if system == 'Windows':
        try:
            import wmi
            w = wmi.WMI(namespace="root\CIMV2")
            for gpu in w.Win32_VideoController():
                gpu_info = {
                    "model": gpu.Name,
                    "vendor": gpu.AdapterCompatibility,
                    "memory_total": int(gpu.AdapterRAM) / (1024 ** 2),  # Convert bytes to MB
                    "driver_version": gpu.DriverVersion
                }
                return gpu_info
        except ImportError:
            logging.warning("WMI module not available, skipping AMD/Intel GPU detection.")

    elif system == 'Linux':
        try:
            import pyamdgpuinfo
            if pyamdgpuinfo.detect_gpus():
                gpu_info = {
                    "model": pyamdgpuinfo.query_gpu_model(),
                    "vendor": "AMD",
                    "memory_total": pyamdgpuinfo.query_memory_total(),
                    "driver_version": pyamdgpuinfo.query_driver_version()
                }
                return gpu_info
        except ImportError:
            logging.warning("pyamdgpuinfo module not available, skipping AMD GPU detection.")

    return {"model": "Unknown", "vendor": "Unknown", "memory_total": 0, "driver_version": "Unknown"}

def collect_telemetry():
    """
    Collects system telemetry information and stores it in the database.
    """
    logging.info("Collecting system telemetry information...")
    try:
        cpu_name = get_cpu_info()
        memory_total = get_memory_info()
        num_cores = psutil.cpu_count(logical=True)
        gpu_info = get_gpu_info()

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        telemetry_cursor.execute('''INSERT INTO telemetry (timestamp, cpu_name, memory_total, num_cores, gpu_model, gpu_vendor, gpu_memory_total, gpu_driver_version)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                                 (timestamp, cpu_name, memory_total, num_cores, gpu_info["model"], gpu_info["vendor"], gpu_info["memory_total"], gpu_info["driver_version"]))
        telemetry_conn.commit()

        logging.info(f"Telemetry data stored: CPU={cpu_name}, Memory={memory_total} GB, Cores={num_cores}, GPU Model={gpu_info['model']}, Vendor={gpu_info['vendor']}, Memory={gpu_info['memory_total']} MB, Driver={gpu_info['driver_version']}")

    except Exception as e:
        logging.error(f"Failed to collect telemetry: {e}", exc_info=True)

def close_telemetry_db():
    logging.info("Closing telemetry database connection.")
    telemetry_conn.close()

def main():
    logging.info("Starting telemetry tracking...")
    try:
        collect_telemetry()  # No arguments are needed
    finally:
        close_telemetry_db()
        logging.info("Telemetry tracking ended.")

if __name__ == "__main__":
    main()
