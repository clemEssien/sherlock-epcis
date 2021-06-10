#Author: Kevin Zong and Helina Solomon
#Last Modified: June 10th, 2021
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
    eventDicts = []                                                                 #List of Event dicts
    for list in root.iter('EventList'):
        for event in list:                                                          #Iterate through each event 
            myDict = {}
            if(event.tag == "extension") :                                          #Check for extension tag on Event
                for subEvent in event :                                             #Iterate through each event in extension
                    #print(subEvent.tag)
                    myDict["isA"] = subEvent.tag
                    myDict.update(parseTag(subEvent))                               
                    tempDict = myDict.copy()
                    eventDicts.append(tempDict)                                     
            else :
                #print(event.tag)
                myDict["isA"] = event.tag            
                myDict.update(parseTag(event))
                tempDict = myDict.copy()
                eventDicts.append(tempDict)
    print(eventDicts)

def parseTag(node):
    nodeDict = {}
    if(node.tag == 'epcList' or node.tag == 'childEPCs' or node.tag == 'inputEPCList' or node.tag == 'outputEPCList') : #epc lists
        #print('parsing an epcList')
        uriList = []
        for epc in node :
            uriList.append(epc.text)
        if(len(uriList) > 0):    
            nodeDict[node.tag] = uriList
    elif(node.tag == 'readPoint' or node.tag == 'bizLocation') :
        #print('parsing readPoint or bizLocation')
        for id in node:
            nodeDict[node.tag] = parseTag(id)
    elif(node.tag == 'bizTransactionList' or node.tag == 'sourceList' or node.tag == 'destinationList') : #typed lists
        dictList = []
        for listElement in node:
            transactionDict = {}
            transactionDict['type'] = listElement.get('type')
            transactionDict[listElement.tag] = listElement.text
            tempDict = transactionDict.copy()
            dictList.append(tempDict)
        nodeDict[node.tag] = dictList
    elif(node.tag == 'quantityList' or node.tag == 'childQuantityList' or node.tag == 'inputQuantityList' or node.tag == 'outputQuantityList') :
        dictList = []
        for listElement in node:
            dictList.append(parseTag(listElement))
        nodeDict[node.tag] = dictList
    else:
        if len(node):
            for child in node:
                #print('parsing ' +child.tag)
                nodeDict.update(parseTag(child))
        else:
            nodeDict[node.tag] = node.text
    return nodeDict

if __name__ == '__main__' :
    main()
