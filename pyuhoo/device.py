from typing import Any, Dict


class Device(object):
    def __init__(self, device: dict) -> None:
        self._device: Dict[str,Any] = {}

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
        return f"<{self.__module__}.{self.__class__.__name__}(device={repr(self._device)})>"

    @property
    def calibration(self) -> int:
        return self._device["calibration"]

    @property
    def created_at(self) -> str:  # "YYYY-MM-DDThh:mm:ss.sssZ" UTC time
        return self._device["createdAt"]

    @property
    def home(self) -> Any: # type unknown
        return self._device["home"]

    @property
    def latitude(self) -> Any: # type unknown
        return self._device["latitude"]

    @property
    def longitude(self) -> Any: # type unknown
        return self._device["longitude"]

    @property
    def mac_address(self) -> str:
        return self._device["macAddress"]

    @property
    def name(self) -> str:
        return self._device["name"]

    @property
    def serial_number(self) -> str:
        return self._device["serialNumber"]

    @property
    def server(self) -> int:
        return self._device["server"]

    @property
    def ssid(self) -> str:
        return self._device["ssid"]

    @property
    def status(self) -> int:
        return self._device["status"]

    @property
    def location(self):
        return self._device["location"]

    @property
    def city(self):
        return self._device["city"]

    @property
    def city_ios(self):
        return self._device["city_ios"]

    @property
    def room_type(self):
        return self._device["RoomType"]

    @property
    def offline(self):
        return self._device["offline"]

    @property
    def offline_timestamp(self):
        return self._device["offline_timestamp"]

    def update_device(self, device: dict) -> None:
        self._device = { k:v for k,v in device.items() if k not in ("data","userSettings","threshold") }

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
