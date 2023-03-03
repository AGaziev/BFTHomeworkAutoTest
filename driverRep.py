import os
import fnmatch

class DriverPath:
    @staticmethod
    def getDriverPath():
        drivers = [driver for driver in DriverPath.getDriversInDir()]
        print("Select Driver")
        for i,driver in enumerate(drivers):
            print(f'[{i+1}]: {driver}')
        i = int(input('Write an opt:\t'))
        return fr'drivers\{drivers[i-1]}'

    @staticmethod
    def getDriversInDir():
        for file in os.listdir('drivers'):
            if fnmatch.fnmatch(file, '*driver.exe'):
                yield file

print(DriverPath.getDriverPath())