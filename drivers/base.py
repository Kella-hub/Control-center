from abc import ABC, abstractmethod
from typing import List, Dict
from core.devices import Device

class Driver(ABC):
    """
    Interface commune pour tous les drivers.
    N'importe quel driver (Simulation, Netmiko, etc.) devra respecter cette interface.
    """

    @abstractmethod
    def get_devices(self) -> List[Device]:
        """Récupère la liste de tous les équipements"""
        pass

    @abstractmethod
    def get_device_status(self, device_name: str) -> Dict:
        """Récupère le statut d'un équipement spécifique"""
        pass

    @abstractmethod
    def connect(self) -> bool:
        """Établit la connexion (simulation ou réelle)"""
        pass