# libhueble

A library for controlling your Bluetooth-capable Philips Hue lights directly using Bluetooth Low Energy (BLE) without a bridge.

## Pairing

1. In the Hue BT app, go to **Settings** > **Voice Assistants** > **Amazon Alexa** and tap **Make visible**.¹
2. Open the bluetoothctl shell:
   ```
   sudo bluetoothctl
   ```
3. Start the discovery:
   ```
   scan on
   ```
4. Write down the MAC address of your light.
5. Pair to your light:
   ```
   pair [MAC address]
   trust [MAC address]
   ```
6. Done, you can now pair the light to your phone again.

¹ [Thanks to @danieleds.](https://github.com/alexhorn/laemp/issues/1)

## Usage

```
lamp = Lamp('00:11:22:33:44:55')
await lamp.connect()
try:
   await lamp.set_power(True)
   await lamp.set_brightness(1.0)
   await lamp.set_color_rgb(1.0, 0.0, 0.0)
finally:
   await lamp.disconnect()
```

## Usage (Wake-up Routine)

- Set the parameters in the `examples/wake_up.py` script.
- Add the script to the "Startup Applications".

![startup_configuration](startup_configuration.png)

## Usage (GUI)

![hue_gui](examples/pyside_app/hue_gui.png)

```bash
# Add to .bashrc, maybe...
function hue_gui()
{
    (cd "/home/salih/Github/libhueble/examples/pyside_app"; python "/home/salih/Github/libhueble/examples/pyside_app/my_app.py")
}
```



## Compatibility

Works on Raspbian Buster.

Sometimes it also works on Windows 10 20H2, but it is very flaky.

## Credits

This is pieced together from the reverse engineering efforts of other people on the internet.

Sources:
* https://github.com/npaun/philble
* https://gist.github.com/shinyquagsire23/f7907fdf6b470200702e75a30135caf3
* https://www.reddit.com/r/Hue/comments/eq0y3y/philips_hue_bluetooth_developer_documentation
