import requests
from bs4 import BeautifulSoup as bs
from urllib.request import Request,urlopen


class Scrapper:
    def __init__(self):
        self.poke_data={}
        self.name = "Bulbasaur"
    
    def scrape_data(self,name):
        preprocessed_name = name.replace('.','').replace(' ','-').replace('\xe9','e')
        url = f"https://pokemondb.net/pokedex/{preprocessed_name}"
        site = Request(url, headers={"User-Agent": "Mozilla/5.0"})

        urlclient = urlopen(site).read()
        self.html = bs(urlclient,"html.parser")
        forms = self.html.find_all("div",{"class":"sv-tabs-tab-list"})[0].find_all("a")
        form = 0
        images = self.html.find_all("img",{"fetchpriority":"high"})[1:]
        self.poke_data['image_link'] = images[form]['src'].strip('\n')
        self.poke_data['name'] = name

        self.dex()

        self.training()

        self.breeding()
        self.base_stats()
        self.dex_entry()

        return self.poke_data


    def dex(self):
        #Pokédex data
        table = self.html.find("h2",string="Pokédex data").find_next("table",{"class":"vitals-table"})

        tds = table.find_all("td")
        self.poke_data["index"] = '#'+tds[0].text
        self.poke_data['types']=[]
        for a in tds[1].find_all("a"):
            self.poke_data['types'].append(a.text.strip('\n'))
        
        if len(self.poke_data['types'])==0:
            self.poke_data['types'].append('???')


        self.poke_data['species'] = tds[2].text.strip('\n')
        ht = tds[3].text.strip('\n')
        self.poke_data['ht'] = ht[:ht.index('m')+1]
        wt = tds[4].text.strip('\n')
        self.poke_data['wt'] = wt[:wt.index('g')+1]
        self.poke_data['abilities']=[]
        for a in tds[5].find_all('a'):
            name = a.text.strip('\n')
            desc = a['title']
            self.poke_data['abilities'].append({name:desc})


    def training(self):
        try:
            #Training
            table = self.html.find("h2",string="Training").find_next("table",{"class":"vitals-table"})
            tds = table.find_all("td")
            self.poke_data['catch rate'] = tds[1].text.strip('\n')
            self.poke_data['catch rate'] = self.poke_data['catch rate'][:self.poke_data['catch rate'].index('(')]
            self.poke_data['happiness'] = tds[2].text.strip('\n')
            self.poke_data['happiness'] = self.poke_data['happiness'][:self.poke_data['happiness'].index('(')]
            self.poke_data['base exp'] = tds[3].text.strip('\n')
            self.poke_data['growth rate'] = tds[4].text.strip('\n')
        except:
            pass

    def breeding(self):
        #Breeding
        try:
            table = self.html.find("h2",string="Breeding").find_next("table",{"class":"vitals-table"})
            tds = table.find_all("td")
            self.poke_data['egg group'] = tds[0].text.strip('\n')
            self.poke_data['gender ratio']=[]
            for span in tds[1].find_all('span'):
                ratio = span.text.strip('\n')
                self.poke_data['gender ratio'].append(ratio[:ratio.find('%')])

            self.poke_data['egg cycles'] = tds[2].text.strip('\n')
            self.poke_data['egg cycles'] = self.poke_data['egg cycles'][:self.poke_data['egg cycles'].index('(')]
        except:
            pass

    def base_stats(self):
        #Base Stats
        try:
            table = self.html.find("h2",string="Base stats").find_next("table",{"class":"vitals-table"})
            tds = table.find_all("td")
            self.poke_data['hp'] = tds[0].text.strip('\n')
            self.poke_data['atk'] = tds[4].text.strip('\n')
            self.poke_data['def'] = tds[8].text.strip('\n')
            self.poke_data['sp.atk'] = tds[12].text.strip('\n')
            self.poke_data['sp.def'] = tds[16].text.strip('\n')
            self.poke_data['speed'] = tds[20].text.strip('\n')
            self.poke_data['total'] = tds[24].text.strip('\n')
        except:
            pass
    

    def dex_entry(self):
        #Dex Entries
        try:
            table = self.html.find("h2",string="Pokédex entries").find_next("table",{"class":"vitals-table"})
            tds = table.find_all('td')
            self.poke_data['desc'] = tds[-1].text.strip('\n')
        except:
            pass
    
