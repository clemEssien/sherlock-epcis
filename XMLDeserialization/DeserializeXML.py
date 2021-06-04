# Author: Helina Solmn and Kevin Zong
# Last Modified: June 4, 2021
# Script to deserialize standard EPCIS documents in XML form.
import xml
import xml.etree.ElementTree as ET

def main() :
    tree = ET.parse("XMLDeserialization/GS1StandardExample1.xml")
    root = tree.getroot()

    if root.tag != "{urn:epcglobal:epcis:xsd:1}EPCISDocument" :                     #Check for the EPCISDocument tag 
        print("Not EPCISDocument")
        return
    eventDicts = []                                                                 #List of Event Dicts
    for list in root.iter('EventList') :                                           #Iterate through each event
        myDict = {}
        for event in list :
            for child in event :
                print(child.tag)
                if len(child) :                                                     #Check for lists (e.g. epcList, businessTransactionList)
                    if(child.tag == "readPoint" or child.tag == "bizLocation") :    #Check for specific outliers
                        myDict[child.tag] = child[0].text                           #Extract the id uris
                    else :
                        childDicts = []
                        for subchild in child :                                     #Create a dict for each list element
                            childDict = {}
                            childDict[subchild.tag] = subchild.text
                            childDicts.append(childDict)
                        myDict[child.tag] = childDicts                              #Append the list[dict]
                else :
                    myDict[child.tag] = child.text                                  #Append the URI
            eventDicts.append(myDict)
    print(eventDicts)
                # myDict[ob.tag].append(ob.text)
        #for event in child :
        #    if len(event) :
         #       for ob in event :
         #           keyList.append(ob.tag)
        #myDict = dict.fromkeys(keyList, [])
        #for event in child :
          #  for ob in event :
         #       myDict[ob.tag].append(ob.text)
   #print(myDict)

if __name__ == '__main__' :
    main()