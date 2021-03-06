# mi-scale-2

Get Xiaomi Mi Smart Scale 2 weight

## Requirements

 * python3
 * bluepy
 * root permission for `bluepy.btle`

```bash
sudo pip install -r requirements.txt
```

## Usage

run \w sudo || from #root:

```bash
sudo ./get_weight.py 00:00:00:00:00:00
# ./get_weight.py 00:00:00:00:00:00 --with-units
# ./get_weight.py 00:00:00:00:00:00 --verbose
# ./get_weight.py --help
```

## Help

get dev mac address:

```bash
sudo hcitool lescan
```

if u hv troubleshoots \w dev - restart u bluetooth/adapter

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
