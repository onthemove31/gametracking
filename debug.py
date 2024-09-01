import GPUtil
import logging

# Set up logging to print to console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def print_available_gpus():
    """
    Prints information about all available GPUs detected by GPUtil.
    """
    gpus = GPUtil.getGPUs()
    
    if not gpus:
        logging.info("No GPUs found or unsupported GPU type.")
        return

    for index, gpu in enumerate(gpus):
        logging.info(f"GPU {index + 1}:")
        logging.info(f"  Name: {gpu.name}")
        logging.info(f"  Driver: {gpu.driver}")
        logging.info(f"  GPU ID: {gpu.id}")
        logging.info(f"  GPU UUID: {gpu.uuid}")
        logging.info(f"  GPU Load: {gpu.load * 100}%")
        logging.info(f"  Total Memory: {gpu.memoryTotal} MB")
        logging.info(f"  Free Memory: {gpu.memoryFree} MB")
        logging.info(f"  Used Memory: {gpu.memoryUsed} MB")
        logging.info(f"  Temperature: {gpu.temperature} C")
        logging.info(f"  Vendor: {gpu.driver} (likely vendor-related information)")

if __name__ == "__main__":
    print_available_gpus()
