import os
import re
import requests
"""
Program to search through all markdown files in the repo, and look for links in the form:
(*)[<relative link>]:perm

The relative link can be from the root, or from the current directory
i.e:
['potatoes'](Front_Page.png):perm
['potatoes'](/logo_512.png):perm
both convert to permalinks correctly.
If you want it to be linked as a raw file (necessary for embedded images), add that filetype to the imgEndings array.

If we are done with writeups for a particular CTF, add the name of that directory
to exclude array.
"""


base_github_url = "https://github.com/hgarrereyn/Th3g3ntl3man-CTF-Writeups/tree/dev/"
shortened_github_url = base_github_url[len("https://github.com"):] + 'blob/'
check_files_ending_in = ".md"
reSearch = re.compile("(\[.*?\]\(.*?\):perm)")
imgEndings = ['.png','.jpg','.jpeg','.gif']
exclude = ['.git','picoCTF_2017','tamuCTF']

def main():
    notFound = []
    for root, dirs, files in os.walk('.', topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        for f in files:
            if(f.endswith(check_files_ending_in)):
                fcontents = open(root+'/'+f).read()
                matches = reSearch.findall(fcontents)
                if(len(matches)>0):
                    print(("Found %s links to update in " + root+'/'+f) % len(matches))
                    for match in matches:
                        # Convert these to permalinks
                        path = match[match.index('(')+1:match.index(')')]
                        useRaw = False
                        for ending in imgEndings:
                            if(path.endswith(ending)):
                                useRaw = True
                                break
                        URL = ""
                        if(path[0]=='/'):
                            URL = base_github_url + path[1:]
                        elif(path[:4] == 'http'):
                            print(path + " is a URL, trying to convert it anyway...")
                            URL = path
                        else:
                            URL =  base_github_url + root + '/' + path
                        githubURL = convertURLtoPermalink(URL)
                        if(githubURL == -1):
                            notFound.append(path + " linked from file: " + root+'/'+f)
                            continue
                        if(useRaw):
                            githubURL = githubURL + "?raw=true"
                        newMatch = match.replace(path,githubURL)[:-5]
                        print("converting %s to %s" % (match,newMatch))
                        fcontents = fcontents.replace(match,newMatch)
                    open(root+'/'+f,'w').write(fcontents)
    if(len(notFound) > 0):
        print("The following files were not found: " + str(notFound))


def convertURLtoPermalink(URL):
    #print(URL)
    r = requests.get(URL)
    text = r.text
    #print(text)
    try:
        cutdownText = text[:text.index("class=\"d-none js-permalink-shortcut\" data-hotkey=\"y\">Permalink</a>")]
        cutdownText = cutdownText[cutdownText.rindex("<a href=\"")+9:-2]
        return "https://github.com" + cutdownText
    except:
        print("----------File %s not found----------" % URL)
        print("Are you sure you committed and pushed it?")
        return -1

main()
