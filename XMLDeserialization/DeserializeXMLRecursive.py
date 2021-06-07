#Author: Kevin Zong and Helina Solomon
#Last Modified: June 7th, 2021
#Script to deserialize standard EPCIS documents in XML form recursively in order to avoid the <extension> tags
import xml
import xml.etree.ElementTree as ET

def main():
    eventDicts = []
    tree = ET.parse('XMLDeserialization/GS1StandardExample4.xml')
    root = tree.getroot()

    if root.tag != "{urn:epcglobal:epcis:xsd:1}EPCISDocument" :                     #Check for the EPCISDocument tag 
        print("Not EPCISDocument")
        return
    eventDicts = []
    for list in root.iter('EventList'):
        for event in list:
            myDict = {}
            if(event.tag == "extension") :
                for subEvent in event :
                    print(subEvent.tag)
                    myDict.update(parseTag(subEvent))
                    tempDict = myDict.copy()
                    eventDicts.append(tempDict)
            else :
                print(event.tag)
                myDict.update(parseTag(event))
                tempDict = myDict.copy()
                eventDicts.append(tempDict)
    print(eventDicts)

def parseTag(node):
    nodeDict = {}
    #check for base tag cases (Unifinished)
    #if (identyfy lists and deal with them specifically)
    #if not present parse subchildren
    #else:
    if len(node):
        for child in node:
            #print('parsing ' +child.tag)
            nodeDict.update(parseTag(child))
    else:
        nodeDict[node.tag] = node.text
    return nodeDict

if __name__ == '__main__' :
    main()
