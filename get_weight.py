#!/usr/bin/env python3

# run \w sudo || from #root
# tested only on raspberry pi 3b and mi scale 2
# \w <3 @qbbr

import argparse
from bluepy.btle import Scanner, DefaultDelegate

# 1 - flags, 2 - Incomplete 16b Services, 255 - Manufacturer, 22 - 16b Service Data, 9 - Complete Local Name
SERVICE_DATA = 22  # [1d18828809e4070310112302]


class ScanDelegate(DefaultDelegate):
    def __init__(self, args):
        DefaultDelegate.__init__(self)
        self.mac_address = args.mac.upper()
        self.with_units = args.with_units
        self.is_verbose = args.verbose > 0
        self.last_raw_data = None

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if self.mac_address == dev.addr.upper():
            self.parseData(dev)

    def parseData(self, dev):
        if self.is_verbose:
            print('Device %s is %s, rssi: %d dBm, connectable: %s.' % (dev.addr, dev.addrType, dev.rssi, dev.connectable))

        for (adtype, desc, value) in dev.getScanData():
            if adtype == SERVICE_DATA and value.startswith('1d18'):
                raw_data = bytes.fromhex(value[4:])
                if raw_data == self.last_raw_data:
                    if self.is_verbose:
                        print("skip duplicate data")
                    return;

                is_stabilized = (raw_data[0] & (1 << 5)) != 0
                is_weight_removed = (raw_data[0] & (1 << 7)) != 0
                self.last_raw_data = raw_data

                if is_stabilized is True and is_weight_removed is False:
                    weight = int.from_bytes(raw_data[1:3], byteorder='little') / 100

                    if not self.with_units:
                        if (raw_data[0] & (1 << 1)) != 0:  # kg
                            weight /= 2  # catty to kg
                        print(weight)  # outout: 74.7
                    else:
                        if (raw_data[0] & (1 << 4)) != 0:  # chinese catty
                            unit = "jin"
                        elif (raw_data[0] & (1 << 2)) != 0:  # pound
                            unit = "lbs"
                        elif (raw_data[0] & (1 << 1)) != 0:  # kg
                            unit = "kg"
                            weight /= 2  # catty to kg
                        else:
                            unit = "unknown"

                        print(weight, unit)  # outout: 74.7 kg


def main():
    parser = argparse.ArgumentParser(description="Get Xiaomi Mi Smart Scale 2 weight.")
    parser.add_argument("mac", help="Device MAC address")
    parser.add_argument('--with-units', action='store_true', help="return weight \w units")
    parser.add_argument('--verbose', '-v', action='count', default=0)
    scanner = Scanner().withDelegate(ScanDelegate(parser.parse_args()))

    while True:
        scanner.start()
        scanner.process(2)
        scanner.stop()


if __name__ == "__main__":
    main()
