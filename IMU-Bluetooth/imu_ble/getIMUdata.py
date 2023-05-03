import simplepyble
import struct
import imuPOST

NUM_CHIPS = 1
def pair_chips():
    adapters = simplepyble.Adapter.get_adapters()
    service_uuid, characteristic_uuid = "", ""

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
        service_characteristic_pair = []
        for service in services:
            for characteristic in service.characteristics():
                service_characteristic_pair.append((service.uuid(), characteristic.uuid()))

        # Query the user to pick a service/characteristic pair
        print("Please select a service/characteristic pair:")
        for i, (service_uuid, characteristic) in enumerate(service_characteristic_pair):
            print(f"{i}: {service_uuid} {characteristic}")

        choice = int(input("Enter choice: "))
        service_uuid, characteristic_uuid = service_characteristic_pair[choice]
        imu_chips.append(peripheral)
    return imu_chips, service_uuid, characteristic_uuid

def print_notif(data, chip):
    float_value = struct.unpack('f', data)
    print("Address %s" % chip.address())
    print("msg Contents: %.2f" % float_value)

if __name__ == "__main__":
    imu_chips, service_uuid, characteristic_uuid = pair_chips()
    # Write the content to the characteristic
    for chip in imu_chips:
        chip.notify(service_uuid, characteristic_uuid, lambda data: print_notif(data, chip))

    while(1):
        pass

    for chip in imu_chips:
        chip.disconnect()
