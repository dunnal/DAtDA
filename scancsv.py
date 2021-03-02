from CSVPacket import Packet, CSVPackets
import sys

IPProtos = [0 for x in range(256)]
numBytes = 0
numPackets = 0

csvfile = open(sys.argv[1],'r')
scan = 0
countip = 0
connto = 0


if len(sys.argv) > 2:
    if sys.argv[2] == "-scan":
        scan = 1
    elif sys.argv[2] == "-countip":
        countip = 1
    elif sys.argv[2] == "-connto":
        connto = 1

if scan == 1:
    tcpli = [0 for x in range(1025)]
    udpli = [0 for x in range(1025)]

    for pkt in CSVPackets(csvfile):
        proto = pkt.proto & 0xff
        if proto == 6 and pkt.tcpdport < 1025:
            tcpli[pkt.tcpdport] += 1
        elif proto == 17 and pkt.udpdport < 1025:
            udpli[pkt.udpdport] += 1

    for x in range(len(tcpli)):
        if tcpli[x] > 0:
            print "TCP PORT %d : %d" % (x,tcpli[x])
    for x in range(len(udpli)):
        if udpli[x] > 0:
            print "UDP PORT %d : %d" % (x,udpli[x])
elif countip == 1:
    #print("count ip")
    iparr = []
    if len(sys.argv) > 3:
        if sys.argv[3] == "-GRE":
            print("GRE results")
            for pkt in CSVPackets(csvfile):
                if pkt.proto == 47:
                    iparr.append(pkt.ipsrc)
                    iparr.append(pkt.ipdst)
        elif sys.argv[3] == "-IPSEC":
            print("IPSEC results")
            for pkt in CSVPackets(csvfile):
                if pkt.proto == 50 or pkt.proto == 51:
                    iparr.append(pkt.ipsrc)
                    iparr.append(pkt.ipdst)
        elif sys.argv[3] == "-OSPF":
            print("OSPF results")
            for pkt in CSVPackets(csvfile):
                if pkt.proto == 89:
                    iparr.append(pkt.ipsrc)
                    iparr.append(pkt.ipdst)

    else:
        for pkt in CSVPackets(csvfile):
            iparr.append(pkt.ipsrc)
            iparr.append(pkt.ipdst)

    dictionary = { x : iparr.count(x) for x in set(iparr)}

    sdictionary = sorted(dictionary.items(), key=lambda kv: kv[1], reverse=True)

    #print "\n"
    #print "\n"

    for x in sdictionary:
        print x

elif connto == 1:
    ipdic = {}
    proto_port = ""

    for pkt in CSVPackets(csvfile):
        check = 0
        if pkt.proto == 6:
            if pkt.tcpdport < 1025:
                protoport = "tcp/" + str(pkt.tcpdport)
                check = 1
        elif pkt.proto == 17:
            if pkt.udpdport < 1025:
                proto_port = "udp/" + str(pkt.udpdport)
                check = 1

        if check == 1:
            if pkt.ipdst in ipdic:
                ipdic[pkt.ipdst][0].add(pkt.ipsrc)
                ipdic[pkt.ipdst][1].add(proto_port)
            else:
                ipdic[pkt.ipdst] = [set([pkt.ipsrc]), set([proto_port])]

    j = 0
    for k,v in sorted(ipdic.items(), key=lambda (k, v): (len(v[0]), k), reverse=True):
        j += 1
        print "ipdst %s\thas %d\t distinct ipsrc on ports: %s" % (k,len(v[0]), ', '.join(v[1]))
        if j > 20:
            break
csvfile = open(sys.argv[1],'r')
for pkt in CSVPackets(csvfile):
    # pkt.__str__ is defined...
    #print pkt
    numBytes += pkt.length
    numPackets += 1
    proto = pkt.proto & 0xff
    IPProtos[proto] += 1


print "numPackets:%u numBytes:%u" % (numPackets,numBytes)
for i in range(256):
    if IPProtos[i] != 0:
        print "%3u: %9u" % (i, IPProtos[i])
