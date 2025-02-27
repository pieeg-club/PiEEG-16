
# imports
import spidev
from RPi import GPIO
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
import gpiod


def get_voltage(output, a, data_check=0xFFFFFF, data_test=0x7FFFFF):
    voltage=(output[a]<<8) | output[a+1]
    voltage=(voltage<<8) | output[a+2]
    convert_voltage = voltage | data_test
    if convert_voltage==data_check:
        voltage = (voltage - 16777214)
    voltage = round(1000000*4.5*(voltage/16777215),2)

    return voltage
    
    
def setup_pieeg16(gain=1):
    # Convert gain to bits
    gain = convert_gain(gain)

    # GPIO settings
    chip = gpiod.Chip("gpiochip4")

    cs_line = chip.get_line(19)  # GPIO19
    cs_line.request(consumer="SPI_CS", type=gpiod.LINE_REQ_DIR_OUT)
    cs_line.set_value(1)  # Set CS high initially

    # Initialize spidev
    spi_1 = spidev.SpiDev()
    spi_1.open(0,0)
    spi_1.max_speed_hz  = 4000000
    spi_1.lsbfirst=False
    spi_1.mode=0b01
    spi_1.bits_per_word = 8

    spi_2 = spidev.SpiDev()
    spi_2.open(0,1)
    spi_2.max_speed_hz=4000000
    spi_2.lsbfirst=False
    spi_2.mode=0b01
    spi_2.bits_per_word = 8

    # Register Commands
    who_i_am=0x00
    config1=0x01
    config2=0X02
    config3=0X03

    reset=0x06
    stop=0x0A
    start=0x08
    sdatac=0x11
    rdatac=0x10
    wakeup=0x02
    rdata = 0x12

    ch1set=0x05
    ch2set=0x06
    ch3set=0x07
    ch4set=0x08
    ch5set=0x09
    ch6set=0x0A
    ch7set=0x0B
    ch8set=0x0C

    # device initialization and configuration - first 8 channels
    send_command (spi_1, wakeup)
    send_command (spi_1, stop)
    send_command (spi_1, reset)
    send_command (spi_1, sdatac)

    write_byte (spi_1, 0x14, 0x80) #GPIO 80
    write_byte (spi_1, config1, 0x96)
    write_byte (spi_1, config2, 0xD4)
    write_byte (spi_1, config3, 0xFF)
    write_byte (spi_1, 0x04, 0x00)
    write_byte (spi_1, 0x0D, 0x00)
    write_byte (spi_1, 0x0E, 0x00)
    write_byte (spi_1, 0x0F, 0x00)
    write_byte (spi_1, 0x10, 0x00)
    write_byte (spi_1, 0x11, 0x00)
    write_byte (spi_1, 0x15, 0x20)

    write_byte (spi_1, 0x17, 0x00)
    write_byte (spi_1, ch1set, gain)
    write_byte (spi_1, ch2set, gain)
    write_byte (spi_1, ch3set, gain)
    write_byte (spi_1, ch4set, gain)
    write_byte (spi_1, ch5set, gain)
    write_byte (spi_1, ch6set, gain)
    write_byte (spi_1, ch7set, gain)
    write_byte (spi_1, ch8set, gain)

    send_command (spi_1, rdatac)
    send_command (spi_1, start)

    # device initialization and configuration - last 8 channels
    send_command_2 (spi_2, cs_line, wakeup)
    send_command_2 (spi_2, cs_line, stop)
    send_command_2 (spi_2, cs_line, reset)
    send_command_2 (spi_2, cs_line, sdatac)

    write_byte_2 (spi_2, cs_line, 0x14, 0x80) #GPIO 80
    write_byte_2 (spi_2, cs_line, config1, 0x96)
    write_byte_2 (spi_2, cs_line, config2, 0xD4)
    write_byte_2 (spi_2, cs_line, config3, 0xFF)
    write_byte_2 (spi_2, cs_line, 0x04, 0x00)
    write_byte_2 (spi_2, cs_line, 0x0D, 0x00)
    write_byte_2 (spi_2, cs_line, 0x0E, 0x00)
    write_byte_2 (spi_2, cs_line, 0x0F, 0x00)
    write_byte_2 (spi_2, cs_line, 0x10, 0x00)
    write_byte_2 (spi_2, cs_line, 0x11, 0x00)
    write_byte_2 (spi_2, cs_line, 0x15, 0x20)

    write_byte_2 (spi_2, cs_line, 0x17, 0x00)
    write_byte_2 (spi_2, cs_line, ch1set, gain)
    write_byte_2 (spi_2, cs_line, ch2set, gain)
    write_byte_2 (spi_2, cs_line, ch3set, gain)
    write_byte_2 (spi_2, cs_line, ch4set, gain)
    write_byte_2 (spi_2, cs_line, ch5set, gain)
    write_byte_2 (spi_2, cs_line, ch6set, gain)
    write_byte_2 (spi_2, cs_line, ch7set, gain)
    write_byte_2 (spi_2, cs_line, ch8set, gain)

    send_command_2 (spi_2, cs_line, rdatac)
    send_command_2 (spi_2, cs_line, start)

    return spi_1, spi_2, cs_line


# SPI Read/Write Functions
def read_byte(spi, register):
    write=0x20
    register_write=write|register
    data = [register_write,0x00,register]
    spi.xfer(data)


def send_command(spi, command):
    send_data = [command]
    spi.xfer(send_data)


def write_byte(spi, register,data):
    write=0x40
    register_write=write|register
    data = [register_write,0x00,data]
    spi.xfer(data)


def read_byte_2(spi_2, cs_line, register):
    write=0x20
    register_write=write|register
    data = [register_write,0x00,register]
    cs_line.set_value(0)
    spi_2.xfer(data)
    cs_line.set_value(1)


def send_command_2(spi_2, cs_line, command):
    send_data = [command]
    cs_line.set_value(0)
    spi_2.xfer(send_data)
    cs_line.set_value(1)


def write_byte_2(spi_2, cs_line, register, data):
    write=0x40
    register_write=write|register
    data = [register_write,0x00,data]
    cs_line.set_value(0)
    spi_2.xfer(data)
    cs_line.set_value(1)


def convert_gain(value):
# convert to bits
    if value == 1:
        return 0b000
    elif value == 2:
        return 0b001
    elif value == 4:
        return 0b010
    elif value == 6:
        return 0b011
    elif value == 8:
        return 0b100
    elif value == 12:
        return 0b101
    elif value == 24:
        return 0b110
    else:
        raise ValueError("Invalid gain value. Please use 1, 2, 4, 6, 8, 12, or 24.")
