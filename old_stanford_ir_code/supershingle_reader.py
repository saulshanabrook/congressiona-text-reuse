digit = None
files = []
with open("supershingles.sorted") as inf:
    for ln in inf:
        doc, num = ln.replace("\n", "").split(",")
        if num != digit:
            digit = num
            # 'sketches/demos_congress#hr_202.anno_8'
            uniques = set([f.split("#")[1].split(".")[0] for f in files])
            if len(uniques) > 1:
                print set(files)
            files = []
        files.append(doc)