from os import stat
from re import U
from unicodedata import category
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import json
import metadata_parser

currentSeason = 2021 #aktuelle Saison(2021 für Saison 2021/2022)
years = list(range(1990,2021))
for year in years:
    print(year)
    #year = input("Choose Year: ") #Input des Jahres, für das die Daten gezogen werden sollen
    followYear = str(int(year) + 1) #Folgejahr berechnen, da es z.B. Saison 2020-2021 ist und das für die URL benötigt wird
    league = "spain"
    #Array mit allen IDs aller Clubs(wird für die URL benötigt)
    clubUrls = [
        # '054efa67', #FC Bayern
        # 'add600ae', #Dortmund
        # 'c7a9f859', #Leverkusen
        # 'acbb6a5b', #RB Leipzig
        # '7a41008f', #Union Berlin
        # 'a486e511', #Freiburg
        # 'bc357bf7', #Köln
        # 'a224b06a', #Mainz
        # '033ea6b8', #Hoffenheim
        # '32f3ee20', #Gladbach
        # 'f0ac8ee6', #Frankfurt
        # '4eaa11d7', #Wolfsburg
        # 'b42c6323', #Bochum
        # '0cdc4311', #Augsburg
        # '598bc722', #Stuttgart
        # '2818f8bc', #Hertha BSC Berlin
        # '247c4b67', #Arminia Bielefeld
        # '12192a4c', #Greuter Fürth
        # 'c539e393', #Schalke
        # '62add3bf', #Werder Bremen
        # 'b1278397', #Düsseldorf
        # 'd9f93f02', #Paderborn
        # '6f2c108c', #Nürnberg
        # '60b5e41f', #Hannover
        # '26790c6a', #Hamburg
        # '6a6967fc', #Darmstadt
        # '12eb2039', #Ingolstadt
        # '8107958d', #Braunschweig
        # 'b1278397', #Düsseldorf
        # '73a27a73', #Kaiserslautern
        # '54864664', #St. Pauli
        # '7675ab36', #Energie Cottbus
        # '33ba9d7b', #Karlsruhe
        # 'bbfd364f', #Duisburg
        # 'bc31a6e4', #Hansa Rostock
        # '3659060d', #AA Achen
        # '2fbdf057', #1860 München
        # 'ba68a0c5', #Unterhaching
        # '291257b3', #Ulm
        # '08610664', #Uerdingen
        # 'ac36c181', #Dresden
        # '473affe3', #Leipzig
        # '6f7db76a', #Wattenscheid
        # 'eb4b278c', #Saarbrücken
        # 'ee8f53af', #Stuttgarter Kickers
        # '89a86c55', #Homburg
        # '151d706e', #Mannheim
        #-------------------------------Bundesliga (alle Vereine ab 1988/89)
        # 'b8fd03ef', #Manchester City
        # '822bd0ba', #Liverpool
        # 'cff3d9bb', #Chelsea
        # '361ca564', #Tottenham Hotspur
        # '18bb7c10', #Arsenal
        # '19538871', #Manchester United
        # '7c21e445', #West Ham United
        # 'a2d435b3', #Leicester City
        # 'd07537b9', #Brighton & Hove Albion
        # '8cec06e1', #Wolverhampton Wanderers
        # 'b2b47a98', #Newcastle United
        # '47c64c55', #Crystel Palace
        # 'cd051869', #Brentford
        # '8602292d', #Aston Villa
        # '33c895d4', #Southampton
        # 'd3fd31cc', #Everton
        # '5bfb9659', #Leeds United
        # '943e8050', #Burnley
        # '2abfe087', #Watford
        # '1c781004', #Norwich-City
        # 'fd962109', #Fulham
        # '60c6b05f', #West Bromwich Albion
        # '1df6b87e', #Sheffield United
        # '4ba7cbea', #Bournemouth
        # '75fae011', #Cardiff City
        # 'f5922ca5', #Huddersfield
        # 'fb10988f', #Swansea City
        # '17892952', #Stoke City
        # '60c6b05f', #West Brom
        # 'bd8769d1', #Hull City
        # '7f59c601', #Middlesbrough
        # '8ef52968', #Sunderland
        # 'a757999c', #Queens Park Rangers
        # 'e59ddc76', #Wigan Athletic
        # 'b0ac61ff', #Reading
        # '8cec06e1', #Wolves
        # 'e090f40b', #Blackburn
        # '445d3104', #Bolton
        # '7cbf5cb4', #Blackpool
        # 'ec79b7c2', #Birmingham City
        # '76ffc013', #Portsmouth
        # '26ab47ee', #Derby County
        # '1df6b87e', #Sheffield United
        # '7a8db6d4', #Charlton Athletic
        # 'b74092de', #Ipswich Town
        # 'f7e3dfe9', #Coventry City
        # '3148d79f', #Bradford City
        # 'bba7d733', #Sheffield Wednesday
        # '3679c494', #Wimbledon
        # 'e4a775cb', #Nottingham Forest
        # '293cb36b', #Barnsley
        # '1df6b87e', #Sheffield United
        # '4a04a02b', #Oldham Athletic
        # '1b295b25', #Swindon Town
        # #---------------------------------------Premier League (alle Vereine ab 1992/93)
        # 'e2d8892c', #Paris-Saint-Germain
        # '5725cc7b', #Marseille
        # 'fd6114db', #Monaco
        # 'b3072e00', #Rennes
        # '132ebc33', #Nice
        # 'c0d3eab4', #Strasbourg
        # 'fd4e0f7d', #Lens
        # 'd53c0b06', #Lyon
        # 'd7a486cd', #Nantes
        # 'cb188c0c', #Lille
        # 'fb08dbb3', #Brest
        # '7fdd64e0', #Reims
        # '281b0e73', #Montpellier
        # '69236f98', #Angers
        # '54195385', #Troyes
        # 'd2c87802', #Lorient
        # 'd9676424', #Clermont-Foot
        # 'd298ef2c', #Saint-Etienne
        # 'f83960ae', #Metz
        # '123f3efe', #Bordeaux
        # '1cbf5f9e', #Nimes
        # '8dfb7350', #Dijon
        # '25622401', #Amiens
        # '3f8c4b5f', #Toulouse
        # '74229020', #Caen
        # 'd41b5f53', #Guingamp
        # 'e88fc6e5', #Nancy
        # '6283be2c', #Bastia
        # '73905dde', #Gazelec Ajaccio
        # '633fbb6e', #Evian
        # 'b9cd3c9a', #Sochaux
        # '259d3345', #Valenciennes
        # '7a54bb4f', #Ajaccio
        # '5ae09109', #Auxerre
        # 'e95faa7f', #Arles-Avignon
        # 'cd5d7aa6', #Le Mans
        # '98973a5c', #Boulogne
        # '40aa7280', #Grenoble
        # '5c2737db', #Le Havre
        # 'e4e952b9', #Sedan
        # '70f96e85', #Istres
        # '43d17b20', #Chateauroux
        # '69a82db6', #AS Cannes
        # '5dca7789', #Gueugnon
        # '82e8a66d', #FC Martigues
        # #--------------------------------------Ligue 1 (alle Vereine ab 1995/96)
        # 'dc56fe14', #Milan
        # 'd609edc0', #Internazionale
        # 'd48ad4ff', #Napoli
        # 'e0652b02', #Juventus
        # '7213da33', #Lazio
        # 'cf74a709', #Roma
        # '421387cf', #Fiorentina
        # '922493f3', #Atalanta
        # '0e72edf2', #Hellas-Verona
        # '105360fe', #Torino
        # 'e2befd26', #Sassuolo
        # '04eea015', #Udinese
        # '1d8099f8', #Bologna
        # 'a3d88bd8', #Empoli
        # '8ff9e3b3', #Sampdoria
        # '68449f6d', #Spezia
        # 'c5577084', #Salernitana
        # 'c4260e09', #Cagliari
        # '658bf2de', #Genoa
        # 'af5d5982', #Venezia
        # '4fcb34fd', #Benevento
        # '3074d7b1', #Crotone
        # 'eab4234c', #Parma
        # 'ffcbe334', #Lecce
        # '4ef57aeb', #Brescia
        # '1d2fe027', #SPAL
        # 'a3d88bd8', #Empoli
        # '6a7ad59d', #Frosinone
        # 'cc919b35', #Chievo
        # '3074d7b1', #Crotone
        # 'ee058a17', #Palermo
        # 'b985784c', #Pescara
        # '71f07916', #Carpi
        # '6a7ad59d', #Frosinone
        # '283f2557', #Cesena
        # '7b046f08', #Catania
        # '939201df', #Livorno
        # '45a2f824', #Siena
        # 'ffcbe334', #Lecce
        # '6c37111f', #Novara
        # '4ef57aeb', #Brescia
        # '01baa639', #Bari
        # '46f8c29f', #Reggina
        # '72c031e3', #Ascoli
        # 'fe2dc36d', #Messina
        # 'f71ec3ae', #Treviso
        # '37cba288', #Perugia
        # '71a3700b', #Modena
        # '1d2f81d0', #Ancona
        # '72c031e3', #Ascoli
        # 'fe2dc36d', #Messina
        # '28c9c3cd', #Como
        # '81e923a1', #Piacenza
        # #-------------------------------------Serie A (alle Vereine ab 1994/95)
        '53a2f082', #Real Madrid
        '206d90db', #Bracelona
        'db3b9613', #Athletico
        'ad2be733', #Sevilla
        'fc536746', #Real Betis
        'e31d1cd9', #Real Sociedad
        '2a8183b3', #Villareal
        '2b390eca', #Athelic Club Bilbao
        'dcc91a7b', #Valencia
        '03c57e2b', #Osasuna
        'f25da7fb', #Celta Vigo
        '98e8af82', #Rayo Vallecano
        '6c8b07df', #Elche
        'a8661628', #Espanyol Barcelona
        '7848bd64', #Getafe
        '2aa12281', #Mallorca
        'ee7c297c', #Cadiz
        'a0435291', #Granada
        '9800b6a1', #Levante
        '8d6fd021', #Alaves
        'c6c493e6', #Huesca
        '17859612', #Valladolid
        'bea5c710', #Eibar
        '7c6f2c78', #Leganes
        '9024a00a', #Girona
        '2a60ed82', #Deportivo La Coruna
        '0049d422', #Las Palmas
        '1c896955', #Malaga
        'bb9efd50', #Sporting Gijon
        '78ecf4bb', #Almeria
        '6009ff35', #Cordoba
        '800303a0', #Zaragoza
        'dee3bbc8', #Racing Santander
        '4222a514', #Hercules
        'c653e8bf', #Xerez
        '27cc9c62', #Tenerife
        '76d8bafa', #Numancia
        '6e1d6d95', #Recreativo
        'ab0dc306', #Real Murcia
        'd5de8ff3', #Gimnastic
        'b7e3e46e', #Albacete
        'ab358912', #Oviedo
        'be3375e1', #Extremadura
        'c32656d6', #Salamanca
        '819b92aa', #CP Merida
        '63505675' #Compostela
        # #--------------------------------------La Liga (alle Vereine ab 1997/98)
    ]
    data = [] #Array, in das die Daten reingeschrieben werden


    root = 'https://fbref.com/en/squads' #Grund-URL
    url_piece = '/' + str(year) + '-' + followYear #URL-Teil mit Jahresangaben für die Sasion

    if year == currentSeason: #für die aktuelle Saison muss einen andere URL verwendet werden als für vergangene Saisions
        url = root + '/' + clubUrls[0] #URL für den ersten Club des ClubURL Arrays erstellen
    else: url = root + '/' + clubUrls[0] + url_piece

    headers = [] #Array für die Headers der Tabelle


    #HTML der Website ziehen und damit Soup-Objekt erstellen
    response = requests.get(url)
    webpage = response.content
    soup = BeautifulSoup(webpage, "html.parser")

    #alle Reihen finden, die im Table-Header stehen
    rows = soup.find('thead')('tr')

    row = rows[1]  #nur normaler Header und nicht Over-Header

    for tag in row: #über die Tags des Headers iterieren
        if tag.name == 'th': #Falls das Tag 'th' ist, ist das richtige Tag gefunden, das die Zeilenüberschrift enthält
            headers.append(tag.get_text().strip()) #den Text des Tags an das Array für die Header anhängen


    #Metadaten der Website in JSON-Datei speichern
    page=metadata_parser.MetadataParser(url)
    pagedata=page.metadata
    meta=json.dumps(pagedata)
    with open(f'soccer-{league}-Players-' + str(year) + '-' + followYear + '-Metadata.json','w') as f:
        f.write(meta)


    for clubUrl in clubUrls: #über alle ClubIDs im Array iterieren

        root = 'https://fbref.com/en/squads' #Grund-URL
        url_piece = '/' + str(year) + '-' + followYear #URL-Teil mit Jahresangaben für die Sasion


        if year == 2021: #für die aktuelle Saison muss einen andere URL verwendet werden als für vergangene Saisions
            url = root + '/' + clubUrl
        else: url = root + '/' + clubUrl + url_piece


        print("Attempting to send a request to this url:",url)

        print(url)

        #HTML der Website ziehen und damit Soup-Objekt erstellen
        response = requests.get(url)
        webpage = response.content
        soup = BeautifulSoup(webpage, "html.parser")

        #den Tabellen-Body der Tabelle finden(Tabellen haben unterschiedliche IDs und Klassen, deswegen kann die Tabelle nicht anhand davon gefunden werden,
        # aber es gibt nur eine Tabelle auf der Seite, deswegen kann einfach danach gesucht werden)
        table = soup.find('tbody')


        if table: #nur, falls die Tabelle auch gefunden wurde(Für manche Clubs gibt es nicht alle Saisons)
            rows = table('tr') #alle Reihen der Tabelle suchen

            for row in rows: #über alle Reihen der Tabelle iterieren
                cur_row = [] #Array für die aktuelle Zeile der Tabelle
                for tag in row: #über die Tags in einer einzelnen Reihe iterieren
                    if tag.name == 'td' or tag.name == 'th': #Falls das Tag 'td' oder 'th' ist, ist das richtige Tag gefunden, das den Inhalt einer Spalte in der aktuellen Zeile enthält (Die Namen der Spieler werden als 'th' deklariert)
                        if tag.get_text().strip() != 'Matches': #Nur wenn der Tag nicht den String Matches enthält sollen die Daten angefügt werden, damit die letzte Zeile der Tabelle weggelassen wird (in dieser Zeile sind die Matches der Spieler verlinkt)
                            cur_row.append(tag.get_text().strip()) #den Text des Tags an das Array für die aktuelle Spalte anhängen
                        else: cur_row.append('') #wenn der Text Matches ist, dann einfach einen leeren String anhängen
                if cur_row: #nur die Daten hinzufügen, wenn die aktuelle Spalte auch Daten enthält
                    data.append(cur_row) #aktuelle Spalte an das Array für die Tabellenzeilen anhängen
        
        time.sleep(2) #3 Sekunden pausieren, um zu verhindern, von der Seite blockiert zu werden
        

    #Stats in Dataframe konvertieren
    stats = pd.DataFrame(data, columns = headers)
    print(stats)
    stats.drop('Matches', inplace=True, axis=1)

    #Dataframe in CSV-Datei speichern
    stats.to_csv(f'soccer-{league}-Players-' + str(year) + '-' + followYear + '.csv',index=False)
