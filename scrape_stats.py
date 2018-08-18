import csv
import time
from random import randint
from bs4 import BeautifulSoup
import requests

wl, pdiff, mov, sos, offr, defr = ([] for i in range(6))
wl_dict, pdiff_dict, mov_dict, sos_dict, offr_dict, defr_dict = ({} for j in range(6))

def get_afc_stats(soup, y):
    afc_dict = {}
    try:
        total = soup.find(attrs={"id":"all_AFC"})
        second = total.find(class_='overthrow table_container')
        table = second.find('tbody')
        info = table.find_all('tr')
        counter = 0
        for i in info:
            if counter == 0 or counter%5 == 0:
                counter += 1
                continue
            team_name = i.find('a').text
            playoff = i.find('th')
            divisional = False
            playoffs = False
            try:
                if str(playoff.contents[1]) == '*':
                    divisional = True
                    playoffs = True
                if str(playoff.contents[1]) == '+':
                    playoffs = True
            except IndexError:
                divisional = False
                playoffs = False
            more_info = i.find_all('td')
            afc_dict[team_name] = {}
            afc_dict[team_name]['Team Name'] = team_name
            afc_dict[team_name]['Playoffs'] = playoffs
            afc_dict[team_name]['Divisional'] = divisional
            for more in more_info:
                if more['data-stat'] == 'win_loss_perc':
                    try:
                        wl_dict[float(more.text)].append(team_name)
                    except KeyError:
                        wl_dict[float(more.text)] = [team_name]
                    wl.append(float(more.text))
                elif str(more['data-stat']) == 'sos_total':
                    try:
                        sos_dict[float(more.text)].append(team_name)
                    except KeyError:
                        sos_dict[float(more.text)] = [team_name]
                    sos.append(float(more.text))
                elif str(more['data-stat']) == 'mov':
                    try:
                        mov_dict[float(more.text)].append(team_name)
                    except KeyError:
                        mov_dict[float(more.text)] = [team_name]
                    mov.append(float(more.text))
                elif str(more['data-stat']) == 'points_diff':
                    try:
                        pdiff_dict[int(more.text)].append(team_name)
                    except KeyError:
                        pdiff_dict[int(more.text)] = [team_name]
                    pdiff.append(int(more.text))
                elif str(more['data-stat']) == 'srs_offense':
                    try:
                        offr_dict[float(more.text)].append(team_name)
                    except KeyError:
                        offr_dict[float(more.text)] = [team_name]
                    offr.append(float(more.text))
                elif str(more['data-stat']) == 'srs_defense':
                    try:
                        defr_dict[float(more.text)].append(team_name)
                    except KeyError:
                        defr_dict[float(more.text)] = [team_name]
                    defr.append(float(more.text))
            counter += 1
    except Exception as e:
        print(repr(e))
        print('Error on year {}'.format(y))
    return afc_dict

def get_nfc_stats(soup, y):
    nfc_dict = {}
    try:
        total = soup.find(attrs={"id":"all_NFC"})
        second = total.find(class_='overthrow table_container')
        table = second.find('tbody')
        info = table.find_all('tr')
        counter = 0
        for i in info:
            if counter == 0 or counter%5 == 0:
                counter += 1
                continue
            team_name = i.find('a').text
            playoff = i.find('th')
            divisional = False
            playoffs = False
            try:
                if str(playoff.contents[1]) == '*':
                    divisional = True
                    playoffs = True
                if str(playoff.contents[1]) == '+':
                    playoffs = True
            except IndexError:
                divisional = False
                playoffs = False
            more_info = i.find_all('td')
            nfc_dict[team_name] = {}
            nfc_dict[team_name]['Team Name'] = team_name
            nfc_dict[team_name]['Playoffs'] = playoffs
            nfc_dict[team_name]['Divisional'] = divisional
            for more in more_info:
                if more['data-stat'] == 'win_loss_perc':
                    try:
                        wl_dict[float(more.text)].append(team_name)
                    except KeyError:
                        wl_dict[float(more.text)] = [team_name]
                    wl.append(float(more.text))
                elif str(more['data-stat']) == 'sos_total':
                    try:
                        sos_dict[float(more.text)].append(team_name)
                    except KeyError:
                        sos_dict[float(more.text)] = [team_name]
                    sos.append(float(more.text))
                elif str(more['data-stat']) == 'mov':
                    try:
                        mov_dict[float(more.text)].append(team_name)
                    except KeyError:
                        mov_dict[float(more.text)] = [team_name]
                    mov.append(float(more.text))
                elif str(more['data-stat']) == 'points_diff':
                    try:
                        pdiff_dict[int(more.text)].append(team_name)
                    except KeyError:
                        pdiff_dict[int(more.text)] = [team_name]
                    pdiff.append(int(more.text))
                elif str(more['data-stat']) == 'srs_offense':
                    try:
                        offr_dict[float(more.text)].append(team_name)
                    except KeyError:
                        offr_dict[float(more.text)] = [team_name]
                    offr.append(float(more.text))
                elif str(more['data-stat']) == 'srs_defense':
                    try:
                        defr_dict[float(more.text)].append(team_name)
                    except KeyError:
                        defr_dict[float(more.text)] = [team_name]
                    defr.append(float(more.text))
            counter += 1
    except Exception as e:
        print(repr(e))
        print('Error on year {}'.format(y))
    return nfc_dict

def sort_all():
    wl.sort()
    pdiff.sort()
    mov.sort()
    sos.sort()
    offr.sort()
    defr.sort()

def clear_all():
    wl.clear()
    pdiff.clear()
    mov.clear()
    sos.clear()
    offr.clear()
    defr.clear()
    wl_dict.clear()
    pdiff_dict.clear()
    mov_dict.clear()
    sos_dict.clear()
    offr_dict.clear()
    defr_dict.clear()

def rank_wl(nfl_dict):
    counter = 1
    prev = None
    for stat in wl:
        if stat == prev:
            counter += 1
            continue
        if len(wl_dict[stat]) > 1:
            if stat == wl[len(wl) -1]:
                for team in wl_dict[stat]:
                    nfl_dict[team]['W/L%'] = 32
                break
            for team in wl_dict[stat]:
                nfl_dict[team]['W/L%'] = counter
        else:
            nfl_dict[wl_dict[stat][0]]['W/L%'] = counter
        counter += 1
        prev = stat

def rank_pdiff(nfl_dict):
    counter = 1
    prev = None
    for stat in pdiff:
        if stat == prev:
            counter += 1
            continue
        if len(pdiff_dict[stat]) > 1:
            if stat == pdiff[len(pdiff) -1]:
                for team in pdiff_dict[stat]:
                    nfl_dict[team]['Points Diff'] = 32
                break
            for team in pdiff_dict[stat]:
                nfl_dict[team]['Points Diff'] = counter
        else:
            nfl_dict[pdiff_dict[stat][0]]['Points Diff'] = counter
        counter += 1
        prev = stat

def rank_mov(nfl_dict):
    counter = 1
    prev = None
    for stat in mov:
        if stat == prev:
            counter += 1
            continue
        if len(mov_dict[stat]) > 1:
            if stat == mov[len(mov) -1]:
                for team in mov_dict[stat]:
                    nfl_dict[team]['Margin of Victory'] = 32
                break
            for team in mov_dict[stat]:
                nfl_dict[team]['Margin of Victory'] = counter
        else:
            nfl_dict[mov_dict[stat][0]]['Margin of Victory'] = counter
        counter += 1
        prev = stat

def rank_sos(nfl_dict):
    counter = 1
    prev = None
    for stat in sos:
        if stat == prev:
            counter += 1
            continue
        if len(sos_dict[stat]) > 1:
            if stat == sos[len(sos) -1]:
                for team in sos_dict[stat]:
                    nfl_dict[team]['Schedule Strength'] = 32
                break
            for team in sos_dict[stat]:
                nfl_dict[team]['Schedule Strength'] = counter
        else:
            nfl_dict[sos_dict[stat][0]]['Schedule Strength'] = counter
        counter += 1
        prev = stat

def rank_offr(nfl_dict):
    counter = 1
    prev = None
    for stat in offr:
        if stat == prev:
            counter += 1
            continue
        if len(offr_dict[stat]) > 1:
            if stat == offr[len(offr) -1]:
                for team in offr_dict[stat]:
                    nfl_dict[team]['Offense Rating'] = 32
                break
            for team in offr_dict[stat]:
                nfl_dict[team]['Offense Rating'] = counter
        else:
            nfl_dict[offr_dict[stat][0]]['Offense Rating'] = counter
        counter += 1
        prev = stat

def rank_defr(nfl_dict):
    counter = 1
    prev = None
    for stat in defr:
        if stat == prev:
            counter += 1
            continue
        if len(defr_dict[stat]) > 1:
            if stat == defr[len(defr) -1]:
                for team in defr_dict[stat]:
                    nfl_dict[team]['Defense Rating'] = 32
                break
            for team in defr_dict[stat]:
                nfl_dict[team]['Defense Rating'] = counter
        else:
            nfl_dict[defr_dict[stat][0]]['Defense Rating'] = counter
        counter += 1
        prev = stat

def organize(nfl):
    #create seperate organizers
    rank_wl(nfl)
    rank_pdiff(nfl)
    rank_mov(nfl)
    rank_sos(nfl)
    rank_offr(nfl)
    rank_defr(nfl)

if __name__ == "__main__":
    header = ['Team Name', 'W/L%', 'Points Diff', 'Margin of Victory', 'Schedule Strength', 'Offense Rating',
              'Defense Rating', 'Playoffs', 'Divisional']    
    with open('raw_stats.csv', 'a') as stats_file:
        stats_writer = csv.DictWriter(stats_file, fieldnames=header, restval='', extrasaction='ignore')
        stats_writer.writeheader()
        for year in range(2005, 2018):
            url = 'https://www.pro-football-reference.com/years/{}/index.htm'.format(year)
            req = requests.Session()
            page = req.get(url)
            bsoup = BeautifulSoup(page.text, 'html.parser')
            stats_writer.writerow({'Team Name' : 'Year: ' + str(year)})
            clear_all()
            d1 = get_afc_stats(bsoup, year)
            d2 = get_nfc_stats(bsoup, year)
            total = d1.copy()
            total.update(d2)
            sort_all()
            organize(total)
            for k, v in total.items():
                stats_writer.writerow({name: total[k].get(name) for name in header})
            time.sleep(randint(10, 15))
