#!/usr/bin/python3

import argparse  # for getting those command line arguments
import os  # for os path stuff
import sys  # for stopping gracefully
import time  # cos time is all we got
import progressbar  # for nice and shiny progress bar
from termcolor import colored  # for colors and stuff
import traceback  # for when it shits its pants and doesn't stop gracefully

petite = """                                     
                ,--.  ,--.  ,--.          
 ,---.  ,---. ,-'  '-.`--',-'  '-. ,---.  
| .-. || .-. :'-.  .-',--.'-.  .-'| .-. : 
| '-' '\   --.  |  |  |  |  |  |  \   --. 
|  |-'  `----'  `--'  `--'  `--'   `----' 
`--'                                      

"""

poison = """                                     
              ,--.                       
 ,---.  ,---. `--' ,---.  ,---. ,--,--,  
| .-. || .-. |,--.(  .-' | .-. ||      \ 
| '-' '' '-' '|  |.-'  `)' '-' '|  ||  | 
|  |-'  `---' `--'`----'  `---' `--''--' 
`--'                                     

"""

print(colored(petite, "green", attrs=['bold']))
print(colored(poison, "green", attrs=['bold']))

print(colored("A tool to match 'user:hash' files to 'hash:pass' files, PetitePoison 1.0.0", "yellow", attrs=['bold']))
print("Press Ctrl+C if you suddenly changed your mind\n")

print("Brought to you by Dmitry Kireev (@InfiniteSuns)\n")

argparser = argparse.ArgumentParser()
argparser.add_argument('-uh', '--userhash', help="i.e. /root/userhash.txt", required=True)
argparser.add_argument('-hp', '--hashpass', help="i.e. /root/hashpass.txt", required=True)
argparser.add_argument('-up', '--userpass', help="i.e. /root/userpass.txt", required=False)
args = argparser.parse_args()

nostats = False
nosemicolons = True
userhash = ""
hashpass = ""
userpass = ""

timestampstart = 0
timestampstop = 0

if args.userhash:
    print("[i] Userhash path received as argument")
    if os.path.exists(args.userhash):
        print("[+] Userhash path seems legit\n")
        userhash = open(args.userhash, 'r')
    else:
        print("[-] Userhash path seems not legit\n")
        sys.exit()

if args.hashpass:
    print("[i] Hashpass path received as argument")
    if os.path.exists(args.hashpass):
        print("[+] Hashpass path seems legit\n")
        hashpass = open(args.hashpass, 'r')
    else:
        print("[-] Hashpass path seems not legit\n")
        sys.exit()

if args.userpass:
    print("[i] Userpass path received as argument")
    # if os.path.exists(args.userpass):
    if os.access(args.userpass, os.R_OK):
        print(colored("[!] Userpass file seem to already exist, sure you want to append to it?",
                      "red", attrs=['bold']))
        yes = {'yes', 'ye', 'y', ''}
        no = {'no', 'n'}
        answer = input("[?] Default is to append (y/n): ").lower()
        if answer in yes:
            if os.access(args.userpass, os.W_OK):
                print("[+] Userpass file present and can be written\n")
                nostats = True
            else:
                print("[-] Userpass file seems not writable\n")
                sys.exit()
        elif answer in no:
            print("[+] Well then, going to write to our own userpass file\n")
            args.userpass = "userpass" + str(int(time.time())) + ".txt"
        else:
            print("[-] That was as simple as yes or no, now you ruined it\n")
            sys.exit()
else:
    args.userpass = "userpass" + str(int(time.time())) + ".txt"

print(colored("\n[!] Do your hashes contain semicolons (e.g. NetNTLMv2)?",
              "green", attrs=['bold']))
yes = {'yes', 'ye', 'y'}
no = {'no', 'n', ''}
answer = input("[?] Default is no (y/n): ").lower()
if answer in no:
    print("[+] Fine then, it is going to be faster\n")
elif answer in yes:
    print("[-] Okay, but it is going to take more time\n")
    nosemicolons = False
else:
    print("[-] That was as simple as yes or no, now you ruined it\n")
    sys.exit()

currentuser = ""
currenthash = ""
currentpass = ""

totaluserhashcount = 0
totalhashpasscount = 0
totaluserpasscount = 0
currentuserhashcount = 0

userhashlines = userhash.readlines()
userhash.close()
hashpasslines = hashpass.readlines()
hashpass.close()

for userhashline in userhashlines:
    totaluserhashcount += 1

for hashpassline in hashpasslines:
    totalhashpasscount += 1

print ("[i] Got " + str(totaluserhashcount) + " 'user:hash' lines")
print ("[i] Got " + str(totalhashpasscount) + " 'hash:pass' lines")

print ("\n[i] Now, going to replace hashes with passwords\n[i] Do not look away from progress bar\n")

bar = progressbar.ProgressBar(maxval=totaluserhashcount,
                              widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()

timestampstart = int(time.time())
try:
    for userhashline in userhashlines:
        currentuserhashcount += 1
        bar.update(currentuserhashcount)

        currentpass = ""
        currentuser = userhashline.rstrip().split(":")[0]
        currenthash = userhashline.rstrip().split(":")[1]
        for hashpassline in hashpasslines:
            if nosemicolons:
                potfilehash = hashpassline.rstrip().split(":")[0]
                potfilepass = hashpassline.rstrip().split(":")[1]
            else:
                potfilepass = hashpassline.rstrip()[::-1].split(":")[0][
                              ::-1]  # reverse the line in case hashes with semicolons
                potfilehash = hashpassline.rstrip()[::-1].split(":")[1][
                              ::-1]  # reverse the line in case hashes with semicolons
            if potfilehash == currenthash:
                currentpass = potfilepass
        if currentpass != "":
            userpass = open(args.userpass, 'a')
            userpass.write(currentuser + ":" + currentpass + "\n")
            userpass.close()
    bar.finish()

    userpass = open(args.userpass, 'r')
    userpasslines = userpass.readlines()
    for userpassline in userpasslines:
        totaluserpasscount += 1

    timestampstop = int(time.time())
    print("\n[i] Done in " + str(timestampstop - timestampstart) + " seconds")
    if not nostats:
        print ("\n[i] Now you have " + str(totaluserpasscount) + " 'user:pass' lines")
        print ("[i] It is approximately " + str(int(100 * totaluserpasscount / totaluserhashcount)) + "%")

except KeyboardInterrupt:
    print(colored("[!] Ctrl+C caught, stopping gracefully", "red"))
except Exception:
    traceback.print_exc(file=sys.stdout)
    sys.exit()
