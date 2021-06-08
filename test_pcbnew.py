#!/Applications/KiCad/pcbnew.app/Contents/Frameworks/Python.framework/Versions/2.7/bin/python

import sys

sys.path.append(
    "/Applications/KiCad/pcbnew.app/Contents/Frameworks/python/site-packages"
)

from pcbnew import *

ToUnits = ToMM
FromUnits = FromMM



def print_tracks(pcb):
    for item in pcb.GetTracks():
        if type(item) is VIA:

            pos = item.GetPosition()
            drill = item.GetDrillValue()
            width = item.GetWidth()
            print " * Via:   %s - %f/%f "%(ToUnits(pos),ToUnits(drill),ToUnits(width))

        elif type(item) is TRACK:

            start = item.GetStart()
            end = item.GetEnd()
            width = item.GetWidth()

            print " * Track: %s to %s, width %f" % (ToUnits(start),ToUnits(end),ToUnits(width))

        else:
            print "Unknown type    %s" % type(item)

def print_modules(pcb):
    for module in pcb.GetModules():
        print "* Module: %s at %s"%(module.GetReference(),ToUnits(module.GetPosition()))
        # for each module, print the shapes
        pads = module.Pads()
        print pads.GetNetname()
        # for pad in module.Pads():
        #     print "  PAD ", pad.GetPadName(), ToMM(pad.GetLocalSolderPasteMargin())
        #     print pad.GetClass()
        # print(dir(module))
def print_nets(pcb):
    print pcb.GetNetInfo()
    # for net in pcb.GetNetInfo():
    #     print(net)
    #     print(net.GetClassName())
    #     print(net.GetNet())
    #     print(net.GetNetname())
    #     print(net.GetShortNetname())
    print pcb.GetNetsByName()
    print pcb.GetNetClasses()
    nets = pcb.GetNetsByName()
    for key in nets:
        print key, nets[key].GetNetname(), nets[key].GetClassName()
    codes = pcb.GetNetsByNetcode()
    for key in codes:
        print key, codes[key]
    # print ""
    # print "Ratsnest cnt:",len(pcb.GetFullRatsnest())
    # print "track w cnt:",len(pcb.GetTrackWidthList())
    # print "via s cnt:",len(pcb.GetViasDimensionsList())


pcb = LoadBoard("/Users/hebi/Documents/GitHub/bhdl/python/benchmarks/cantact-hw/cantact.kicad_pcb")

# 1. get all the modules, and their shapes and pads
# print_modules(pcb)
# 2. get all the nets for the pads
print_nets(pcb)
# 3. visualize?


conn = pcb.GetConnectivity()
items = pcb.AllConnectedItems()
print items
print dir(items)
print items.next()
print items.__sizeof__()
print dir(conn)
print(VIA)
print(SYMBOL_LIB_TABLE_T)
theitem = conn.GetNetItems(1, PCB_PAD_T)
print dir(theitem)
print theitem


# print dir(conn)
# print conn.GetConnectedItems(items)