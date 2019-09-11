import re

def hilbertrewrite(z):
    def replace(s):
        if s.group(0) == "A":
            return "-BF+AFA+FB-"
        if s.group(0) == "B":
            return "+AF-BFB-FA+"
    return re.sub('[AB]', replace, z)

def curve(m):
    z = "A"
    for i in range(m):
        z = hilbertrewrite(z)
    return re.sub("[AB]", "", z)
