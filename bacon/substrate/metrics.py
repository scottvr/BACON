import psutil

def get_system_metrics():
    """
    Gets system metrics using psutil.
    """
    virtual_mem = psutil.virtual_memory()
    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": virtual_mem.percent,
        "memory_available_gb": round(virtual_mem.available / (1024**3), 2),
        "disk_percent": psutil.disk_usage('/').percent,
    }
