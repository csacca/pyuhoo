from typing import Any


class Device(object):
    def __init__(self, device: dict) -> None:
        self.calibration: int
        self.created_at: str  # "YYYY-MM-DDThh:mm:ss.sssZ" UTC time
        self.home: Any  # type unknown
        self.latitude: Any  # type unknown
        self.longitude: Any  # type unknown
        self.mac_address: str
        self.name: str
        self.serial_number: str
        self.server: int
        self.ssid: str
        self.status: int

        self.co: float  # might be an int
        self.co2: float  # might be an int
        self.dust: float
        self.humidity: float
        self.no2: float
        self.ozone: float
        self.pressure: float
        self.temp: float
        self.timestamp: int
        self.voc: float  # might be an int

        self.update_device(device)
        self.timestamp = -1

    def __repr__(self):
        return f"<{self.__module__}.{self.__class__.__name__} serial_number: {self.serial_number!r}>"

    def update_device(self, device: dict) -> None:
        self.calibration = device["calibration"]
        self.created_at = device["createdAt"]
        self.home = device["home"]
        self.latitude = device["latitude"]
        self.longitude = device["longitude"]
        self.mac_address = device["macAddress"]
        self.name = device["name"]
        self.serial_number = device["serialNumber"]
        self.server = device["server"]
        self.ssid = device["ssid"]
        self.status = device["status"]

    # Maps data key values to struct values
    _DATA_MAPPING = {
        "co" : "co",
        "co2" : "co2",
        "dust" : "dust",
        "humidity" : "humidity",
        "no2" : "no2",
        "ozone" : "ozone",
        "pressure" : "pressure",
        "temp" : "temp",
        "timestamp" : "timestamp",
        "voc" : "voc",
    }

    def update_data(self, data: dict) -> None:
        # The format has been changed - now these values return directly.
        # Since this might not be globally consistent, we'll check each one.
        for value_name, attr_name in self._DATA_MAPPING.items():
            if isinstance(data[value_name], dict):
                setattr(self, attr_name, data[value_name]["value"])
            else:
                setattr(self, attr_name, data[value_name])
