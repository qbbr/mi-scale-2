# mi-scale-2

Get Xiaomi Mi Smart Scale 2 weight \w unit

## Requirements

 * python3 + bluepy

```bash
sudo pip install -r requirements.txt
```

## Usage

run \w sudo || from #root:

```
sudo ./get_weight.py --mac 00:00:00:00:00:00
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

## Links

 * https://github.com/oliexdev/openScale/wiki/Xiaomi-Bluetooth-Mi-Scale
