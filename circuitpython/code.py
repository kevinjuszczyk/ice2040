#Copyright (C) 2022 Kevin Juszczyk
#Source location: https://github.com/kevinjuszczyk/ice2040
#
#This program is free software: you can redistribute it and/or modify it under
#the terms of the GNU General Public License as published by the Free Software
#Foundation, either version 3 of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful, but WITHOUT
#ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along with
#this program. If not, see <https://www.gnu.org/licenses/>.

import board
import busio
import digitalio
import io
import time
import supervisor
import pwmio

print("\n**********ICE2040**********")
print("Starting FPGA Configuration...")

creset = digitalio.DigitalInOut(board.GP0)
creset.direction = digitalio.Direction.OUTPUT
creset.value = False

cdone = digitalio.DigitalInOut(board.GP1)
cdone.direction = digitalio.Direction.INPUT
print("CDONE=" + str(cdone.value))

cs = digitalio.DigitalInOut(board.GP5)
cs.direction = digitalio.Direction.OUTPUT

print("Start with CRESET_B and SPI_SS held LOW, wait >200ns.")
cs.value = False
creset.value = False
time.sleep(0.001)

print("CRESET_B brought HIGH and SPI_SS held LOW, wait >1200us.")
creset.value = True
time.sleep(0.002)

#config SPI
spi = busio.SPI(clock=board.GP2, MISO=board.GP4, MOSI=board.GP3)

while not spi.try_lock():
    pass

spi.configure(baudrate=240000000, phase=0, polarity=0)

bitstream = open("top_bitmap.bin",mode='rb')
bitstreambuf = bitstream.read()

print("SPI_SS brought HIGH, cycle SPI_SCK 8 times.")
cs.value = True
spi.write(bytes(8))

print("SPI_SS brought LOW, reading bitstream file into ICE40 SPI_SI pin.")
cs.value = False
spi.write(bitstreambuf)

print("Finished bitstream file, SPI_SS brought HIGH.")
cs.value = True

print("Cycle SPI_SCK 100 times to read CDONE HIGH.")
spi.write(bytes(100))
gotcdone = cdone.value
print("CDONE=" + str(gotcdone))

if gotcdone:
    print("Cycle SPI_SCK 49 times to release FPGA IO for user application.")
    spi.write(bytes(49))
else:
    print("Error configuring FPGA!!")

#clean up GPIO and file
spi.unlock()
bitstream.close()
cs.deinit()
cdone.deinit()

if gotcdone:
    print("12MHz clock from RP2040 GP1 to ICE40 CDONE.")
    #RP2040 GP1/ICE40 CDONE were arbitrarily chosen.
    #RP2040 can output PWM on any pin, and ICE40 can take its clock on any pin.
    #The CDONE pin is connected to a global line meant for clock distribution
    #across the FPGA. This also demonstrates repurposing an FPGA configuration
    #pin after configuration is finished.
    pwm = pwmio.PWMOut(board.GP1, duty_cycle=2 ** 15, frequency=12000000, variable_frequency=False)

print("Type 'x' to terminate program and reset FPGA.")

while True:
    time.sleep(0.1)
    if supervisor.runtime.serial_bytes_available:
        value = input().strip()
        if value == "x":
            break
