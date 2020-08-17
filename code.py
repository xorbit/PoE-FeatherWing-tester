import time
import board
import busio
import digitalio
import adafruit_requests as requests
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
import fixture

print("PoE-FeatherWing Tester")
time.sleep(1)

# Init fixture
led, voltage = fixture.init()
test_start_time = time.time()

# W5500 connections
cs = digitalio.DigitalInOut(board.D10)
spi_bus = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Read the MAC from the 24AA02E48 chip
default_mac = bytearray((0x98, 0x76, 0xB6, 0x11, 0x76, 0xA0))
mac = bytearray(6)
mac[:] = default_mac
try:
  i2c = busio.I2C(board.SCL, board.SDA)
  while not i2c.try_lock():
      pass
  i2c.writeto(0x50, bytearray((0xFA,)), stop=False)
  i2c.readfrom_into(0x50, mac, start=0, end=6)
  i2c.unlock()
except:
  pass
print ("MAC address: {}".format(':'.join(['%02x' % i for i in mac])))
# Indicate whether we successfully read a MAC
led.mac[mac != default_mac].value = True

# DHCP retries
dhcp_retries = 3
while dhcp_retries:
  try:
    # Initialize ethernet interface with DHCP and default MAC
    # If we used a unique MAC for each board we test, the DHCP server
    # would run out of IP addresses to lease
    eth = WIZNET5K(spi_bus, cs, mac=default_mac,
                    hostname="PoE-FeatherWing-Fixture1")
    print("Chip Version:", eth.chip)
    print("My IP address is:", eth.pretty_ip(eth.ip_address))
    
    # Indicate whether we successfully read the W5500 and got an IP
    led.ip[eth.chip == 'w5500'].value = True
    break
  except:
    dhcp_retries = dhcp_retries - 1

# Report if we didn't succeed in getting an IP from DHCP
if not dhcp_retries:
  led.ip[False].value = True

# Give power at least 5 seconds
while time.time() < test_start_time + 5:
  time.sleep(0.1)

# Print supply voltage for debugging
supply_v = voltage()
print ("Supply voltage: {}".format(supply_v))

# Indicate whether the ~2.6W loaded voltage didn't collapse
led.power[supply_v >= 4.2 and supply_v <= 5.6].value = True

print ("Done!")
while True:
  time.sleep(1)

