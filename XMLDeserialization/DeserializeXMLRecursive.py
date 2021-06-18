# Author: Kevin Zong and Helina Solomon
# Last Modified: June 10th, 2021
# Script to deserialize standard EPCIS documents in XML form recursively in order to avoid the <extension> tags
import xml
import pprint
import xml.etree.ElementTree as ET


def main():
    parse_xml("./data/GS1StandardExample4.xml")

def parse_tag(node):
    nodeDict = {}
    if (
        node.tag == "epcList"
        or node.tag == "childEPCs"
        or node.tag == "inputEPCList"
        or node.tag == "outputEPCList"
    ):  # epc lists
        # print('parsing an epcList')
        uriList = []
        for epc in node:
            uriList.append(epc.text)
        if len(uriList) > 0:
            nodeDict[node.tag] = uriList
    elif node.tag == "readPoint" or node.tag == "bizLocation":
        # print('parsing readPoint or bizLocation')
        for id in node:
            nodeDict[node.tag] = parse_tag(id)
    elif (
        node.tag == "bizTransactionList"
        or node.tag == "sourceList"
        or node.tag == "destinationList"
    ):  # typed lists
        dictList = []
        for listElement in node:
            typedDict = {}
            typedDict["type"] = listElement.get("type")
            typedDict[listElement.tag] = listElement.text
            tempDict = typedDict.copy()
            dictList.append(tempDict)
        nodeDict[node.tag] = dictList
    elif (
        node.tag == "quantityList"
        or node.tag == "childQuantityList"
        or node.tag == "inputQuantityList"
        or node.tag == "outputQuantityList"
    ):  # quantity lists
        dictList = []
        for listElement in node:
            dictList.append(parse_tag(listElement))
        nodeDict[node.tag] = dictList
    elif node.tag == "ilmd":  # instance lot master data
        dictDict = {}
        for element in node:
            dictDict.update(parse_tag(element))
        nodeDict[node.tag] = dictDict
    else:
        if len(node):  # recursively parse subchildren
            for child in node:
                nodeDict.update(parse_tag(child))
        else:
            nodeDict[node.tag] = node.text
    return nodeDict

def parse_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    if (
        root.tag != "{urn:epcglobal:epcis:xsd:1}EPCISDocument"
    ):  # Check for the EPCISDocument tag
        print("Not EPCISDocument")
        return
    eventDicts = []  # List of Event dicts
    for list in root.iter("EventList"):
        for event in list:  # Iterate through each event
            if event.tag == "extension":  # Check for extension tag on Event
                for subEvent in event:  # Iterate through each event in extension
                    # print(subEvent.tag)
                    myDict = {}
                    myDict["isA"] = subEvent.tag
                    myDict.update(parse_tag(subEvent))
                    tempDict = myDict.copy()
                    eventDicts.append(tempDict)
            else:
                # print(event.tag)
                myDict = {}
                myDict["isA"] = event.tag
                myDict.update(parse_tag(event))
                tempDict = myDict.copy()
                eventDicts.append(tempDict)
    print(eventDicts)
    pp = pprint.PrettyPrinter(indent=2)
    for event in eventDicts:
        pp.pprint(event)
        print()

if __name__ == "__main__":
    main()
