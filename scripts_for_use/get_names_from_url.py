#script for get names from url
#http://www.cute-baby-names.com
import os
import sys
import requests
import cfscrape
import bs4 as bs
import lxml
import urllib.parse

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

def simple_write(file, list_content, append=False):
    '''simple_write data to .txt file, with specified strContent'''
    if append:
        mode = "a"
    else:
        mode = "w"
    with open(file, mode) as f:
        for line in list_content:
            try:
                f.write("{}".format(line) + "\n")
            except:
                print('could not write: {}'.format(line))
        f.close()
    return True    
    
def get_names_from_url(url):
    if not url:
        return [], ""
    content, status = get_content(url, True)
    soup = bs.BeautifulSoup(content, 'lxml')
    try:
        h2_header = soup.find_all('h2')[0].text
        if h2_header == "Most popular categories":
            print("--< forwarding... probalby no such site: {}".format(url))
            return [], ""
    except:
        pass
    names = []
    country = soup.title.text.split()[-1].lower()
    print("\n" + soup.title.text + " --> " + country)
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
    ask = input("--< is country name ok, for you? (y/n)\n").lower()
    if ask in ("y", ""):
        pass
    else:
        country = input("--< put your own country name:\n")
    return names, country

def get_urls_from_url():
    countries = ['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Argentina', 'Armenia',
                 'Australia', 'Austria', 'Azerbaijan', 'Bangladesh', 'Belgium', 'Bolivia',
                 'Bosnia-Herzegovina', 'Brazil', 'Bulgaria', 'Canada', 'Chile', 'Chili', 'China',
                 'Colombia', 'Costa Rica', 'Croatia', 'Cuba', 'Czech Republic', 'Denmark',
                 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'Finland',
                 'France', 'Germany', 'Great Britain', 'Greece', 'Guatemala', 'Honduras',
                 'Hungary', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy',
                 'Japan', 'Jordan', 'Kosovo', 'Latvia', 'Lebanon', 'Lithuania', 'Macedonia',
                 'Malaysia', 'Mexico', 'Moldova', 'Montenegro', 'Morocco', 'Mozambique',
                 'Netherlands(Holland)', 'Nicaragua', 'Norway', 'Panama', 'Paraguay', 'Peru',
                 'Philippines', 'Poland', 'Portugal', 'Romania', 'Russia', 'Saudi Arabia',
                 'Serbia', 'Slovakia', 'Slovenia', 'South Korea', 'Spain', 'Suriname', 'Sweden',
                 'Switzerland', 'Syria', 'Tanzania', 'Thailand', 'Tunisia', 'Turkey', 'Ukraine',
                 'United States(America)', 'Uruguay', 'Venezuela', 'Vietnam']
    category_url = "http://www.cute-baby-names.com/i/category.php"
    content, _ = get_content(category_url, True)  
    soup = bs.BeautifulSoup(content, 'lxml')
    hrefs = soup.find_all('a', href=True)
    links = [a['href'] for a in hrefs if a['href'].endswith(tuple(countries))]
    base_url = "http://www.cute-baby-names.com"
    urls_list = [urllib.parse.urljoin(base_url, link) for link in links]
    urls_list.sort()
    return urls_list
    
def try_with_urls():
    urls_to_try = ['Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cameroon', 'Cape Verde',
                   'Central African Republic', 'Chad', 'Comoros', '', 'Democratic Republic Of The Congo',
                   'Djibouti', 'Equatorial Guinea', 'Eritrea', 'Gabon', 'Gambia', 'Ghana', 'Guinea-bissau',
                   'Guinea', 'Ivory Coast', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi',
                   'Mali', 'Mauritania', 'Mauritius', 'Mayotte', 'Namibia', 'Niger', 'Republic Of The Congo',
                   'Rwanda', 'Réunion', 'Saint', 'Sao Tome And Principe', 'Senegal', 'Seychelles', 'Sierra Leone',
                   'Somalia', '', 'South Africa', 'South Sudan', 'Sudan', 'Swaziland', 'Tanzania', 'Togo', 'Tunisia',
                   'Uganda', 'Western Sahara', 'Zambia', 'Zimbabwe']
    base_url = "http://www.cute-baby-names.com"
    categories = "/c/Popular names in "
    urls_list = [urllib.parse.urljoin(base_url, categories + link) for link in urls_to_try]
    return urls_list
    
    
if __name__ == "__main__":
    path = script_path()
    urls_list = get_urls_from_url()         #used
    urls_list = try_with_urls()             #used too
    
    for url in urls_list:
        print(url)
        names, country = get_names_from_url(url)
        file_name = country + "_names().txt"
        if os.path.exists(file_name):
            simple_write(file_name, names, append=True)
        else:
            names.insert(0, "names," + country + ",both")       #it may be 2 or 3 sites about 1 country
            simple_write(file_name, names, append=False)
    
    
    
    
    
    
    