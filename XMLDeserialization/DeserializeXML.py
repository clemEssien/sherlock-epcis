import xml
import xml.etree.ElementTree as ET

def main() :
    tree = ET.parse("XMLDeserialization/GS1StandardExample1.xml")
    root = tree.getroot()

    if root.tag != "{urn:epcglobal:epcis:xsd:1}EPCISDocument" :       
        print("Not EPCISDocument")
        return

    for event in root.iter('EventList') :
        keyList = []
        myDict = {}
        for ob in event :
            for child in ob :
                print(child.tag)
                if len(child) :
                    for subchild in child :
                        if(ob.text != '\n        ') :
                            keyList.append(ob.text)
                    myDict[child.tag] = keyList
                else :
                    myDict[child.tag] = child.text
            break
    print(myDict)
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