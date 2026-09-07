from datetime import datetime

class Device:
    """Classe de base pour tous les équipements réseau"""

    def __init__(self, name: str, ip: str, device_type: str):
        self.name = name
        self.ip = ip
        self.device_type = device_type
        self.status = "up"          # up ou down
        self.cpu = 0                # en %
        self.memory = 0             # en %
        self.last_seen = datetime.now()

    def get_info(self) -> dict:
        """Retourne les informations de l'équipement sous forme de dictionnaire"""
        return {
            "name": self.name,
            "ip": self.ip,
            "type": self.device_type,
            "status": self.status,
            "cpu": self.cpu,
            "memory": self.memory,
            "last_seen": self.last_seen.strftime("%Y-%m-%d %H:%M:%S")
        }

    def __str__(self):
        return f"{self.name} ({self.ip}) - {self.status}"


class Router(Device):
    """Classe pour les routeurs"""

    def __init__(self, name: str, ip: str):
        super().__init__(name, ip, device_type="router")


class Switch(Device):
    """Classe pour les switches"""

    def __init__(self, name: str, ip: str):
        super().__init__(name, ip, device_type="switch")


class EndDevice(Device):
    """Classe pour les équipements finaux (PC, serveur...)"""

    def __init__(self, name: str, ip: str):
        super().__init__(name, ip, device_type="end_device")