# ACS-ACR122U-Tool
Python tool for ACR122U NFC Reader/Writer

## Enviroment
* pyscard 1.9.4
* python 2.7.10

## Command List (Help Page)
* usage: python nfctool.py <command>

* List of available commands: help, mute, unmute, getuid

* Before executing command, make sure that a card is being tagged on the reader.

* help: Show this command list

* mute: Disable beep sound when card is tagged. (This setting is volatile. Lasts till device off.)

* unmute: Enable beep sound when card is tagged.

* getuid: Print UID of the tagged card.

* info: Print card type and available protocols.
