import random
from datetime import datetime
from typing import List, Dict
from core.devices import Device, Router, Switch, EndDevice
from drivers.base import Driver

class SimulationDriver(Driver):
    """
    Driver de simulation.
    Il invente des données réalistes pour qu'on puisse développer
    sans avoir de vrais équipements.
    """

    def __init__(self):
        self.devices = self._create_fake_topology()
        self.connected = False

    def _create_fake_topology(self) -> List[Device]:
        """Crée une topologie fictive de départ"""
        devices = [
            Router("R1-Core", "192.168.1.1"),
            Router("R2-Edge", "192.168.1.2"),
            Switch("SW1-Access", "192.168.1.10"),
            Switch("SW2-Access", "192.168.1.11"),
            EndDevice("PC-Admin", "192.168.1.100"),
            EndDevice("Server-Web", "192.168.1.50"),
        ]

        # On donne des valeurs de CPU/Mémoire aléatoires réalistes
        for device in devices:
            device.cpu = random.randint(5, 45)
            device.memory = random.randint(20, 70)
            device.status = "up"

        return devices

    def connect(self) -> bool:
        """Simule une connexion réussie"""
        self.connected = True
        return True

    def get_devices(self) -> List[Device]:
        """Retourne la liste des équipements + met à jour les métriques"""
        # On fait varier un peu le CPU et la mémoire à chaque appel
        for device in self.devices:
            device.cpu = max(1, min(95, device.cpu + random.randint(-5, 5)))
            device.memory = max(10, min(90, device.memory + random.randint(-3, 3)))
            device.last_seen = datetime.now()

        return self.devices

    def get_device_status(self, device_name: str) -> Dict:
        """Retourne les infos d'un équipement par son nom"""
        for device in self.devices:
            if device.name == device_name:
                return device.get_info()
        return {"error": f"Équipement {device_name} non trouvé"}