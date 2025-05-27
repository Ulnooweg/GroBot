import time
import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
import asyncio
import busio
import adafruit_ina219

########################################################################################
# setup
########################################################################################

# Settings
pumpTime = 10
settleTime = 1
sampleRate = 50
filterWindowSize = 10
filterStartVal = 0
P_dry = (0.5, 4)
t_rampUp = 2.0

# constants
adc2volts = 3.30 / 65536

# calculated parameters
sampleTime = 1/sampleRate

# filter
class MovingMax:
    def __init__(self, window_size=20, startVal=0):
        """
        implements a moving-window maximum filter to detect peak current draw in a very noisy signal
        """
        self.window_size = window_size
        self.ring = [startVal] * window_size
        self.index = 0

    def update(self, newVal):
        self.ring[self.index] = newVal
        self.index += 1
        if self.index >= self.window_size:
            self.index = 0
        return max(self.ring)

powerFilter = MovingMax(filterWindowSize)

########################################################################################
# Hardware Setup
########################################################################################

# Analog Sensor Setup
A0 = AnalogIn(board.A0)

# ina219 setup
i2c = busio.I2C(board.SCL, board.SDA)
ina = adafruit_ina219.INA219(i2c)
if True:
    print("int219 config:")
    # print("  bus_voltage_range:    0x%1X" % ina.bus_voltage_range)
    print("  bus_voltage_range:     " + str(ina.bus_voltage_range))
    print("  gain:                  " + str(ina.gain))
    print("  bus_adc_resolution:    " + str(ina.bus_adc_resolution))
    print("  shunt_adc_resolution:  " + str(ina.shunt_adc_resolution))
    print("  mode:                  " + str(ina.mode))
    print("")

# Pump Setup
LeftPump            = DigitalInOut(board.MISO)
LeftPump.direction  = Direction.OUTPUT
LeftPump.value      = False

RightPump           = DigitalInOut(board.MOSI)
RightPump.direction = Direction.OUTPUT
RightPump.value     = False

# LED setup
led             = DigitalInOut(board.LED)
led.direction   = Direction.OUTPUT

########################################################################################
# async functions
########################################################################################

async def pumpCycle(pt,st,plotting):
    plotting.set()
    powerFilter.maximum = 0

    RightPump.value = True
    print('right pump on')
    await asyncio.sleep(pt)
    RightPump.value = False
    print('right pump off')
    await asyncio.sleep(st)
    plotting.clear()

    LeftPump.value = True
    print('left pump on')
    await asyncio.sleep(5)
    LeftPump.value = False
    print('left pump off')
    await asyncio.sleep(st)


async def sensorReadPlot(plotting,t_start):
    while True:
        if plotting.is_set():
            P_filtered = round(powerFilter.update(ina.power),2)
            t_elapsed = time.monotonic() - t_start
            if(
                RightPump.value and \
                P_filtered > P_dry[0] and \
                P_filtered < P_dry[1] and \
                t_elapsed >= t_rampUp
                ):
                led.value = True
            else:
                led.value = False
            print( (
                t_elapsed,
                P_filtered,
                led.value*1,
                ) )

        else:
            pass
        await asyncio.sleep(sampleTime)

########################################################################################
# async main
########################################################################################

# main function
async def main():
    t_start = time.monotonic()
    plotting = asyncio.Event()
    pumpTask = asyncio.create_task(pumpCycle(pumpTime,settleTime,plotting))
    sensorReadTask = asyncio.create_task(sensorReadPlot(plotting,t_start))
    await asyncio.gather(pumpTask)

# execute Main()
while True:
    input('press enter to start')
    try:
        asyncio.run(main())
    except Exception as e:
        RightPump.value = False
        LeftPump.value = False
        led.value = False
        print(e)
    print('done')

