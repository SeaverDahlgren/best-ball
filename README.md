# best-ball
Capstone Spring 2023


## 3/31 - Test IMU bluetooth
1. Double tap Chip reset to remove current chip firmware
2. Upload arduino code to chip.
3. Connect to app on phone.
4. Look for "Arduino"
5. Select "Hex" in the top right corner of app and switch to "Float"
6. Select "enable notifications" on app to get constant stream of floats


## 4/21 - Receive Bluetooth
We are using a Python module called SimpleBLE. It can be found here: https://github.com/OpenBluetoothToolbox/SimpleBLE
I (seaver) created a Fork of this module and I pushed it here: https://github.com/SeaverDahlgren/SimpleBLE
This is how to use the library:
1. clone the repo
2. cd into the main repo
3. run `pip install .`

To use the module in a Python file run: `import simplepyble`
