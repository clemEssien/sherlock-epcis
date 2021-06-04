import xml
import xml.etree.ElementTree as ET

def main() :
    events = []
    events_objects = []
    tree = ET.parse("XMLDeserialization/GS1StandardExample1.xml")
    root = tree.getroot()

    if root.tag == "EPCISDocument" :        # doesnt work but concept
        print("worked")

    for child in root.iter('EventList') :
        for event in child :
            for ob in event :
                if len(ob) :                    # check if child of root has subchildren
                    for subChild in ob :
                        print(subChild.text)
                else :                          # no subchildren
                    print(ob.text)

if __name__ == '__main__' :
    main()