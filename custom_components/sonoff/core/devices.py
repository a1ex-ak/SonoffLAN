"""
Each device has a specification - list of classes (XEntity childs)

XEntity properties:
- params - required, set of parameters that this entity can read
- param - optional, entity main parameter (useful for sensors)
- uid - optional, entity unique_id tail

spec - function can change default class with some options

device_class - can override platform for switch entity
"""
from typing import Optional

from aiomusiccast.capabilities import BinarySensor
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity

from ..binary_sensor import XBinarySensor, XZigbeeMotion, XZigbeeDoor
from ..cover import XCover, XCoverDualR3
from ..fan import XFan, XDiffuserFan, XToggleFan
from ..light import *
from ..remote import XRemote
from ..sensor import XSensor, XZigbeeButton, XUnknown
from ..switch import XSwitch, XSwitches, XSwitchTH, XToggle

# supported custom device_class
DEVICE_CLASS = {
    "binary_sensor": (XEntity, BinarySensor),
    "fan": (XToggleFan,),  # using custom class for overriding is_on function
    "light": (XEntity, LightEntity),
    "sensor": (XEntity, SensorEntity),
    "switch": (XEntity, SwitchEntity),
}


def spec(cls, enabled=None, base=None, **kwargs):
    if enabled is not None:
        kwargs["_attr_entity_registry_enabled_default"] = enabled
    bases = DEVICE_CLASS[base] if base else (cls,)
    return type(cls.__name__, bases, {**cls.__dict__, **kwargs})


Switch1 = spec(XSwitches, channel=0, uid="1")
Switch2 = spec(XSwitches, channel=1, uid="2")
Switch3 = spec(XSwitches, channel=2, uid="3")
Switch4 = spec(XSwitches, channel=3, uid="4")

XSensor100 = spec(XSensor, multiply=0.01, round=2)

Battery = spec(XSensor, param="battery")
LED = spec(XToggle, param="sledOnline", uid="led", enabled=False)
RSSI = spec(XSensor, param="rssi", enabled=False)

SPEC_SWITCH = [XSwitch, LED, RSSI]
SPEC_1CH = [Switch1]
SPEC_2CH = [Switch1, Switch2]
SPEC_3CH = [Switch1, Switch2, Switch3]
SPEC_4CH = [Switch1, Switch2, Switch3, Switch4]

DEVICES = {
    1: SPEC_SWITCH,
    2: SPEC_2CH,
    3: SPEC_3CH,
    4: SPEC_4CH,
    5: SPEC_SWITCH,
    6: SPEC_SWITCH,
    7: SPEC_2CH,  # Sonoff T1 2CH
    8: SPEC_3CH,  # Sonoff T1 3CH
    9: SPEC_4CH,
    11: [XCover, LED, RSSI],  # King Art - King Q4 Cover (only cloud)
    14: SPEC_SWITCH,  # Sonoff Basic (3rd party)
    15: [
        XSwitchTH, LED, RSSI,
        spec(XSensor, param="currentTemperature", uid="temperature", round=1),
        spec(XSensor, param="currentHumidity", uid="humidity"),
    ],  # Sonoff TH16
    18: [
        spec(XSensor, param="temperature"),
        spec(XSensor, param="humidity"),
        spec(XSensor, param="dusty"),
        spec(XSensor, param="light"),
        spec(XSensor, param="noise"),
    ],
    22: [XLightB1],  # Sonoff B1 (only cloud)
    # https://github.com/AlexxIT/SonoffLAN/issues/173
    25: [XDiffuserFan, XDiffuserLight],  # Diffuser
    28: [XRemote, LED, RSSI],  # Sonoff RF Brigde 433
    29: SPEC_2CH,
    30: SPEC_3CH,
    31: SPEC_4CH,
    32: [
        XSwitch, LED, RSSI,
        spec(XSensor, param="current"),
        spec(XSensor, param="power"),
        spec(XSensor, param="voltage"),
    ],  # Sonoff Pow
    34: [XFan, XFanLight],  # Sonoff iFan02 and iFan03
    36: [XDimmer],  # KING-M4 (dimmer, only cloud)
    44: [XLightD1],  # Sonoff D1
    57: [XLight57],  # Mosquito Killer Lamp
    59: [XLightLED],  # Sonoff LED (only cloud)
    # 66: switch1,  # ZigBee Bridge
    77: SPEC_1CH,  # Sonoff Micro
    78: SPEC_1CH,
    81: SPEC_1CH,
    82: SPEC_2CH,
    83: SPEC_3CH,
    84: SPEC_4CH,
    102: [XBinarySensor, Battery, RSSI],  # Sonoff DW2 Door/Window sensor
    103: [XLightB02],  # Sonoff B02 CCT bulb
    104: [XLightB05],  # Sonoff B05 RGB+CCT color bulb
    107: SPEC_1CH,
    126: [
        Switch1, Switch2,
        spec(XSensor100, param="current_00", uid="current_1"),
        spec(XSensor100, param="current_01", uid="current_2"),
        spec(XSensor100, param="voltage_00", uid="voltage_1"),
        spec(XSensor100, param="voltage_01", uid="voltage_2"),
        spec(XSensor100, param="actPow_00", uid="power_1"),
        spec(XSensor100, param="actPow_01", uid="power_2"),
    ],  # Sonoff DualR3
    182: [
        Switch1, LED, RSSI,
        spec(XSensor, param="current"),
        spec(XSensor, param="power"),
        spec(XSensor, param="voltage"),
    ],  # Sonoff S40
    1000: [XZigbeeButton, Battery],  # zigbee_ON_OFF_SWITCH_1000
    1256: [XZigbeeLigth],  # ZCL_HA_DEVICEID_ON_OFF_LIGHT
    1770: [
        spec(XSensor100, param="temperature"),
        spec(XSensor100, param="humidity"),
        Battery,
    ],  # ZCL_HA_DEVICEID_TEMPERATURE_SENSOR
    2026: [XZigbeeMotion, Battery],  # ZIGBEE_MOBILE_SENSOR
    3026: [XZigbeeDoor, Battery],  # ZIGBEE_DOOR_AND_WINDOW_SENSOR
}

DIY = {
    # DIY type, UIID, Brand, Model/Name
    "plug": [1, None, "Single Channel DIY"],
    "strip": [4, None, "Multi Channel DIY"],
    "diy_plug": [1, "SONOFF", "MINI DIY"],
    "enhanced_plug": [5, "SONOFF", "POW DIY"],
    "th_plug": [15, "SONOFF", "TH DIY"],
    "rf": [28, "SONOFF", "RFBridge DIY"],
    "fan_light": [34, "SONOFF", "iFan DIY"],
    "light": [44, "SONOFF", "D1 DIY"],
    "multifun_switch": [126, "SONOFF", "DualR3 DIY"],
}


def set_default_class(device_class: str):
    XSwitch.__bases__ = XSwitches.__bases__ = XSwitchTH.__bases__ = (
        XEntity, LightEntity if device_class == "light" else SwitchEntity
    )


def get_spec(device: dict) -> Optional[list]:
    uiid = device["extra"]["uiid"]
    # DualR3 in cover mode
    if uiid == 126 and device["params"].get("workMode") == 2:
        return [XCoverDualR3]

    if uiid in DEVICES:
        classes = DEVICES[uiid]
    elif "switch" in device["params"]:
        classes = SPEC_SWITCH
    elif "switches" in device["params"]:
        classes = SPEC_4CH
    else:
        classes = [XUnknown]

    if "device_class" in device:
        classes = get_custom_spec(classes, device["device_class"])

    return classes


def get_custom_spec(classes: list, device_class):
    """Supported device_class formats:
    1. Single channel:
       device_class: light
    2. Multiple channels:
       device_class: [light, fan, switch]
    3. Light with brightness control
       device_class:
         - switch  # entity 1 (channel 1)
         - light: [2, 3]  # entity 2 (channels 2 and 3)
         - fan: 4  # entity 3 (channel 4)
    """
    # 1. single channel
    if isinstance(device_class, str):
        classes[0] = spec(classes[0], base=device_class)

    elif isinstance(device_class, list):
        # remove all default multichannel classes from spec
        classes = [cls for cls in classes if XSwitches not in cls.__bases__]

        for i, sub_class in enumerate(device_class):
            # 2. simple multichannel
            if isinstance(sub_class, str):
                classes.append(spec(
                    XSwitches, channel=i, uid=str(i + 1), base=sub_class
                ))

            elif isinstance(sub_class, dict):
                sub_class, i = next(iter(sub_class.items()))

                # 3. light with brightness
                if isinstance(i, list) and sub_class == "light":
                    channels = [i - 1 for i in i]
                    classes.append(spec(XLightGroup, channels=channels))

                # 4. multichannel
                elif isinstance(i, int):
                    classes.append(spec(
                        XSwitches, channel=(i - 1), uid=str(i), base=sub_class
                    ))

    return classes


def setup_diy(device: dict) -> dict:
    uiid, brand, model = DIY.get(device["diy"])
    device.setdefault("name", model)
    device["brandName"] = brand
    device["extra"] = {"uiid": uiid}
    device["online"] = False
    device["productModel"] = model
    return device
