# ACS-ACR122U-Tool
Python tool for ACR122U NFC Reader/Writer

## Notice (2018-03-24)
There will be any update from me for a while because I don't have the hardware now. 
Pull requests are welcome.

## Enviroment
* pyscard 1.9.4
* python 2.7.10

## Command List (Help Page)
     $ python nfctool.py <command>

 Before executing command, make sure that a card is being tagged on the reader.

* help: Show this command list

* mute: Disable beep sound when card is tagged. (This setting is volatile. Lasts till device off.)

* unmute: Enable beep sound when card is tagged.

* getuid: Print UID of the tagged card.

* info: Print card type and available protocols.

* loadkey \<key\>: Load key \<key\> (6byte hexstring) for auth. (The loaded key is volatile. Lasts till device off.)

* read \<sector\>: Read sector \<sector\> with loaded key.

* firmver: Print the firmware version of the reader.

## How to read data
* Connect the reader to computer and put a card on the reader. Check connection with 'getuid' or 'info' command.

* Load key with 'loadkey' command (This procedure is not needed for MIFARE Ultralight)

          $ python nfctool.py loadkey FFFFFFFFFFFF

* Read sector with 'read' command

          $ python nfctool.py read 4

## TODO
* Make options for 'read' command

## Copyright
Copyright © 2016 Kim Dong Min.

The MIT License (MIT)
