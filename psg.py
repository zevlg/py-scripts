#!/usr/bin/env python

# send gcode to 3d printer
import sys, os
import getopt
import serial

def usage():
    print("usage: %s [-bhv] [-p USBPORT] [-s SPEED] [-c HEIGHT] GCODEFILE")
    print("  -p USBPORT       Serial port to send (default=/dev/ttyUSB0)")
    print("  -c HEIGHT        Continue from HEIGHT")
    print("  -s SPEED         Serial port speed (default=115200)")

    sys.exit(0)

NEED_WAIT_PREFIXES = [
    "start",
    "TargetBed",
    "TargetExtr",
    ]

def prnt_wait(prnt):
    while 1:
        msg = prnt.readline()
        if msg.strip() == "wait":
            return
        yield msg

def main(opts, gcodefn):
    sport = opts.get('-p', '/dev/ttyUSB0')
    speed = int(opts.get('-s', '115200'))
    heigt = opts.get('-c')

    prnt = serial.Serial(sport, speed)
    prnt.rts = True
    prnt.dtr = True
    prnt.reset_input_buffer()
    prnt.reset_output_buffer()

    print "+ Connected"

    fsize = os.stat(gcodefn).st_size
    rdsize = 0
    glines = open(gcodefn).xreadlines()
    for gl in glines:
	rdsize += len(gl)
        gls = gl.strip().split(';')[0].strip()
        if not gls:
            # skip comments
            continue
        cmdst = prnt.readline().strip()
        if any(map(cmdst.startswith, NEED_WAIT_PREFIXES)):
            print "+ Waiting .. "
            print "<----", cmdst
            while 1:
                msg = prnt.readline().strip()
                if msg == "wait":
                    # resume
                    break
                print msg

        prnt.write(gls + '\n')
        print "%s <--- %s  || %.1f%%" %(gls, cmdst, 100.0*rdsize/fsize)

    prnt.close()

if __name__ == "__main__":
   try:
      opts, args = getopt.getopt(sys.argv[1:], "bhvp:c:")
   except getopt.GetoptError, err:
      print str(err)
      usage()

   if len(args) != 1:
       usage()

   dopts = dict(opts)
   if '-h' in opts:
       usage()

   main(dopts, args[0])
