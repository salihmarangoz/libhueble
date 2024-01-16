import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QPushButton, QFileDialog, QGraphicsScene
from PySide6.QtCore import Slot, Qt, QDir
from PySide6.QtGui import QPixmap, QIcon, QImageReader, QGuiApplication

import libhueble
import asyncio

BLUETOOTH_ADDRESS = 'C1:F4:FA:FD:FB:78'

class MainWindow():
    def __init__(self):
        # Load window from ui file
        loader = QUiLoader()
        self.w = loader.load("main_window.ui", None)

        # Setup window
        self.w.setWindowTitle("Hue Control App")
        #app_icon = QIcon()
        #app_icon.addFile('icon.png')
        #self.w.setWindowIcon(app_icon)

        self.lamp = libhueble.Lamp(BLUETOOTH_ADDRESS)
        asyncio.get_event_loop().run_until_complete(self.lamp_connect())

        # Setup window elements
        self.setup_window_elements()

        # Show window
        self.w.show()

    def __del__(self):
        asyncio.get_event_loop().run_until_complete(self.lamp_disconnect())


    def setup_window_elements(self):
        # Setup 1st section

        # Connect push button actions to functions
        self.w.pushButton_on.clicked.connect(lambda l: asyncio.get_event_loop().run_until_complete(self.lamp_set_power(True)))
        self.w.pushButton_off.clicked.connect(lambda l: asyncio.get_event_loop().run_until_complete(self.lamp_set_power(False)))

        # Setup 2nd section

        current_brightness = asyncio.get_event_loop().run_until_complete(self.lamp_get_brightness())
        self.w.slider_brightness.setValue(int(current_brightness*100))

        current_temperature = asyncio.get_event_loop().run_until_complete(self.lamp_get_temperature())
        self.w.slider_temperature.setValue(int(current_temperature*100))

        # Connect slider and spinbox actions to lambda functions
        self.w.slider_brightness.valueChanged.connect(lambda l: asyncio.get_event_loop().run_until_complete(self.lamp_set_brightness( self.w.slider_brightness.value()/100 )) )
        self.w.slider_temperature.valueChanged.connect(lambda l: asyncio.get_event_loop().run_until_complete(self.lamp_set_temperature( self.w.slider_temperature.value()/100 )) )


    @Slot()
    def update_lcd_display(self, new_value):
        self.w.lcdNumber.display(new_value)

    async def lamp_connect(self):
        await self.lamp.connect()

    async def lamp_disconnect(self):
        await self.lamp.disconnect()

    async def lamp_set_power(self, state):
        await self.lamp.set_power(state)

    async def lamp_set_brightness(self, brightness):
        await self.lamp.set_brightness(brightness)

    async def lamp_set_temperature(self, temperature):
        await self.lamp.set_temperature(temperature)

    async def lamp_get_temperature(self):
        return await self.lamp.get_temperature()

    async def lamp_get_brightness(self):
        return await self.lamp.get_brightness()