#script for get names from url
#http://www.cute-baby-names.com
import os
import sys
import requests
import cfscrape
import bs4 as bs
import lxml

def script_path():
    path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  #it seems to be quite important
    return path
    
def get_content(url="", ANTISPAM=True):
    if not ANTISPAM:
        res = requests.get(url)
        content = res.text
        status = res.status_code
    else:
        scraper = cfscrape.create_scraper(delay=5) #for cloudflare use this one
        res = scraper.get(url)
        content = res.text
        #content = res.content.decode("utf-8")
        status = res.status_code
    return content, status

def simple_write(file, list_content):
    '''simple_write data to .txt file, with specified strContent'''
    with open(file, "w") as f:
        for line in list_content:
            try:
                f.write("{}".format(line) + "\n")
            except:
                print('could not write: {}'.format(line))
        f.close()
    return True    
    
def get_names_from_url(url):
    content, _ = get_content(url, True)  
    soup = bs.BeautifulSoup(content, 'lxml')
    names = []
    country = soup.title.text.split()[-1].lower()
    print(country)
    #return False
    for line in soup.find_all('tr'):
        name = ''
        sex = ''
        if line.find('a'):
            name = line.find('a').text.replace(" ", "_")
            sex_gif = line.find('img')['src']
            if sex_gif.endswith("gm.png"):
                sex = 'male'
            elif sex_gif.endswith('gf.png'):
                sex = 'female'
            else:
                print("wrong gif name: {}".format(sex_gif))
                continue
        if name and sex:
            #print(name, sex)
            names.append(name + " " + sex)
    return names, country

    
if __name__ == "__main__":
    path = script_path()
    urls = ["http://www.cute-baby-names.com/c/Popular%20names%20in%20Angola",
            "http://www.cute-baby-names.com/c/Popular%20names%20in%20Angola",
            "http://www.cute-baby-names.com/c/Popular%20names%20in%20Angola",
            "http://www.cute-baby-names.com/c/Popular%20names%20in%20Angola",
    ]
    for url in urls:
        names, country = get_names_from_url(url)
        names.insert(0, "names," + country + ",both")
        file_name = country + "_names.txt"
        simple_write(file_name, names)
    
    
    
    
    
    
    