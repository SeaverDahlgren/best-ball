import pygatt

# Define the UUID of the service and characteristic that we want to read
SERVICE_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"
CHARACTERISTIC_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"

# Define the MAC address of the Seeed XIAO
MAC_ADDRESS = "E9:61:17:0D:1B:D4"

# Callback function to be executed when data is received from the chip
def handle_data(handle, value):
    print(f"Received data: {value.hex()}")

# Create a GATT connection to the Seeed XIAO using the MAC address
adapter = pygatt.GATTToolBackend()
adapter.start()
device = adapter.connect(MAC_ADDRESS)

# Subscribe to the characteristic to start receiving data
device.subscribe(CHARACTERISTIC_UUID, callback=handle_data)

# Keep the program running to continue listening for data
while True:
    pass

# When finished, unsubscribe from the characteristic and disconnect from the device
device.unsubscribe(CHARACTERISTIC_UUID)
adapter.disconnect(device)
adapter.stop()

