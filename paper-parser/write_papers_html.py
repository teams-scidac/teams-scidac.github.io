# due to Unicode, this requires python 3+

# we take 3 bibtex files:
#
# refereed.bib
# others.bib
# presentations.bib
#
# and the templar

import parser


class PaperCollection(object):
    def __init__(self, key, papers, ostr=""):
        self.key = key
        self.papers = papers
        self.ostr = ostr

all_papers = []
print("working on refereed.bib")
all_papers.append(PaperCollection("@@refereed@@", parser.parse_bibfile("refereed.bib")))
print("working on others.bib")
all_papers.append(PaperCollection("@@others@@", parser.parse_bibfile("others.bib")))
print("working on presentations.bib")
all_papers.append(PaperCollection("@@presentations@@", parser.parse_bibfile("presentations.bib")))

# open the template and the output
tf = open("papers.template", "r")
dh = open("../papers.html", "w")

for pc in all_papers:

    if not pc.papers:
        continue

    # sort by date
    current_year = 3000
    first = True
    ostr = ""

    years = list(set([p.year for p in pc.papers]))
    years.sort(reverse=True)

    for p in pc.papers:
        if p.year < current_year:
            if not first:
                ostr += "</table>\n</div>\n\n"
            else:
                first = False

            ostr += "<p><h3><a name='{}'></a>{}</h3>\n".format(p.year, p.year)

            ostr += "<div class='table-wrapper'>\n"
            ostr += "  <table>\n"

        current_year = p.year

        t, o, l = p.jstring()
        ostr += "<tr><td>"
        if not l == "":
            ostr += "<a href='{}'><em>{}</em></a><br>\n".format(l, t)
        else:
            ostr += "<em>{}</em><br>\n".format(t)

        ostr += "{}</td></tr>\n".format(o)

    ostr += "</table>\n</div>\n"
    pc.ostr = ostr


for line in tf:
    for pc in all_papers:
        line = line.replace(pc.key, pc.ostr)
    dh.write(line)

dh.close()
tf.close()

