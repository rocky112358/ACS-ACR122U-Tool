'''
Python3 ACS-ACR122U-Tool
'''
from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.ATR import ATR
from smartcard.CardType import AnyCardType
import sys

if len(sys.argv) < 2:
	print("usage: nfcTool.py <command>\nList of available commands: help, mute, unmute, getuid, info, loadkey, read, firmver")
	sys.exit()

#detect command
cmd = sys.argv[1]

if cmd == "help":
	print("usage: python nfctool.py <command>\nList of available commands: help, mute, unmute, getuid") 
	print ("Before executing command, make sure that a card is being tagged on the reader.")
	print ("\thelp\tShow this help page")
	print ("\tmute\tDisable beep sound when card is tagged.")
	print ("\tunmute\tEnable beep sound when card is tagged.")
	print ("\tgetuid\tPrint UID of the tagged card.")
	print ("\tinfo\tPrint card type and available protocols.")
	print ("\tloadkey <key>\tLoad key <key> (6byte hexstring) for auth.")
	print ("\tread <sector>\tRead sector <sector> with loaded key.")
	#print ("\tread [-s <sector>] [-h | -a] [-d | -t] \tRead sector <sector> (or all sectors) with loaded key. Print as [hex | ascii]. Print [data only | trailer only]")
	print ("\tfirmver\tPrint the firmware version of the reader.")
	sys.exit()

r = readers()
if len(r) < 1:
	print("error: No readers available!")
	sys.exit()

print("Available readers: ", r)

reader = r[0]
print ("Using: ", reader)

connection = reader.createConnection()
connection.connect()

cmdMap = {
	"mute":[0xFF, 0x00, 0x52, 0x00, 0x00],
	"unmute":[0xFF, 0x00, 0x52, 0xFF, 0x00],
	"getuid":[0xFF, 0xCA, 0x00, 0x00, 0x00],
	"firmver":[0xFF, 0x00, 0x48, 0x00, 0x00],
}

COMMAND = cmdMap.get(cmd, cmd)

#send command
if type(COMMAND) == list:
	data, sw1, sw2 = connection.transmit(COMMAND)
	if cmd == "firmver":
		print (cmd +": "+ ''.join(chr(i) for i in data)+chr(sw1)+chr(sw2))
	else:
		print(cmd + ": " + toHexString(data))
		print ("Status words: %02X %02X" % (sw1, sw2))
	if (sw1, sw2) == (0x90, 0x0):
		print ("Status: The operation completed successfully.")
	elif (sw1, sw2) == (0x63, 0x0):
		print ("Status: The operation failed.")

elif type(COMMAND) == str:
	if COMMAND == "info":
		print ("###Tag Info###")
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
		print ("Card Name: "+ name)
		print ("T0 supported: ", atr.isT0Supported())
		print ("T1 supported: ", atr.isT1Supported())
		print ("T15 suppoerted: ", atr.isT15Supported())

	elif COMMAND == "loadkey":
		if (len(sys.argv) < 3):
			print ("usage: python nfctool.py loadkey <key>")
			print ("ex) python nfctool.py loadkey FFFFFFFFFFFF")
			sys.exit()

		COMMAND = [0xFF, 0x82, 0x00, 0x00, 0x06]
		key = [sys.argv[2][0:2], sys.argv[2][2:4], sys.argv[2][4:6], sys.argv[2][6:8], sys.argv[2][8:10], sys.argv[2][10:12]]
		for i in range(6):
			key[i] = int(key[i], 16)
		COMMAND.extend(key)

		data, sw1, sw2 = connection.transmit(COMMAND)
		print ("Status words: %02X %02X" % (sw1, sw2))
		if (sw1, sw2) == (0x90, 0x0):
			print ("Status: Key is loaded successfully to key #0."	)
		elif (sw1, sw2) == (0x63, 0x0):
			print ("Status: Failed to load key.")

	elif COMMAND == "read":
	# decrypt first block of sector with key. if succeed, sector is unlocked
	# if other sector is unlocked, previous sector is locked
		COMMAND = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, int(sys.argv[2])*4, 0x60, 0x00]
		data, sw1, sw2 = connection.transmit(COMMAND)
		if (sw1, sw2) == (0x90, 0x0):
			print ("Status: Decryption sector "+ sys.argv[2] +" using key #0 as Key A successful.")
		elif (sw1, sw2) == (0x63, 0x0):
			print ("Status: Decryption sector "+ sys.argv[2] +" failed. Trying as Key B")
			COMMAND = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, int(sys.argv[2])*4, 0x61, 0x00]
			data, sw1, sw2 = connection.transmit(COMMAND)
			if (sw1, sw2) == (0x90, 0x0):
				print ("Status: Decryption sector "+ sys.argv[2] +" using key #0 as Key B successful.")
			elif (sw1, sw2) == (0x63, 0x0):
				print ("Status: Decryption sector "+ sys.argv[2] +" failed.")
				sys.exit()
		# TODO -h -a for hex/ascii, -d -t for data/trailer, none for all, -s <sector> for certain sector	
		print ("---------------------------------Sector "+ sys.argv[2] +"---------------------------------")
		for block in range(int(sys.argv[2])*4, int(sys.argv[2])*4+4):
			COMMAND = [0xFF, 0xB0, 0x00]
			COMMAND.append(block)
			COMMAND.append(16)
			data, sw1, sw2 = connection.transmit(COMMAND)
			print ("block "+ str(block) +":\t"+ toHexString(data) +" | "+''.join(chr(i) for i in data))
		print ("Status words: %02X %02X" % (sw1, sw2))
		if (sw1, sw2) == (0x90, 0x0):
			print ("Status: The operation completed successfully.")
		elif (sw1, sw2) == (0x63, 0x0):
			print ("Status: The operation failed. Maybe auth is needed.")

	else:
		print ("error: Undefined command: "+ cmd +"\nUse \"help\" command for command list.")
		sys.exit()	
