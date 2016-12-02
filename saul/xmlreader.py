import xml.etree.ElementTree

import sys

import glob

congress = sys.argv[1]

for fno, fn in enumerate(open(congress + ".all", "r")):
    fn = fn.replace("\n", "")
    if fno % 1000 == 0:
        print fno
    try:
        root = xml.etree.ElementTree.parse(fn).getroot()
        sections = root.findall('.//section')
        for section in sections:
            section_text = "".join(section.itertext())
            id = section.attrib["id"]
            bill_no = fn.split('/').pop()
            with open("govtrackdata/" + congress + "/sections/" + id + "_" + fn.replace(".xml", ".txt").replace("/", "_"), "w") as outf:
                outf.write(section_text.encode("ascii", "ignore"))
    except xml.etree.ElementTree.ParseError:
        print "ERROR"