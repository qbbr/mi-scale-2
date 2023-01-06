# mi-scale-2

[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://github.com/vshymanskyy/StandWithUkraine/blob/main/docs/README.md)

Get Xiaomi Mi Smart Scale 2 weight and publishing to mqtt

*Tested only on Raspberry Pi 3b + Mi Scale 2*

## Requirements

 * python3
 * python-dotenv
 * bluepy
 * paho-mqtt
 * root permission for `bluepy.btle`

```bash
sudo pip install -r requirements.txt
```

## Usage

always run with `sudo` or from `root`:

```bash
cp .env.dist .env
vim .env
sudo ./main.py
# sudo ./main.py --help
# sudo ./main.py --loglevel=DEBUG
```

## Autostart

```bash
sudo cp mi-scale-2.service /etc/systemd/system/
sudo systemctl enable mi-scale-2
sudo systemctl start mi-scale-2
```

## Integrate with Home Assistant

[![qbbr-mi-scale-2-home-assistant-integration](https://i.imgur.com/rRetkYZ.png)](https://i.imgur.com/rRetkYZ.png)

```yaml
# configuration.yaml:
mqtt:
    sensor:
      - name: "my_weight"
        state_topic: "miscale/qbbr/weight"
        force_update: true
        unit_of_measurement: "kg"
        state_class: "measurement"
        icon: mdi:scale

# customize.yaml:
sensor.my_weight:
    friendly_name: Мой вес
```

## Help

get dev mac address:

```bash
sudo hcitool lescan
```

if u have troubleshoots, try restart u bluetooth/adapter

```bash
sudo hciconfig hci0 reset
sudo invoke-rc.d bluetooth restart
```

### Reverse Engineering RAW Schema for Mi Scale 2

!!! *slightly different than from openScale wiki* !!!

**byte 0:**

- 0 bit - unknown
- 1 bit - unit kg
- 2 bit - unit lbs
- 3 bit - unknown
- 4 bit - jin (chinese catty) unit
- 5 bit - stabilized
- 6 bit - unknown
- 7 bit - weight removed

**byte 1-2:**
 - weight (little endian)

## Links

 * https://github.com/oliexdev/openScale/wiki/Xiaomi-Bluetooth-Mi-Scale
