#!/usr/bin/python3
#
# Makes the XENON Latex authorlist for different journal styles
#
# Patrick Decowski, decowski@nikhef.nl
#

from datetime import datetime
import re
import sys

# These are all the XENON institutes as of May 2020. 
institutes = {
    'bologna': r'Department of Physics and Astronomy, University of Bologna and INFN-Bologna, 40126 Bologna, Italy', 
    'chicago': r'Department of Physics \& Kavli Institute for Cosmological Physics, University of Chicago, Chicago, IL 60637, USA', 
    'coimbra': r'LIBPhys, Department of Physics, University of Coimbra, 3004-516 Coimbra, Portugal', 
    'columbia': r'Physics Department, Columbia University, New York, NY 10027, USA', 
    'lngs': r"INFN-Laboratori Nazionali del Gran Sasso and Gran Sasso Science Institute, 67100 L'Aquila, Italy", 
    'mainz': r'Institut f\"ur Physik \& Exzellenzcluster PRISMA, Johannes Gutenberg-Universit\"at Mainz, 55099 Mainz, Germany', 
    'heidelberg': r'Max-Planck-Institut f\"ur Kernphysik, 69117 Heidelberg, Germany', 
    'munster': r'Institut f\"ur Kernphysik, Westf\"alische Wilhelms-Universit\"at M\"unster, 48149 M\"unster, Germany', 
    'nikhef': r'Nikhef and the University of Amsterdam, Science Park, 1098XG Amsterdam, Netherlands', 
    'nyuad': r'New York University Abu Dhabi, Abu Dhabi, United Arab Emirates', 
    'purdue': r'Department of Physics and Astronomy, Purdue University, West Lafayette, IN 47907, USA', 
    'rpi': r'Department of Physics, Applied Physics and Astronomy, Rensselaer Polytechnic Institute, Troy, NY 12180, USA', 
    'rice': r'Department of Physics and Astronomy, Rice University, Houston, TX 77005, USA', 
    'stockholm': r'Oskar Klein Centre, Department of Physics, Stockholm University, AlbaNova, Stockholm SE-10691, Sweden', 
    'subatech': r"SUBATECH, IMT Atlantique, CNRS/IN2P3, Universit\'e de Nantes, Nantes 44307, France", 
    'torino': r'INAF-Astrophysical Observatory of Torino, Department of Physics, University  of  Torino and  INFN-Torino,  10125  Torino,  Italy', 
    'ucsd': r'Department of Physics, University of California San Diego, La Jolla, CA 92093, USA', 
    'wis': r'Department of Particle Physics and Astrophysics, Weizmann Institute of Science, Rehovot 7610001, Israel', 
    'zurich': r'Physik-Institut, University of Z\"urich, 8057  Z\"urich, Switzerland', 
    'paris': r"LPNHE, Sorbonne Universit\'{e}, Universit\'{e} de Paris, CNRS/IN2P3, Paris, France", 
    'freiburg': r'Physikalisches Institut, Universit\"at Freiburg, 79104 Freiburg, Germany',
    'lal': r"Universit\'{e} Paris-Saclay, CNRS/IN2P3, IJCLab, 91405 Orsay, France", 
    'napels': r"Department of Physics ``Ettore Pancini'', University of Napoli and INFN-Napoli, 80126 Napoli, Italy", 
    'nagoya': r'Kobayashi-Maskawa Institute for the Origin of Particles and the Universe, and Institute for Space-Earth Environmental Research, Nagoya University, Furo-cho, Chikusa-ku, Nagoya, Aichi 464-8602, Japan', 
    'laquila': r"Department of Physics and Chemistry, University of L'Aquila, 67100 L'Aquila, Italy", 
    'tokyo': r'Kamioka Observatory, Institute for Cosmic Ray Research, and Kavli Institute for the Physics and Mathematics of the Universe (WPI), the University of Tokyo, Higashi-Mozumi, Kamioka, Hida, Gifu 506-1205, Japan', 
    'kobe': r'Department of Physics, Kobe University, Kobe, Hyogo 657-8501, Japan',
    'ucla': r'Physics \& Astronomy Department, University of California, Los Angeles, CA 90095, USA', 
    'alsoatferrara': r'INFN, Sez. di Ferrara and Dip. di Fisica e Scienze della Terra, Universit\`a di Ferrara, via G. Saragat 1, Edificio C, I-44122 Ferrara (FE), Italy', 
    'alsoatsuny': r'Simons Center for Geometry and Physics and C. N. Yang Institute for Theoretical Physics, SUNY, Stony Brook, NY, USA', 
    'alsoatutrecht': r'Institute for Subatomic Physics, Utrecht University, Utrecht, Netherlands', 
#    'alsoatspacenagoya': r'Institute for Space-Earth Environmental Research, Nagoya University, Nagoya, Aichi 464-8601, Japan', 
    'alsoatcoimbrapoli': r'Coimbra Polytechnic - ISEC, Coimbra, Portugal',
    'alsoatiarnagoya': r'Institute for Advanced Research, Nagoya University, Nagoya, Aichi 464-8601, Japan'
    }

def print_header():
    '''Print the default header at the beginning of the Latex output'''
    print('% Autogenerated on ' + datetime.now().strftime("%d %b, %Y at %H:%M:%S"))
    print('% Generated with make-authorlist.py')
    
def format_prl(list):
    '''Format for PRL/PRC/PRD etc. '''
    print_header()
    print(r'''
% -> SNIP
\documentclass[prl,aps,twocolumn,superscriptaddress,showpacs,showkeys,amsmath,amssymb,floatfix]{revtex4}
\usepackage[colorlinks=true,citecolor=blue,filecolor=blue,linkcolor=blue,urlcolor=blue,pdftex]{hyperref}
\usepackage{currfile} % To be able to list current file name in title
% <- SNIP
''')
    
    for institute in institutes:
        inst = '\\newcommand{\\' + institute + r'}{\affiliation{' + institutes[institute] + '}}'
        print(inst)

    print(r'''
\begin{document}

% CHANGE TO TITLE
\title{XENON Authors \currfilename}
''')
    
    for author in list:
        auth = r'\author{' + author['name'] + '}'
        if author['alsoat']:
            auth = auth + r'\altaffiliation[Also at ]{' + institutes[author['alsoat']] + '}'
        for inst in author['institute']:
            auth = auth + '\\' + inst
        print(auth)
    print(r'''
\collaboration{XENON Collaboration}
\email[]{xenon@lngs.infn.it}
\noaffiliation

\date{\today} 

% CHANGE
\begin{abstract}
\end{abstract}

\pacs{
    95.35.+d, %Dark matter
    14.80.Ly, %Supersymmetric partners of known particles
    29.40.-n,  %Radiation detectors
    95.55.Vj
}

\keywords{Dark Matter, Direct Detection, Xenon}

% <--- SNIP 
\maketitle

\end{document}
''')

def format_epjc(list):
    '''Format for EPJC'''
    print_header()
    print("% NOTE!!! For proper formatting you need epjc3upd.clo !")
    print(r'''
% -> SNIP
\documentclass[epjc3upd,twocolumn]{svjour3}
\usepackage{currfile} % To be able to list current file name in title
% <- SNIP

\journalname{Eur. Phys. J. C}

\begin{document}

% CHANGE TO TITLE
\title{XENON Authors \\currfilename}
''')

    addr_label = {}
    # for EPJC we need an extra level of indirection for addr labels
    for indx, institute in enumerate(institutes):
        addr_label[institute] = 'addr' + str(indx)

    alsoat = []
    sorted_inst = []
    first = True
    for author in list:
        addr = ""
        auth = ""
        if first:
            auth = r'\author{'
            first = False
        else:
            print(r'\and')            
        for inst in author['institute']:
            if addr != "": 
                addr = addr + "," + addr_label[inst]
            else:
                addr = addr_label[inst]
            if not inst in sorted_inst:
                sorted_inst.append(inst)
        if author['alsoat']: # We need to build the list of alsoat institutes
            addr = addr + "," + addr_label[author['alsoat']]
            alsoat.append(author['alsoat'])
        auth = auth + author['name'] + r'\thanksref{' + addr + '}'
        print(auth)
    print(r'(XENON Collaboration\thanksref{email1}). }')
    for institute in institutes:
        inst = '\\newcommand{\\' + institute + '}{' + institutes[institute] + '}'
        print(inst)

    print(r'\authorrunning{XENON Collaboration}')
    for inst in alsoat:
        txt = r'\thankstext{' + addr_label[inst] + '}{Also at \\' + inst + '}'
        print(txt)

    print(r'''
% ADD Corresponding Author Email here:
\thankstext{email1}{\texttt{xenon@lngs.infn.it}}''')

    first = True
    alsoat_dict = dict.fromkeys(alsoat, True)
  
    for institute in sorted_inst:
        if institute in alsoat_dict: # Skip the AlsoAt institutes
            continue
        inst = ""
        if first:
            inst = r'\institute{'
            first = False
        else:
            print(r'\and')
        inst = inst + '\\' + institute + r'\label{' + addr_label[institute] + '}'
        print(inst)
    print(r'''}
\maketitle
\end{document}
''')

def format_jcap(list):
    '''Format for JCAP journal'''
    print_header()
    print(r'''
% -> SNIP
\documentclass[a4paper]{article}
\usepackage{jcappub}
\usepackage{currfile} % To be able to list current file name in title
% <- SNIP

% CHANGE TO TITLE
\title{XENON Authors \\currfilename}

\author{The XENON collaboration: }''')

    inst_label = {}
    inst_label_ordered = []
    also_label = {}
    indx = 0
    indx_also = 0
    first_auth = True
    auth = ''
    post = ''
    for author in list:
        if not first_auth:
            auth = auth + ',' + post + '}'
            print(auth)
        auth = r'\author['
        first_inst = True
        for inst in author['institute']:
            if not first_inst:
                auth = auth + ','
            if not inst in inst_label:
                label = ''
                for i in range(0, int(indx/26)):
                    label = chr(0x61 + i) # ASCII-code 'a'
                inst_label[inst] = label + chr(0x61 + (indx % 26))
                inst_label_ordered.append(inst) # Order according to use in list
                indx = indx + 1
            auth = auth + inst_label[inst]
            first_inst = False
            post = ''
        if author['alsoat']:
            if not author['alsoat'] in also_label:
                also_label[author['alsoat']] = chr(0x31 + indx_also)
            auth = auth + ',' + also_label[author['alsoat']]
            post = '\\note{Also at: ' + institutes[author['alsoat']] + '}'
            indx_also = indx_also + 1
        else:
            post = ''
        auth = auth + r']{' + author['name']
        first_auth = False
    # Last author is special because list ends with a period and not comma
    auth = auth + post + '.}'
    print(auth)

    # Make the affiliations
    for inst in inst_label_ordered:
        affil = r'\affiliation[' + inst_label[inst] + ']{' + institutes[inst] + '}'
        print(affil)

    print(r'''
\keywords{Dark matter experiments, dark matter simulations}

\begin{document}
\maketitle

\end{document}
''')

def format_arxiv(list):
    '''Format for arXiv - during submission'''
    output = ""
    first = True
    for author in list:
        auth = author['name']
        auth = auth.replace('~', ' ')
        if first:
            output = auth
            first = False
        else:
            output = output + ', ' + auth
    print(output)
        
def read_authorlist(filename):
    ''' Read the XENON author list in the format: author: affil1, affil2 % comment'''

    rx = re.compile(r'(?P<name>.*)\:\s*(?P<institute>\S*)\s*?\%?\s*(?P<comment>.*)\n')
    rx_inst = re.compile(r'(?P<inst1>\w+)\,?(?P<inst2>\w*)')
    rx_also = re.compile(r'.*?(?P<alsoat>alsoat\w*)')

    list = []
    with open(filename, 'r') as file:
        for line in file:
            if line[0] == "#":
                # Skip comments
                continue
            match = rx.search(line)
            if match:
                author = { }
                author['name'] = match.group("name")
                m = rx_inst.search(match.group("institute"))
                a = rx_also.search(match.group("institute"))
                institute = [] # Can be multiple institutes
                for inst in m.groups():
                    if (a and inst == a.group("alsoat")) or inst == "":
                        continue
                    institute.append(inst)
                author['institute'] = institute
                if a:
                    author['alsoat'] = a.group("alsoat")
                else:
                    author['alsoat'] = None
                list.append(author)
            else:
                print("Failed on:", line)
                sys.exit(1)
    return list

def usage():
    print("make-authorlist.py --prl | --epjc | --jcap | --arxiv filename")
    sys.exit(0)
    
options = { "--prl": format_prl,
            "--epjc": format_epjc,
            "--jcap": format_jcap,
            "--arxiv": format_arxiv,
            "--help": usage }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
    option = sys.argv[1]
    filename = sys.argv[2]
    list = read_authorlist(filename)
    try:        
        options[option](list)
    except KeyError:
        usage()
