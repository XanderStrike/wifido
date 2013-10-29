# Interface to iwlist command line tool
# Simply runs 'iwlist if scanning', gets the output and parses it int a dictionary
# @author Ovidiu Ciule, ovidiu.ciule@gmail.com

import os, logging

log = logging.getLogger("PyWiList.IWList")

class IWList():
    def __init__(self, interface):
        self.rawdata = ""
        self.data = None
        self.interface = interface
        self.refresh()

    def refresh(self):
        # Get raw data as a string
        self.rawdata = self.getRawData(self.interface)
        # Parse raw data into a dictionary
        if self.rawdata is not None and self.rawdata.strip() is not "":
            self.data = self.parseRawData(self.rawdata)

    def getRawData(self, interface):
        # Runs iwlist and gets WiFi data in a string
        # Developped, tested with Wireless Extension v29 English translation, Nov 2007
        cstring = "iwlist " + interface + " scanning"
        return os.popen(cstring).read()

    def parseRawData(self, rawdata):
        # Parses a string containing the data printed by iwlist
        # Pre-condition: rawdata is not empty
        rawdatas = rawdata.split("\n")
        # Strip blanks
        # Let's separate by cells
        cellDataL = []
        currentCell = None
        for s in rawdatas:
            # If new cell:
            if s.lstrip().startswith("Cell "):
                # log.debug("parseRawData: new cell")
                cellDataL.append([])
            if len(cellDataL)>0 and len(s)>0:
                cellDataL[len(cellDataL)-1].append(s)
        # Data is separated by cells, now we'll parse each cell's data
        parsedCellData = {}
        for s in cellDataL:
            if s is not None:
                (cellNumber, cellData) = self.parseCellData("\n".join(s))
                parsedCellData[cellNumber] = cellData
        log.debug("parseRawData: parsed "+str(len(cellDataL))+" cells")
        return parsedCellData
        # print self.data

    def printData(self):
        # Debugging print
        for s in self.data:
            print s, self.data[s]

    def parseCellData(self, rawCellData):
        # Parses a string containing raw cell data
        # @return a tuble containing the cell's number and a dictionary with the data
        splitRawData = rawCellData.split("\n")
        cellData = {}
        for s in splitRawData:
            if s.strip().startswith("Cell "):
               cellData["Number"] = self.getCellNumber(s)
               cellData["MAC"] = self.getCellMAC(s)
            if s.strip().startswith("ESSID:\""):
               cellData["ESSID"] = self.getCellESSID(s)
            if s.strip().startswith("Protocol:"):
               cellData["Protocol"] = self.getCellProtocol(s)
            if s.strip().startswith("Mode:"):
               cellData["Mode"] = self.getCellMode(s)
            if s.strip().startswith("Mode:"):
               cellData["Mode"] = self.getCellMode(s)
            if s.strip().startswith("Frequency:"):
               cellData["Frequency"] = self.getCellFrequency(s)
            if s.strip().startswith("Quality="):
                cellData["Quality"] = self.getCellQuality(s)
                cellData["Signal"] = self.getCellSignal(s)
                #cellData["Noise"] = self.getCellNoise(s)
            if s.strip().startswith("Encryption key:"):
               cellData["Encryption"] = self.getCellEncryption(s)
            # if s.strip().startswith("Bit Rates:"):
            #    cellData["Bit Rates"] = self.getCellBitRates(s, splitRawData)
            # TODO: parse encryption key details and Extra tags
            if s.strip().startswith("Extra:"):
                try:
                    extra = cellData["Extra"]
                except KeyError:
                    extra = []
                extra.append(self.getCellExtra(s))
                cellData["Extra"] = extra
        
        return cellData["Number"], cellData

    def getCellExtra(self, s):
        s = s.split(":")
        if len(s)>2:
            ret = ":".join(s[1:])
            return ret
        else:
            return s[1]
       
    # def getCellBitRates(self, s, rawdatas):
    #     # Pre-condition: s is in rawdatas, and bit rates are described in 3 lines
    #     ixBitRate = rawdatas.index(s)
    #     rawBitRate = rawdatas[ixBitRate].split(":")[1].strip() + "; " + rawdatas[ixBitRate+1].strip() + "; " + \
    #         rawdatas[ixBitRate+2].strip()
    #     return rawBitRate
    
    def getCellNumber(self, s):
        return s.strip().split(" ")[1]

    def getCellFrequency(self, s):
        s = s.split(":")[1]
        return s.strip().split(" ")[0]

    def getCellChannel(self, s):
        return s.strip().split(" ")[3][0:-1]

    def getCellEncryption(self, s):
        return s.strip().split(":")[1]

    def getCellSignal(self, s):
        signal = s[s.index("l=") + 2:-1]
        return signal

    def getCellNoise(self, s):
        s = s.split("Noise level:")[1]
        return s.strip().split(" ")[0]

    def getCellQuality(self, s):
        quality = s[s.index("y=") + 2:s.index("/100") + 4]
        return quality

    def getCellMAC(self, s):
        return s.strip().split(" ")[4]

    def getCellESSID(self, s):
        return s.strip().split(":\"")[1][0:-1]

    def getCellProtocol(self, s):
        return s.strip().split(":")[1][-1]

    def getCellMode(self, s):
        return s.strip().split(":")[1]

    def getData(self): 
        return self.data
