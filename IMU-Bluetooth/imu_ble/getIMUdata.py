import simplepyble
import struct
import imuPOST
from datetime import *

'''
BC8CE2F1-BF64-F2BE-4947-1333F248D42C - Seaver's
B7839721-AE2B-A4A0-B2BC-2BA551BF556A - Seaver's
72200B5C-EAFA-6E24-DE5A-BA8247C72E72 - Inside Ball: ball1
7DCD0CFE-640A-E67D-0DF7-76E621CECB8B - tamago: ball2
154176C3-177E-D211-E633-803022CC07A5 - Putter
'''
chip_ids = {
                '72200B5C-EAFA-6E24-DE5A-BA8247C72E72': 1,
                '7DCD0CFE-640A-E67D-0DF7-76E621CECB8B': 2,
                '154176C3-177E-D211-E633-803022CC07A5': 3
           }

curr_ball_spin = {}
curr_ball_spin[1] = 0
curr_ball_spin[2] = 0
putter_state = [0]
prev_ball_time = [datetime.now()]*4
ball_stat_count = [0]*4
STAT_INTERVAL = 20
NUM_CHIPS = 2
def pair_chips():
    adapters = simplepyble.Adapter.get_adapters()
    service_uuid, characteristic_uuid = "", ""
    service_characteristic_pair = []

    if len(adapters) == 0:
        print("No adapters found")

    # Query the user to pick an adapter
    # print("Please select an adapter:")
    # for i, adapter in enumerate(adapters):
    #     print(f"{i}: {adapter.identifier()} [{adapter.address()}]")

    # choice = int(input("Enter choice: "))
    default = 0
    adapter = adapters[default]

    print(f"Selected adapter: {adapter.identifier()} [{adapter.address()}]")

    adapter.set_callback_on_scan_start(lambda: print("Scan started."))
    adapter.set_callback_on_scan_stop(lambda: print("Scan complete."))
    adapter.set_callback_on_scan_found(lambda peripheral: print(f"Found {peripheral.identifier()} [{peripheral.address()}]"))

    # Scan for 5 seconds
    adapter.scan_for(3000)
    peripherals = adapter.scan_get_results()

    # Query the user to pick a peripheral
    imu_chips = []
    for j in range(NUM_CHIPS):
        print("Please select a peripheral:")
        for i, peripheral in enumerate(peripherals):
            print(f"{i}: {peripheral.identifier()} [{peripheral.address()}]")

        choice = int(input("Enter choice: "))
        peripheral = peripherals[choice]

        print(f"Connecting to: {peripheral.identifier()} [{peripheral.address()}]")
        peripheral.connect()

        print("Successfully connected, listing services...")
        services = peripheral.services()
        for service in services:
            for characteristic in service.characteristics():
                if (service.uuid(), characteristic.uuid()) not in service_characteristic_pair:
                    service_characteristic_pair.append((service.uuid(), characteristic.uuid()))

        for service, characteristic in service_characteristic_pair:
            print(service, characteristic)

        imu_chips.append(peripheral)
    return imu_chips, service_characteristic_pair

def print_notif(data, chip):
    float_value = struct.unpack('f', data)
    #print("Address %s" % chip.address())
    #print("msg Contents: %.2f" % float_value)
    handle_chip_spin(data, chip)

def handle_putter(data, chip):
    int_val = struct.unpack('i', data)
    #print("Address %s" % chip.address())
    #print("msg Contents: %d" % int_val)
    putter_state[0] = int_val[0]
    print("Put State = ", putter_state)

def handle_chip_accel(data, chip):
    float_value = struct.unpack('f', data)
    new_accel = float_value[0]
    chip_id = chip_ids[chip.address()]

    if (curr_ball_spin[chip_id] == 0 and new_accel > 10):
        print("SENDING A MESSAGE")
        imuPOST.add_stroke(chip_id)

def handle_chip_spin(data, chip):
    float_value = struct.unpack('f', data)
    new_spin = float_value[0]
    chip_id = chip_ids[chip.address()]
    print("chip id", chip_id)
    curr_ball_spin[chip_id] = float_value
    if prev_ball_time[chip_id] + timedelta(seconds=1) < datetime.now():
        print("SENDING A MESSAGE")
        imuPOST.add_stroke(chip_id)
        print("put state", putter_state[0])
        imuPOST.set_club_state(chip_id, putter_state[0])
    prev_ball_time[chip_id] = datetime.now()
    if ball_stat_count[chip_id] % STAT_INTERVAL == 0:
        imuPOST.set_spin(chip_id, float_value)
    ball_stat_count[chip_id] += 1

if __name__ == "__main__":
    imu_chips, service_characteristic_pairs = pair_chips()
    # Write the content to the characteristic
    for chip in imu_chips:
        for service_uuid, characteristic_uuid in service_characteristic_pairs:
            if chip.address() != '154176C3-177E-D211-E633-803022CC07A5':
                chip.notify(service_uuid, characteristic_uuid, lambda data: print_notif(data, chip))
            else:
                chip.notify(service_uuid, characteristic_uuid, lambda data: handle_putter(data, chip))
    while(1):
        pass

    for chip in imu_chips:
        chip.disconnect()

