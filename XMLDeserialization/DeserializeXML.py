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
        for event in child :
            for ob in event :
                if len(ob) :                    # check if child of root has subchildren
                    print(ob.tag)
                    print(ob.text)
                    for subChild in ob :
                        print(subChild.tag)
                        print(subChild.text)
                else :                          # no subchildren
                    print(ob.tag)
                    print(ob.text)

if __name__ == '__main__' :
    main()