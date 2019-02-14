# PetitePoison #

A tool to match 'user:hash' files to 'hash:pass' files, creating a 'user:pass' file.

## What it's for ##

Imagine you have a long list of users and their hashes, and a hashcat potfile of craked hashes. Now you can create yourself a nice file consisting of only users with their cracked passwords.

## Usage ##

Note that this thing is extremely poorly written and slow AF. Not multithreading or all those other shiny things.

The scripts is expecting a 'user:hash' and 'hash:pass' as -uh and -hp arguments. Optionally you can set a name for a resulting 'user:pass' file as -up argument:
- ```-uh or --userhash is a path to 'user:hash' file (i.e. /root/userhash.txt)```
- ```-hp or --hashpass is a path to 'hash:pass' file (i.e. /root/hashpass.txt)```
- ```-up or --userpass is a path to 'user:pass' file (i.e. /root/userpass.txt)```
