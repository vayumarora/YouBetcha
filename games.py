import MySQLdb
import requests
from bs4 import BeautifulSoup
import re
import datetime
import time


def makeURL(bettingkind,bettingdate):
    #coding for two different kinds of bets
    if bettingkind== 'spreads':
        bettingtypeinURL=""
    elif bettingkind=='totals':
        bettingtypeinURL='totals/'
    url = 'https://www.covers.com/sport/basketball/nba/odds'+bettingtypeinURL+"?date="+bettingdate
    return url

def getTeams(soup):
    firstlevels = soup.find_all('div', class_='cover-CoversOdds-details-Team')
    #general scraping to get the teams
    awayTeams = firstlevels[0].getText().rstrip().replace('\r', '').replace('\n', '')
    homeTeams = firstlevels[1].getText().rstrip().replace('\r', '').replace('\n', '')
    return awayTeams,homeTeams

def getPreviews(soup):
    firstlevels = soup.find_all('div', class_='el-div eventLine-team')


    previewURLS=[]


    for firstlevel in firstlevels:
        #same as above
        secondlevels= firstlevel.find_all('div',class_='eventLine-value')
        for secondlevel in secondlevels:
            thirdlevels= secondlevel.find_all('span',class_='team-name')
            for thirdlevel in thirdlevels:
                for element in thirdlevel:
                    previewURLS.append(element['href'])
    return previewURLS[0],previewURLS[1]

    

def getTimes(soup):
    #general scraping to get the teams
    time = soup.find_all('span', class_='cover-CoversOdds-tableTime')
    t = time[0]
    text= t.getText()
    return text.lstrip()

def getLines(soup):
    firstlevels = soup.find_all('div', class_='covers-CoversOdss-oddsTd--row')
    awayLines = firstlevels[0].getText().rstrip().replace('\r', '').replace('\n', '')
    homeLines = firstlevels[1].getText().rstrip().replace('\r', '').replace('\n', '')
    print(awayLines)
    return awayLines, homeLines

def main():
    #connection to database
    db=MySQLdb.connect("localhost","root","vayum123","finalyoubetchadb")
    totalGames = []
    hello = []
    z=db.cursor()
    todaysdate=datetime.datetime.today()
    x=makeURL("spreads",str(todaysdate.strftime('%Y%m%d')))
    #y=makeURL("totals",str(todaysdate.strftime('%Y%m%d')))
    #gets all the info needed from website
    r = requests.get(x)
    w=str(datetime.datetime.now().date())
    soup = BeautifulSoup(r.text,"html.parser")
    #parses info using soup
    allGames = soup.find_all('table', class_= 'table covers-CoversMatchups-Table covers-CoversOdds-gamelineTable covers-CoversComponents-fixedColumn')
    for g in allGames:
        games = g.find_all('tr', class_='covers-CoversComponents-fixedColumnRow')
        #cut down to today's games only
        for game in games:
            gametime=(getTimes(game))
            awayteam,hometeam=(getTeams(game))
            awayline,homeLines=getLines(game)
            print(awayline,homeLines)
            #print(str(datetime.datetime.now().date()),gametime,hometeam,awayteam,homeline,awayline,gamelink1,gamelink2)
            #insertion into database
            #z.execute("""INSERT into game(sport,date,time,Home_team,Away_team,Home_line,Away_line,Home_preview,Away_preview) values ('NBA',%s,%s,%s,%s,%s,%s,%s,%s)""",(w,[gametime],[hometeam],[awayteam],[homeline],[awayline],[gamelink1],[gamelink2]))
            #db.commit()
        #db.close() 
    return hello   

    





if __name__ == "__main__":
    main()
