import csv
import pandas
import collections

def calculate_score(win_loss, points_diff, sos, off_rate, def_rate, poff, div):
    if not poff:
        return 0
    else:
        if div:
            return (2*win_loss + 5*points_diff + 3*sos + off_rate + 4*def_rate) + 100
        else:
            return (2*win_loss + 5*points_diff + 3*sos + off_rate + 4*def_rate)

if __name__ == '__main__':
    df = pandas.read_csv('raw_stats.csv')
    total = {}
    headers = []
    full = False
    for index, row in df.iterrows():
        if index%33 == 0:
            current_year = row['Team Name']
            total[current_year] = {}# Team Name here is the year
            total[current_year]['Year'] = int(current_year[6:])
            if index != 0:
                full = True
        else:
            score = calculate_score(int(row['W/L%']), int(row['Points Diff']), int(row['Schedule Strength']), int(row['Offense Rating']),
                                    int(row['Defense Rating']), row['Playoffs'], row['Divisional'])
            total[current_year][row['Team Name']] = score
            if not full:
                headers.append(row['Team Name'])
    headers.insert(0, 'Year')
    ordered_total = collections.OrderedDict(sorted(total.items()))
    with open('weighted_stats.csv', 'a') as weighted_file:
        weighted_writer = csv.DictWriter(weighted_file, fieldnames=headers, restval='', extrasaction='ignore')
        weighted_writer.writeheader()
        for k, v in ordered_total.items():
            if int(k[6:]) >= 2016:
                headers[16] = 'Los Angeles Rams'
                weighted_writer.writerow({name: ordered_total[k].get(name) for name in headers})
            else:
                weighted_writer.writerow({name: ordered_total[k].get(name) for name in headers})
        
    #team_name
    #writerow ({name: total[name].get(team_name)
    #perhaps iterate over the team names?
    #Hardcode
    #{Year: year, team_name: score that year}
    #Change headers to make it each team
    #Add year as a key value in the nested dictionary
    #writedict{name:get(name) for name in headers} essentially only accessing the inner dict while looping over the outer dict like in scrape_web CloudBrain
    #MAKE SURE TEAM NAME IN HEADERS IS THE SAME AS row['Team Name']
