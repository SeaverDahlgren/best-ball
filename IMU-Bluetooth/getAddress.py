import bluetooth

addr = None
name = "XIAO" # Name of your Seeed XIAO chip
timeout = 5 # Number of seconds to search for the device

# Search for the device
devices = bluetooth.discover_devices(duration=timeout, lookup_names=True)

# Find the address of the device with the matching name
for device in devices:
    if name == device[1]:
        addr = device[0]
        break

if addr is None:
    print("Could not find device with name " + name)
else:
    print("MAC address of " + name + " is " + addr)

