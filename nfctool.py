from smartcard.System import readers
from smartcard.util import toHexString
import sys

if len(sys.argv) < 2:
	print "usage: nfcTool.py <command>\nList of available commands: help, mute, unmute, getuid"
	sys.exit()

cmd = sys.argv[1]

if cmd == "help":
	print "usage: python nfctool.py <command>\nList of available commands: help, mute, unmute, getuid"
	print "Before executing command, make sure that a card is being tagged on the reader."
	print "\thelp\tShow this help page"
	print "\tmute\tDisable beep sound when card is tagged."
	print "\tunmute\tEnable beep sound when card is tagged."
	print "\tgetuid\tPrint UID of the tagged card."
	sys.exit()

cmdMap = {
	"mute":[0xFF, 0x00, 0x52, 0x00, 0x00],
	"unmute":[0xFF, 0x00, 0x52, 0xFF, 0x00],
	"getuid":[0xFF, 0xCA, 0x00, 0x00, 0x00]
}

COMMAND = cmdMap.get(cmd, "unknown")

if COMMAND == "unknown":
	print "error: Undefined command: "+ cmd +"\nUse \"help\" command for command list."
	sys.exit()

r = readers()
if len(r) < 1:
	print "error: No readers available!"
	sys.exit()

print "Available readers: ", r

reader = r[0]
print "Using: ", reader

connection = reader.createConnection()
connection.connect()

data, sw1, sw2 = connection.transmit(COMMAND)
print cmd + ": " + toHexString(data)
print "Response: %02X %02X" % (sw1, sw2)
if (sw1, sw2) == (0x90, 0x0):
	print "Response: The operation completed successfully."
