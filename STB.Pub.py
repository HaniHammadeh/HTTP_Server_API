#!/usr/bin/python

######## -Description : This file is provides to set HTTP server DB with the required files
######## which are 'LPI', Phone number, UserID
######## - Filename : STB.py
######## - Programming Language : Python, OS is Linux 
######## - Author: Hani Hammadeh, hani.hammadeh@gmail.com
######## - Version: 1.0
######## - TODO is add the log facility
######## - FIXME is optimizing the string parsing 

import csv,re,sys,httplib
import xml.dom
import xml.dom.minidom
import time
mac_list = []
found = ''
found_t = ''
mac_list = []
ph = []
uid = []
location = []
slot = ''
port = ''
oltname = ''
m = ''
str = ''
prefix = 'TVRO.ENC.CAS.P2.'
region = ''
lthree = ''
fcc = ''
olt_exchange = ''
olt_nr = ''
card = ''
olt = ''
lthree = ''
aname = 'TVRO.ENC.CAS.P2.[REGION].[FCC].[L3].[OLT_EXCHANGE].[OLT_NR].[CARD].[OLT]'
ulocation = []
lthree_t = ''
stb_f = '/opt/STB/STB2/STB/STBs.txt'
fcc_f = '/opt/STB/STB2/STB/fcc.txt'
l3_f = '/opt/STB/STB2/STB/l3.txt'
j =  0
class STB(object):
 def __init__(self, SM):
  self.SM = SM
  mac_list = []
 def _get_uid(self, mac):
	#SoapmMessage = self.SM
    SM_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
        <SOAP-ENV:Envelope xmlns:ns3="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:ns0="http://www.agama.tv/ws/emp" xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns2="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <SOAP-ENV:Header/>
         <ns1:Body>
         <ns0:getMetadataForProbes>
                 <probes xsi:type="ns0:ArrayOfString" ns3:arrayType="ns2:string[1]">
                <item xsi:type="ns2:string">"""+mac+"""</item>

                </probes>
                 <metadata_types xsi:type="ns0:ArrayOfString" ns3:arrayType="ns2:string[1]">
                 <item xsi:type="ns2:string">user_account_id</item>
                 </metadata_types>
         </ns0:getMetadataForProbes>
           </ns1:Body>
        </SOAP-ENV:Envelope>
        """
    
    self.SM = SM_TEMPLATE
    ws = httplib.HTTP("0.0.0.0:8008")
    ws.putrequest("POST", "/ws/emp")
    ws.putheader("Host", "0.0.0.0:8008")
    ws.putheader("User-Agent", "Python post")
    ws.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
    ws.putheader("Content-length", "%d" % len(self.SM))
    ws.putheader("SOAPAction", "\"\"")
    ws.endheaders()
    ws.send(SM_TEMPLATE)
    # get the response
    statuscode, statusmessage, header = ws.getreply()
    print "Response: ", statuscode, statusmessage
    print "headers: ", header
    res = ws.getfile().read()
	#print res
	####################### SAVE THE RESULT TO A TEXT FILE
    print res
    with open("log.uid.xml", "w") as uidf:
        #print res
        uidf.write(res)
    doc = xml.dom.minidom.parse('log.uid.xml')
    node = doc.getElementsByTagName('value')
    for n in node:
     for cn in n.childNodes:
        print(cn.nodeValue)
        #location.append(cn.nodeValue) ### filling the location array with the required value
	res = cn.nodeValue
    return 	res
 def _get_mac_list(self):
	#SoapmMessage = self.SM
	ws = httplib.HTTP("0.0.0.0:8008")
	ws.putrequest("POST", "/ws/emp")
	ws.putheader("Host", "0.0.0.0:8008")
	ws.putheader("User-Agent", "Python post")
	ws.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
	ws.putheader("Content-length", "%d" % len(self.SM))
	ws.putheader("SOAPAction", "\"\"")
	ws.endheaders()
	ws.send(self.SM)
	# get the response
	statuscode, statusmessage, header = ws.getreply()
	print "Response: ", statuscode, statusmessage
	print "headers: ", header
	res = ws.getfile().read()
	#print res
	####################### SAVE THE RESULT TO A TEXT FILE
	print res
	with open("out.txt", "w") as f:
         #print res
         f.write(res)
 def _filter_mac_list(self):
   global found 
   global found_t  
   global mac_list 
   global ph  
   global uid 
   global j
   with open("out.txt", "r") as f:
    for line in f:
	time.sleep(1)
        try:
                found = re.search('([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})', line).group()
                #print found
                #print line
                found_t = found
                found = found.replace(':', '') ### change the format of the MAC address
                with open(stb_f, "r") as csvf:
                   reader = csv.DictReader(csvf)
                   for row in reader:
                        #print row
                        #print row['MACADDRESS']
                        if row['MACADDRESS'].upper() == found.upper(): #### UPPER CASE for both then use 
                                #print row ['ip']
                                print found
                                mac_list.append(found_t) ### this is the mac address's vectore
                                ph.append(row['PHONENUM']) ### this is the phone number
                                #uid.append(row['USERID']) ### this is the user id
				#uid.append(self._get_uid(found_t))
				j = j+1
				break
                                print 'found--------------------------------------------'
        except AttributeError:
                found = ''
	#if j == 4:
	# break
 def _get_current_lpi(self, SM):
   self.SM = SM
   ws = httplib.HTTP("0.0.0.0:8008")
   ws.putrequest("POST", "/ws/emp")
   ws.putheader("Host", "0.0.0.0:8008")
   ws.putheader("User-Agent", "Python post")
   ws.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
   ws.putheader("Content-length", "%d" % len(self.SM))
   ws.putheader("SOAPAction", "\"\"")
   ws.endheaders()
   ws.send(self.SM)
    # get the response
   statuscode, statusmessage, header = ws.getreply()
   print "Response: ", statuscode, statusmessage
   print "headers: ", header
   res = ws.getfile().read()
   print res
   print '--------------------------------------------print location-------------------'
  #for i in range(len(li_list)):
  # m = li_list[i]
  # print m #
   with open("log.xml", "w") as lpif:
        #print res
        lpif.write(res)
   doc = xml.dom.minidom.parse('log.xml')
   node = doc.getElementsByTagName('value')
   for n in node:
    for cn in n.childNodes:
        print(cn.nodeValue)
        location.append(cn.nodeValue) ### filling the location array with the required value
 def _getStr (self, str1, str2):
  global port
  global oltname
  global slot
  global card
  global olt
  global olt_exchange
  global olt_nr
  global region
  print str1
  print str2
  str1 = str1.replace('http://86.96.241.17:7547/ACS-server/ACS/', '')
  m = re.search('HO', str1)
  if m:
    str2 = str1.split('/')
    oltname = str2[0]
    slot = str2[3]
    port = str2[5]
  m = re.search('AO', str1)
  if m:
        str2 = str1.split('/')
        oltname = str2[0]
        slot = str2[4]
        port = str2[5]
  m = re.search('ZO', str1)
  if m:
        str2 = str1.split('/')
        oltname = str2[0]
        str2 = str2[1].split('-')
        slot = str2[1]
        port = str2[2]
  print 'oltname is : '+ oltname
  print 'port is : '+ port
  print 'slot is : ' + slot
  card = slot
  print 'card is : ' + card
  olt = port
  print ' olt is :' +olt
  str2 = oltname.split('-')
  olt_exchange = str2[1]
  print 'olt exchange is :'+ olt_exchange
  olt_nr = str2[2]
  print ' olt_nr is :' + olt_nr
  region = str2[0]
  return;
 def _get_lthree(self, x, str):
  global lthree
  global oltname
  x = oltname
  with open(l3_f, "r") as csvf:
    str = csv.DictReader(csvf)
    print ' X is ' +x
    for row in str:
        #print row
	#time.sleep(1)
       # print 'oltname is ------------------------' + oltname
        if row['OLTHostname'] == x:

                 lthree = row['L3AGG-1Hostname']
		 break
                 #print 'lthree  is :----------------------------------------------' + lthree
  return lthree[:-2];
 def _get_fcc(self, x, str):
  global fcc
  global lthree
  x = lthree
 # print ' lthree is **********************************************************************' + lthree
  with open(fcc_f, "r") as csvf:
    str = csv.DictReader(csvf)
    for row in str:
        print row
        if row['L3AGG-1Hostname'] == x:

                 fcc = row['FCC-1Hostname']
                # print  'fcc is ------------------------------------------' + fcc
                 return lthree[:-2];
 def _set_lpi(self, mac, lpi):
        SM_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
                        <SOAP-ENV:Envelope xmlns:ns3="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:ns0="http://www.agama.tv/ws/emp" xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns2="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
           <SOAP-ENV:Header/>
           <ns1:Body>
                  <ns0:setMetadataForProbes>
                         <metadata xsi:type="ns0:ArrayOfProbeMetadataStruct" ns3:arrayType="ns0:ProbeMetadataStruct[2]">

                                <item xsi:type="ns0:ProbeMetadataStruct">
                                   <id xsi:type="ns2:string">"""+mac+"""</id>
                                        <metadata xsi:type="ns0:ArrayOfProbeMetadataItem" ns3:arrayType="ns0:ProbeMetadataItem[1]">
                                          <item xsi:type="ns0:ProbeMetadataItem">
                                                 <name xsi:type="ns2:string">lpi</name>
                                                 <value xsi:type="ns2:string">"""+lpi+"""</value>
                                          </item>
                                   </metadata>
                                </item>
                         </metadata>
                  </ns0:setMetadataForProbes>
           </ns1:Body>
        </SOAP-ENV:Envelope>
        """
        SoapMessage = SM_TEMPLATE
        ws = httplib.HTTP("0.0.0.0:8008")
        ws.putrequest("POST", "/ws/emp")
        ws.putheader("Host", "0.0.0.0:8008")
        ws.putheader("User-Agent", "Python post")
        ws.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
        ws.putheader("Content-length", "%d" % len(SoapMessage))
        ws.putheader("SOAPAction", "\"\"")
        ws.endheaders()
        ws.send(SoapMessage)
        return;
 def _set_phone(self, mac, phone):
        SM_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
                        <SOAP-ENV:Envelope xmlns:ns3="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:ns0="http://www.agama.tv/ws/emp" xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns2="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
           <SOAP-ENV:Header/>
           <ns1:Body>
                  <ns0:setMetadataForProbes>
                         <metadata xsi:type="ns0:ArrayOfProbeMetadataStruct" ns3:arrayType="ns0:ProbeMetadataStruct[2]">

                                <item xsi:type="ns0:ProbeMetadataStruct">
                                   <id xsi:type="ns2:string">"""+mac+"""</id>
                                        <metadata xsi:type="ns0:ArrayOfProbeMetadataItem" ns3:arrayType="ns0:ProbeMetadataItem[1]">
                                          <item xsi:type="ns0:ProbeMetadataItem">
                                                 <name xsi:type="ns2:string">user_defined_1</name>
                                                 <value xsi:type="ns2:string">"""+phone+"""</value>
                                          </item>
                                   </metadata>
                                </item>
                         </metadata>
                  </ns0:setMetadataForProbes>
           </ns1:Body>
        </SOAP-ENV:Envelope>
        """
        SoapMessage = SM_TEMPLATE
        ws = httplib.HTTP("0.0.0.0:8008")
        ws.putrequest("POST", "/ws/emp")
        ws.putheader("Host", "0.0.0.0:8008")
        ws.putheader("User-Agent", "Python post")
        ws.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
        ws.putheader("Content-length", "%d" % len(SoapMessage))
        ws.putheader("SOAPAction", "\"\"")
        ws.endheaders()
        ws.send(SoapMessage)
        return;
 def _set_userid(self, mac, userid):
        SM_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
                        <SOAP-ENV:Envelope xmlns:ns3="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:ns0="http://www.agama.tv/ws/emp" xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns2="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
           <SOAP-ENV:Header/>
           <ns1:Body>
                  <ns0:setMetadataForProbes>
                         <metadata xsi:type="ns0:ArrayOfProbeMetadataStruct" ns3:arrayType="ns0:ProbeMetadataStruct[2]">

                                <item xsi:type="ns0:ProbeMetadataStruct">
                                   <id xsi:type="ns2:string">"""+mac+"""</id>
                                        <metadata xsi:type="ns0:ArrayOfProbeMetadataItem" ns3:arrayType="ns0:ProbeMetadataItem[1]">
                                          <item xsi:type="ns0:ProbeMetadataItem">
                                                 <name xsi:type="ns2:string">user_defined_2</name>
                                                 <value xsi:type="ns2:string">"""+userid+"""</value>
                                          </item>
                                   </metadata>
                                </item>
                         </metadata>
                  </ns0:setMetadataForProbes>
           </ns1:Body>
        </SOAP-ENV:Envelope>
        """
        SoapMessage = SM_TEMPLATE
        ws = httplib.HTTP("0.0.0.0:8008")
        ws.putrequest("POST", "/ws/emp")
        ws.putheader("Host", "0.0.0.0:8008")
        ws.putheader("User-Agent", "Python post")
        ws.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
        ws.putheader("Content-length", "%d" % len(SoapMessage))
        ws.putheader("SOAPAction", "\"\"")
        ws.endheaders()
        ws.send(SoapMessage)
        return;

#######################THE MAIN BODY#################################################################### 

SM_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:emp="http://www.agama.tv/ws/emp">
   <soapenv:Header/>
      <soapenv:Body>
            <emp:getProbesInGroup soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                     <groupName xsi:type="xsd:string">All</groupName>
            </emp:getProbesInGroup>
      </soapenv:Body>
 </soapenv:Envelope>
"""
#########################################################################################################
_my_STB = STB(SM_TEMPLATE)
_my_STB._get_mac_list()
_my_STB._filter_mac_list()
######################### ###############################################################################
SM_TEMPLATE = ''
for i in range(len(mac_list)):
  time.sleep(1)
  m = mac_list[i]
  print m #### M will return the location of the STB with a specific unprocessed format.
  SM_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
        <SOAP-ENV:Envelope xmlns:ns3="http://schemas.xmlsoap.org/soap/encoding/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:ns0="http://www.agama.tv/ws/emp" xmlns:ns1="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns2="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
         <SOAP-ENV:Header/>
         <ns1:Body>
         <ns0:getMetadataForProbes>
                 <probes xsi:type="ns0:ArrayOfString" ns3:arrayType="ns2:string[1]">
                <item xsi:type="ns2:string">"""+m+"""</item>

                </probes>
                 <metadata_types xsi:type="ns0:ArrayOfString" ns3:arrayType="ns2:string[1]">
                 <item xsi:type="ns2:string">location_description</item>
                 </metadata_types>
         </ns0:getMetadataForProbes>
           </ns1:Body>
        </SOAP-ENV:Envelope>
        """
  _my_STB._get_current_lpi(SM_TEMPLATE)
####### FIXME For each STB, 1) get the current location. 2) re-generate the parameters 3) set the actual location 4) set the 
#for i in range(len(location)):
#for i in range(3):
# print location[i]
for i in range(len(location)):
   time.sleep(1)
   m = location[i]
   print 'm is ...'+ m ####### HANDLE the string
   if m.count('/') > 5 :

           _my_STB._getStr(m, str) ## parse the sting and produce the required strings as below
	   print 'oltname is : '+ oltname
	   print 'port is : '+ port
	   print 'slot is : ' + slot
	   print 'card is : ' + card
	   print ' olt is :' +olt
	   print ' olt_nr is :' + olt_nr
	   print ' getting lthree value .... please wait!...'
	   lthree_t = _my_STB._get_lthree(oltname, str)#### get the L3 value
	   print 'lthree is ' + lthree
	   print ' getting FCC value ..please wait!....'
	   #print 'lthree_t is ' + lthree_t
	   _my_STB._get_fcc(lthree, str) ### get the FCC value
	   print 'fcc is :' + fcc
	   aname = prefix+region+'.'+fcc[:-2]+'.'+lthree[:-2]+'.'+olt_exchange+'.'+olt_nr+'.'+card+'.'+olt+'.'+mac_list[i]### THE ultimate location value
	   print 'aname is : '+ aname
   else:
        aname = m + '    null'
   ulocation.append(aname)
   time.sleep(1)
###############################################
for i in range(len(ph)):
	print ph[i]

### For Test only
#_my_STB._set_lpi(mac_list[0], ulocation[0])
#### TODO for the rest vectors of phone, and UID 'set', add delay function
#for i in range ( len(mac_list)):

#_my_STB._set_lpi('00:03:78:4b:3a:f4','http://86.96.241.17:7547/ACS-server/ACS/DXB-OBS-HO01/xpon/0/2/0/0/46/1511/14')
for i  in range(len(ulocation)):
#for i  in range(3):
	time.sleep(1)
	print ulocation[i]
	print mac_list[i]
	_my_STB._set_lpi(mac_list[i], ulocation[i])
	_my_STB._set_phone(mac_list[i], ph[i])
	uid.append(_my_STB._get_uid(mac_list[i]))
	_my_STB._set_userid(mac_list[i], uid[i])
