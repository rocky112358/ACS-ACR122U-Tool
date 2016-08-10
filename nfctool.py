from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.ATR import ATR
from smartcard.CardType import AnyCardType
import sys

if len(sys.argv) < 2:
	print "usage: nfcTool.py <command>\nList of available commands: help, mute, unmute, info, getuid"
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

#detect command
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

COMMAND = cmdMap.get(cmd, cmd)

#send Command
if type(COMMAND) == list:
	data, sw1, sw2 = connection.transmit(COMMAND)
	print cmd + ": " + toHexString(data)
	print "Response Code: %02X %02X" % (sw1, sw2)
	if (sw1, sw2) == (0x90, 0x0):
		print "Response Code: The operation completed successfully."

elif type(COMMAND) == str:
	if COMMAND == "info":
		print "###Tag Info###"
		atr = ATR(connection.getATR())
		hb = toHexString(atr.getHistoricalBytes())
		cardname = hb[-17:-12]
		cardnameMap = {
			"00 01": "MIFARE Classic 1K",
			"00 02": "MIFARE Classic 4K",
			"00 03": "MIFARE Ultralight",
			"00 26": "MIFARE Mini",
			"F0 04": "Topaz and Jewel",
			"F0 11": "FeliCa 212K",
			"F0 11": "FeliCa 424K"
		}
		name = cardnameMap.get(cardname, "unknown")
		print "Card Name: "+ name
		print "T0 supported: ", atr.isT0Supported()
		print "T1 supported: ", atr.isT1Supported()
		print "T15 suppoerted: ", atr.isT15Supported()

	else:
		print "error: Undefined command: "+ cmd +"\nUse \"help\" command for command list."
		sys.exit()	
