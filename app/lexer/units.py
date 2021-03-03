from enum import Enum, IntFlag, auto
from typing import List

class UnitFlag(IntFlag):
    # System
    Basic = 0 # Nothing special about this unit
    Default = auto() # Used when no metric unit exists in given category
    Metric = auto()
    Imperial = auto()
    # Type
    Distance = auto()
    Mass = auto()
    Temperature = auto()
    Information = auto()
    Time = auto()
    # Combined
    System = Basic | Default | Metric | Imperial
    

class UnitType(Enum):
    # ([NAMES], FLAGS, (MULT, ADD))

    # Distance
    Meter   = (['m', 'meter'], UnitFlag.Metric | UnitFlag.Distance)
    # Mass
    Gram    = (['g', 'gram'], UnitFlag.Mass | UnitFlag.Metric)
    Tonne    = (['T', 'tonne'], UnitFlag.Mass, (10**6, 0.0))
    # Temperature
    Celsius = (['C', 'celsius'], UnitFlag.Temperature | UnitFlag.Default)
    Fahrenheit = (['F', 'fahrenheit'], UnitFlag.Temperature, (5/9, -32))
    Kelvin  = (['K', 'kelvin'], UnitFlag.Temperature, (1.0, -273.15))
    # Information
    Byte    = (['B', 'byte'], UnitFlag.Information | UnitFlag.Default)
    Bit     = (['b', 'bit'], UnitFlag.Information, (1/8, 0.0))
    Hertz   = (['Hz', 'hertz'], UnitFlag.Basic)
    # Time
    Second  = (['s', 'second'], UnitFlag.Time | UnitFlag.Metric)
    Minute = (['min', 'minute'], UnitFlag.Time, (60.0, 0.0))
    Hour = (['h', 'hour'], UnitFlag.Time, (3600.0, 0.0))
    Day = (['d', 'day'], UnitFlag.Time, (3600*24, 0.0))
    Month = (['M', 'month'], UnitFlag.Time, (3600*730, 0.0))
    Year = (['y', 'year'], UnitFlag.Time, (3600*730*12, 0.0))
    # Electric
    Ampere  = (['A', 'ampere'], UnitFlag.Metric)
    Volt  = (['V', 'volt'], UnitFlag.Basic)
    Watt = (['W', 'watt'], UnitFlag.Basic)
    Ohm = (['Ohm', 'ohm'], UnitFlag.Basic)
    # Other
    Candela = (['ca', 'candela'], UnitFlag.Metric)

    def __repr__(self):  return self.names()[1]
    def names(self): return self.value[0]
    def flags(self): return self.value[1]
    def conv(self): return self.value[2] if len(self.value) > 2 else (1.0, 0.0)

    def isDefault(self) -> bool:
        f = self.flags()
        return UnitFlag.Metric in f or UnitFlag.Default in f

    def getDefault(self):
        category = self.flags()  & ~UnitFlag.System
        if category is UnitFlag.Basic:
            return self

        for ut in UnitType:
            if category in ut.flags() and (UnitFlag.Metric in ut.flags() or UnitFlag.Default in ut.flags()):
                return ut

    @staticmethod
    def fromText(text) -> List:
        values = []
        for unitObj in UnitType:
            for unitStr in unitObj.names():
                values.append((unitObj, unitStr))
        # Exact case
        results = []
        maxLen = 0
        for unitObj, unitStr in values:
            if text.endswith(unitStr):
                maxLen = max(maxLen, len(unitStr))
                results.append((unitObj, unitStr))
        # Ignore case
        text = text.lower()
        for unitObj, unitStr in values:
            if text.endswith(unitStr.lower()): 
                if len(unitStr)-1 > maxLen:
                    results.append((unitObj, unitStr))
        return results

class UnitPrefix(Enum):
    Atto = (['a', 'atto'],  10**-18)
    Femto = (['f', 'femto'], 10**-15)
    Pico = (['p', 'pico'], 10**-12)
    Nano = (['n', 'nano'], 10**-9)
    Micro = (['u', 'micro'], 10**-6)
    Mili = (['m', 'mili'],  10**-3)
    Centi = (['c', 'centi'], 10**-2)
    Deci = (['d', 'deci'], 10**-1)
    # Zero
    Deca = (['da', 'da'], 10**1)
    Hecto = (['h', 'hecto'],10**2)
    Kilo = (['k', 'kilo'], 10**3)
    Mega = (['M', 'mega'], 10**6)
    Giga = (['G', 'giga'], 10**9)
    Tera = (['T', 'tera'], 10**12)
    Peta = (['P', 'peta'], 10**15)
    Exa = (['E', 'exa'],  10**18)
    Zetta = (['Z', 'zetta'],10**21)

    def __repr__(self): return self.value[0][1]
    def names(self): return self.value[0]
    def mult(self): return self.value[1]

    def bigger(self):
        prefixes = sorted(UnitPrefix, key=lambda x: x.value[1])
        index = prefixes.index(self)
        if index+1 >= len(prefixes): return None 
        return prefixes[index+1]

    def smaller(self):
        prefixes = sorted(UnitPrefix, key=lambda x: x.value[1])
        index = prefixes.index(self)
        if index-1 < 0: return None 
        return prefixes[index-1]

    @staticmethod
    def fromText(text):
        values = []
        for prefixObj in UnitPrefix:
            for prefixStr in prefixObj.value[0]:
                values.append((prefixObj, prefixStr))
        # Exact case
        for prefixObj, prefixStr in values:
            if text.endswith(prefixStr): return (prefixObj, prefixStr)
        # Ignore case
        text = text.lower()
        for prefixObj, prefixStr in values:
            if text.endswith(prefixStr.lower()): return (prefixObj, prefixStr)
        return None

class Unit:
    def __init__(self, text:str, unitType:UnitType, prefix:UnitPrefix=None):
        self.type = unitType
        self.prefix = prefix
        self.text = text

    def __repr__(self):
        if self.prefix is None: return f'{repr(self.type)}'
        else: return f'{repr(self.prefix)}{repr(self.type)}'

    def short_name(self):
        pref = self.prefix.names()[0] if self.prefix else ''
        unit = self.type.names()[0]
        return f'{pref}{unit}'

    def long_name(self):
        pref = self.prefix.names()[1] if self.prefix else ''
        unit = self.type.names()[1]
        return f'{pref}{unit}'

    @staticmethod
    def fromText(text:str):
        # Find matching units
        units = UnitType.fromText(text)
        if len(units) == 0: return []

        # Iterate over units to find matching prefixes
        results = []
        for unitObj, unitStr in units:
            # Try matching prefix
            prefix = UnitPrefix.fromText(text[:-len(unitStr)])
            if prefix is not None:
                prefixObj = prefix[0]
                prefixStr = prefix[1]
                results.append(Unit(prefixStr+unitStr, unitObj, prefixObj))
            else:
                # Add version without prefix
                results.append(Unit(unitStr, unitObj, None))
        return results



