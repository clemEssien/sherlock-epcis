import xml
import xml.etree.ElementTree as ET

def main() :
    tree = ET.parse("XMLDeserialization/GS1StandardExample1.xml")
    root = tree.getroot()

    if root.tag != "{urn:epcglobal:epcis:xsd:1}EPCISDocument" :       
        print("Not EPCISDocument")
        return
    eventDicts = []
    for event in root.iter('EventList') :
        myDict = {}
        for ob in event :
            for child in ob :
                print(child.tag)
                if len(child) :
                    if(child.tag == "readPoint" or child.tag == "bizLocation") :
                        myDict[child.tag] = child[0].text
                    else :
                        childDicts = []
                        for subchild in child :
                            childDict = {}
                            childDict[subchild.tag] = subchild.text
                            childDicts.append(childDict)
                        myDict[child.tag] = childDicts
                else :
                    myDict[child.tag] = child.text
        print(myDict)
        break
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