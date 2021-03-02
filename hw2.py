#print("hello")


import psutil
import threading 
import os
import sys
import pprint
import subprocess

while 1 == 1:

    print("what would you like to do?")
    print("     1: Enumerate all running processes")
    #print("     2: List all the running threads within process boundary")
    print("     3: Stop")

    process = input(":: ")

    if process == "1":
        for proc in psutil.process_iter():
            try:
                processName = proc.name()
                processID = proc.pid
                print(processName, " :: ",processID)
            except (psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
                pass

        print("what process do you want to see threads of?")
        process = input("   :: ")
        if process == -1:
            break
        else:
            temp = "ps -T -p " + process
            os.system(temp)
        print("would you like to see the loaded moudles of this process? y/n")
        process2 = input("   :: ")
        if process2 == "y":
            temp2 = 'lsmod | grep " '+ process + ' "'
            os.system(temp2)
        else:
            pass

        print("would you like to see the executable pages of this file? y/n")
        process2 = input("  :: ")
        if process2 == 'y':
            temp3 = "pmap "+ process
            os.system(temp3)
        else:
            pass

        print("would you like to read the memory of this process? y/n")
        process2 = input("  :: ")
        if process2 == 'y':
            #p1 = subprocess.Popen(["ps", "-ux"], stdout=subprocess.PIPE)
            #p2 = subprocess.Popen(["grep", process], stdin=p1.stdout, stdout=subprocess.PIPE)
            #p1.stdout.close()
            #output = p2.communicate()[0]
            #print(output)
            temp4 = "gcore -a " + process 
            os.system(temp4)
            temp5 = "cat core."+process
            os.system(temp5)
            temp6 = "rm "+temp5
            os.system(temp6)
            break;
        else:
            pass
    #elif process == "2":
        #print("second")
        #print(threading.enumerate())
        #for some in threading.enumerate():
        #    print(some)
    elif process == "3":
        break
    else:
        print("non supported input")
