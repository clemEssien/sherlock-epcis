import xml
import xml.etree.ElementTree as ET

def main() :
    events = []
    events_objects = []
    tree = ET.parse("XMLDeserialization/GS1StandardExample1.xml")
    root = tree.getroot()

    if root.tag != "{urn:epcglobal:epcis:xsd:1}EPCISDocument" :       
        print("Not EPCISDocument")
        return

    for child in root.iter('EventList') :
        keyList = []
        myDict = {}
        for event in child :
            for ob in event :
                keyList.append(ob.tag)
        myDict = dict.fromkeys(keyList, [])
        for event in child :
            for ob in event :
                myDict[ob.tag].append(ob.text)
        print(myDict)

if __name__ == '__main__' :
    main()