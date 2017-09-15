"""
This is a simple API for reading data from a micro:bit.

You will need the Bluetooth services on the micro:bit exposed.

This code was developed using the 'Bluetooth Most Services, No Security'
micro:bit hex file from:
http://www.bittysoftware.com/downloads.html
The hex file called "For micro:bit Blue - Main Bluetooth services,
pairing not required" was used.

The following link is a good reference for Bluetooth on the microbit
http://bluetooth-mdw.blogspot.co.uk/p/bbc-microbit.html
"""
from time import sleep

from bluezero import central
from bluezero import tools

import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

ACCEL_SRV = 'E95D0753-251D-470A-A062-FA1922DFA9A8'
ACCEL_DATA = 'E95DCA4B-251D-470A-A062-FA1922DFA9A8'
ACCEL_PERIOD = 'E95DFB24-251D-470A-A062-FA1922DFA9A8'
MAGNETO_SRV = 'E95DF2D8-251D-470A-A062-FA1922DFA9A8'
MAGNETO_DATA = 'E95DFB11-251D-470A-A062-FA1922DFA9A8'
MAGNETO_PERIOD = 'E95D386C-251D-470A-A062-FA1922DFA9A8'
MAGNETO_BEARING = 'E95D9715-251D-470A-A062-FA1922DFA9A8'
BTN_SRV = 'E95D9882-251D-470A-A062-FA1922DFA9A8'
BTN_A_STATE = 'E95DDA90-251D-470A-A062-FA1922DFA9A8'
BTN_B_STATE = 'E95DDA91-251D-470A-A062-FA1922DFA9A8'
IO_PIN_SRV = 'E95D127B-251D-470A-A062-FA1922DFA9A8'
IO_PIN_DATA = 'E95D8D00-251D-470A-A062-FA1922DFA9A8'
IO_AD_CONFIG = 'E95D5899-251D-470A-A062-FA1922DFA9A8'
IO_PIN_CONFIG = 'E95DB9FE-251D-470A-A062-FA1922DFA9A8'
IO_PIN_PWM = 'E95DD822-251D-470A-A062-FA1922DFA9A8'
LED_SRV = 'E95DD91D-251D-470A-A062-FA1922DFA9A8'
LED_STATE = 'E95D7B77-251D-470A-A062-FA1922DFA9A8'
LED_TEXT = 'E95D93EE-251D-470A-A062-FA1922DFA9A8'
LED_SCROLL = 'E95D0D2D-251D-470A-A062-FA1922DFA9A8'
TEMP_SRV = 'E95D6100-251D-470A-A062-FA1922DFA9A8'
TEMP_DATA = 'E95D9250-251D-470A-A062-FA1922DFA9A8'
TEMP_PERIOD = 'E95D1B25-251D-470A-A062-FA1922DFA9A8'

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
logger.addHandler(NullHandler())


class Microbit:
    """
    Class to simplify interacting with a micro:bit over Bluetooth Low Energy
    """
    def __init__(self, device_addr, adapter_addr=None):
        """
        Initialization of an instance of a remote micro:bit
        :param device_addr: Discovered microbit device with this address
        :param adapter_addr: Optional unless you have more than one adapter
                             on your machine
        """
        self.ubit = central.Central(adapter_addr=adapter_addr,
                                    device_addr=device_addr)

        # Micro:bit Characteristics
        self._accel_data = self.ubit.add_characteristic(ACCEL_SRV,
                                                        ACCEL_DATA)
        self._accel_period = self.ubit.add_characteristic(ACCEL_SRV,
                                                          ACCEL_PERIOD)
        self._magneto_data = self.ubit.add_characteristic(MAGNETO_SRV,
                                                          MAGNETO_DATA)
        self._magneto_period = self.ubit.add_characteristic(MAGNETO_SRV,
                                                            MAGNETO_PERIOD)
        self._magneto_bearing = self.ubit.add_characteristic(MAGNETO_SRV,
                                                             MAGNETO_BEARING)
        self._btn_a_state = self.ubit.add_characteristic(BTN_SRV,
                                                         BTN_A_STATE)
        self._btn_b_state = self.ubit.add_characteristic(BTN_SRV,
                                                         BTN_B_STATE)
        self._io_pin_data = self.ubit.add_characteristic(IO_PIN_SRV,
                                                         IO_PIN_DATA)
        self._io_ad_config = self.ubit.add_characteristic(IO_PIN_SRV,
                                                          IO_AD_CONFIG)
        self._io_pin_config = self.ubit.add_characteristic(IO_PIN_SRV,
                                                           IO_PIN_CONFIG)
        self._io_pin_pwm = self.ubit.add_characteristic(IO_PIN_SRV,
                                                        IO_PIN_PWM)
        self._led_state = self.ubit.add_characteristic(LED_SRV,
                                                       LED_STATE)
        self._led_text = self.ubit.add_characteristic(LED_SRV,
                                                      LED_TEXT)
        self._led_scroll = self.ubit.add_characteristic(LED_SRV,
                                                        LED_SCROLL)
        self._temp_data = self.ubit.add_characteristic(TEMP_SRV,
                                                       TEMP_DATA)
        self._temp_period = self.ubit.add_characteristic(TEMP_SRV,
                                                         TEMP_PERIOD)

    @property
    def connected(self):
        """Indicate whether the remote device is currently connected."""
        return self.ubit.connected

    def connect(self):
        """
        Connect to the specified micro:bit for this instance
        """
        self.ubit.connect()
        while not self.ubit.services_resolved:
            sleep(0.5)
        self.ubit.load_gatt()

    def disconnect(self):
        """
        Disconnect from the micro:bit
        """
        self.ubit.disconnect()

    @property
    def scroll_delay(self):
        return int.from_bytes(self._led_scroll.value,
                              byteorder='little',
                              signed=False)

    @scroll_delay.setter
    def scroll_delay(self, delay=None):
        """
        Specifies a millisecond delay to wait for in between showing each
        character on the display.
        """
        if delay < 0:
            delay = 0
        elif delay > 2**16:
            delay = 2**16
        self._led_scroll.value = tools.int_to_uint16(delay)

    @property
    def text(self):
        pass

    @text.setter
    def text(self, words):
        """
        Specify text to be displayed. Limit of 20 characters.
        The content will be restricted to that number of characters.
        :param words:
        """
        data = []
        text = ''
        if len(words) > 20:
            text = words[:19]
        else:
            text = words
        for letter in text:
            data.append(ord(letter))
        self._led_text.value = data

    def _write_pixels(self, data):
        """
        Utility function for the different display functions
        :param data: list of 5 numbers in the range 0 to 255
        (e.g. [0xff, 0x00, 0, 255, 0b10101]
        """

        self._led_state.value = data

    def clear_display(self):
        """
        Clear the LED display on the microbit
        """
        self._write_pixels([0x00, 0x00, 0x00, 0x00, 0x00])

    @property
    def pixels(self):
        """
        Returns a list of 5 binary numbers. Each number represents a row
        from top to bottom
        :return: Example [0b01110, 0b01000, 0b10000, 0b10000, 0b01110]
        """
        rows = self._led_state.value
        return [int(i) for i in rows]

    @pixels.setter
    def pixels(self, rows):
        """
        For each row of LEDs specify which LEDs will be on.
        :example:
        0b11111 will turn all LEDs in specified row on
        0b10101 will turn alternate LEDs on
        0b00000 will turn all LEDs in row off
        :param row0: top row
        :param row1:
        :param row2: middle row
        :param row3:
        :param row4: bottom row
        """
        self._write_pixels([rows[0], rows[1], rows[2], rows[3], rows[4]])

    @property
    def temperature(self):
        """
        Temperature from sensors in micro:bit processors
        :return: Integer of temperature in Celsius
        """
        tmp_val = self._temp_data.value

        return int.from_bytes(tmp_val, byteorder='little', signed=True)

    @property
    def button_a(self):
        """
        Read the state of button A on a micro:bit
        3 button states are defined and represented by a simple numeric
        enumeration:  0 = not pressed, 1 = pressed, 2 = long press.
        :return: integer representing button value
        """
        btn_val = self._btn_a_state.value

        return int.from_bytes(btn_val, byteorder='little', signed=False)

    @property
    def button_b(self):
        """
        Read the state of button B on a micro:bit
        3 button states are defined and represented by a simple numeric
        enumeration:  0 = not pressed, 1 = pressed, 2 = long press.
        :return: integer representing button value
        """
        btn_val = self._btn_b_state.value

        return int.from_bytes(btn_val, byteorder='little', signed=False)

    def subscribe_button_a(self, user_callback):
        """
        Execute user_callback on Button A being press on micro:bit
        :param user_callback:
        :return:
        """
        self._btn_a_state.add_characteristic_cb(user_callback)
        self._btn_a_state.start_notify()

    def subscribe_button_b(self, user_callback):
        """
        Execute user_callback on Button B being press on micro:bit
        :param user_callback:
        :return:
        """
        self._btn_a_state.add_characteristic_cb(user_callback)
        self._btn_a_state.start_notify()

    @property
    def accelerometer(self):
        """
        Read the values of the accelerometer on the microbit
        :return: return a list in the order of x, y & z
        """
        # [16, 0, 64, 0, 32, 252]
        # x=0.16, y=0.024, z=-0.992
        accel_bytes = self._accel_data.value

        return tools.bytes_to_xyz(accel_bytes)

    @property
    def magnetometer(self):
        """
        Exposes magnetometer data.
        A magnetometer measures a magnetic field such
        as the earth's magnetic field in 3 axes.
        :return: List of x, y & z value
        """
        mag_bytes = self._magneto_data.value

        return tools.bytes_to_xyz(mag_bytes)

    @property
    def bearing(self):
        """
        Compass bearing in degrees from North.
        :return: degrees in integer
        """
        mag_bear_val = self._magneto_bearing.value

        return int.from_bytes(mag_bear_val,
                              byteorder='little', signed=False)

    @property
    def _pin_config(self):
        """
        A bit mask (32 bit) which defines which inputs will be read.
        A value of 0 means configured for output and 1 means configured
        for input.
        """
        return self._io_pin_config.value

    @_pin_config.setter
    def _pin_config(self, states):
        """
        A bit mask (32 bit) which defines which inputs will be read.
        A value of 0 means configured for output and 1 means configured
        for input.
        """
        self._io_pin_config.value = states

    @property
    def _pin_ad_config(self):
        """
        A bit mask (32 bit) which allows each pin to be configured for
        analogue or digital use.
        A value of 0 means digital and 1 means analogue.
        If no states are specified then the current state is returned
        """
        return self._io_ad_config.value

    @_pin_ad_config.setter
    def _pin_ad_config(self, states):
        """
        A bit mask (32 bit) which allows each pin to be configured for
        analogue or digital use.
        A value of 0 means digital and 1 means analogue.
        If no states are specified then the current state is returned
        """
        self._io_pin_config.value = states

    @property
    def _pin_states(self):
        """
        Contains data relating to zero or more pins.
        Structured as a variable length list of up to 19 Pin
        Number / Value pairs.
        """
        return self._io_pin_data.value

    @_pin_states.setter
    def _pin_states(self, pin_value_pairs):
        """
        Contains data relating to zero or more pins.
        Structured as a variable length list of up to 19 Pin
        Number / Value pairs.
        """
        self._io_pin_data.value = pin_value_pairs

    @property
    def _pin_pwm_control(self):
        """
        Write only method to set the PWM control data
        :param pin: pin number [range 0-19]
        :param value: Value is in the range 0 to 1024, per the current DAL API
            (e.g. setAnalogValue). 0 means OFF.
        :param period: Period is in microseconds and is an unsigned integer
        :return:
        """
        self._io_pin_pwm.value

    @_pin_pwm_control.setter
    def _pin_pwm_control(self, data):
        """
        Write only method to set the PWM control data
        :param pin: pin number [range 0-19]
        :param value: Value is in the range 0 to 1024, per the current DAL API
            (e.g. setAnalogValue). 0 means OFF.
        :param period: Period is in microseconds and is an unsigned integer
        :return:
        """
        pin = data[0]
        value = data[1]
        period = data[2]
        byte_value = tools.int_to_uint16(value)
        byte_period = tools.int_to_uint32(period)
        self._io_pin_pwm.value = [pin,
                                  byte_value[0],
                                  byte_value[1],
                                  byte_period[0],
                                  byte_period[1],
                                  byte_period[2],
                                  byte_period[3]
                                  ]


class MIpower(Microbit):
    def __init__(self, device_addr, adapter_addr=None):
        """
        Initialization of an instance of a remote bit:bot
        with a MI:power board attached
        :param device_addr: Connect to a BLE device with this address
        :param adapter_addr: Use the adapter with this address
        """
        Microbit.__init__(self, device_addr, adapter_addr)

    def beep(self, duration=1):
        """
        If a buzzer is attached to pin 0 then a beep will be played
        :param duration: time in seconds
        """
        self._pin_pwm_control = [0, 512, 2094]
        sleep(duration)
        self._pin_pwm_control = [0, 0, 0]


class BitBot:
    """
    Class to simplify interacting with a microbit attached to a bit:bot
    over Bluetooth Low Energy
    The bit:bot is a micro:bit robot available from 4tronix.co.uk
    """
    def __init__(self, device_addr, adapter_addr=None):
        """
        Initialization of an instance of a remote bit:bot
        :param name: Will look for a BLE device with this string in its name
        :param device_addr: Will look for a BLE device with this address
        """
        self._pins_configured = False
        self.ubit = Microbit(device_addr, adapter_addr)

    def __enter__(self):
        return self

    def __del__(self):
        self.clean_up()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.clean_up()

    def clean_up(self):
        if self.connected:
            self.stop()
            self.buzzer_off()

    def connect(self):
        """
        Connect to the bit:bot
        """
        self.ubit.connect()
        self._config_pins()

    def disconnect(self):
        """
        Disconnect from the bit:bot
        """
        self.clean_up()
        self.ubit.disconnect()

    @property
    def connected(self):
        """
        Returns true if bit:bot is connected
        """
        return self.ubit.connected

    def stop(self):
        """
        Stop both wheels of the bit:bot
        """
        self.ubit._pin_states = [0x01, 0x00,
                                 0x0C, 0x00,
                                 0x00, 0x00,
                                 0x08, 0x00]

    def spin_right(self):
        """
        Spin right wheel forward and left wheel backwards so bit:bot spins
        """
        self.ubit._pin_states = [0x01, 0x01,
                                 0x0C, 0x00,
                                 0x00, 0x00,
                                 0x08, 0x01]

    def spin_left(self):
        """
        Spin left wheel forward and right wheel backwards so bit:bot spins
        """
        self.ubit._pin_states = [0x01, 0x00,
                                 0x0C, 0x01,
                                 0x00, 0x01,
                                 0x08, 0x00]

    def forward(self):
        """
        Spin both wheels forward
        """
        self.ubit._pin_states = [0x01, 0x01,
                                 0x0C, 0x00,
                                 0x00, 0x01,
                                 0x08, 0x00]

    def reverse(self):
        """
        Spin both wheels backwards
        """
        self.ubit._pin_states = [0x01, 0x00,
                                 0x0C, 0x01,
                                 0x00, 0x00,
                                 0x08, 0x01]

    def _left_motor(self, pwm_value, reverse=False):
        if not reverse:
            self.ubit._pin_states = [0x08, 0x00]
        else:
            self.ubit._pin_states = [0x08, 0x01]
        self.ubit._pin_pwm_control = [0, pwm_value, 20000]

    def _right_motor(self, pwm_value, reverse=False):
        if not reverse:
            self.ubit._pin_states = [0x0C, 0x00]
        else:
            self.ubit._pin_states = [0x0C, 0x01]
        self.ubit._pin_pwm_control = [1, pwm_value, 20000]

    def _update_motors(self, left_val, right_val,
                       left_rev, right_rev,
                       pwm_period=20000):
        period = tools.int_to_uint32(pwm_period)
        left_pwm = tools.int_to_uint16(left_val)
        right_pwm = tools.int_to_uint16(right_val)
        self.ubit._io_pin_pwm.value = [0,
                                       left_pwm[0],
                                       left_pwm[1],
                                       period[0],
                                       period[1],
                                       period[2],
                                       period[3],
                                       1,
                                       right_pwm[0],
                                       right_pwm[1],
                                       period[0],
                                       period[1],
                                       period[2],
                                       period[3]
                                       ]
        self.ubit._pin_states = [0x08, left_rev, 0x0C, right_rev]

    def drive(self, left=100, right=100):
        """
        Set the drive power of both wheels at same time
        :param left: percentage of power (negative numbers are reverse)
        :param right: percentage of power (negative numbers are reverse)
        """
        left_direction = 0
        left_motor = self._percentage_to_pwm(left)

        right_direction = 0
        right_motor = self._percentage_to_pwm(right)

        if left < 0:
            left_direction = 1

        if right < 0:
            right_direction = 1

        self._update_motors(left_motor, right_motor,
                            left_direction, right_direction)

    def _percentage_to_pwm(self, percent):
        if percent < 0:
            percent += 100
        return int(10.23 * percent)

    def buzzer_on(self):
        """
        Play the buzzer
        """
        self.ubit._pin_states = [0x0E, 0x01]

    def buzzer_off(self):
        """
        Stop the buzzer
        """
        self.ubit._pin_states = [0x0E, 0x00]

    @property
    def left_line_senor(self):
        """
        Value ofthe left line sensor
        :return: False = No line  True = Line
        """
        return bool(self._get_pin_value(11))

    @property
    def right_line_sensor(self):
        """
        Value of the right line sensor
        :return: False = No line  True = Line
        """
        return bool(self._get_pin_value(5))

    @property
    def line_sensors(self):
        """
        Get the value of both line sensors
        :return: (left, right)
        """
        if not self._pins_configured:
            self._config_pins()
            self._pins_configured = True
        pins = self.ubit._pin_states
        return bool(pins[3]), bool(pins[5])

    @property
    def left_light_sensor(self):
        """
        Get the value of the left light sensor
        """
        self.ubit._pin_states = [0x10, 0x00]
        return int(self._get_pin_value(2))

    @property
    def right_light_sensor(self):
        """
        Get the value of the left light sensor
        """
        self.ubit._pin_states = [0x10, 0x01]
        return int(self._get_pin_value(2))

    def _config_pins(self):
        self.ubit._pin_config = [0x24, 0x08, 0x00, 0x00]
        self.ubit._pin_ad_config = [0x04, 0x00, 0x00, 0x00]

    def _build_pin_value_pairs(self, pin_states):
        val_dict = {}
        if len(pin_states) > 0:
            val_dict = dict(zip(pin_states[::2], pin_states[1::2]))
        return val_dict

    def _get_pin_value(self, pin):
        if not self._pins_configured:
            self._config_pins()
            self._pins_configured = True
        pin_value_pairs = self._build_pin_value_pairs(self.ubit._pin_states)
        if pin in pin_value_pairs.keys():
            return pin_value_pairs[pin]
        else:
            return None