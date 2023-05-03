from ids import extract_ids
from ids import generate_links
from scrape1X2 import get_odds_by_bookmaker

# Get matches ids
numberOfMatches = 3
links = generate_links(extract_ids(numberOfMatches))

arbitrage_list = []

for link in links:
    odds_by_bookmaker, max_odds = get_odds_by_bookmaker(link)
    
    #if a match does not have any odds skip
    if not odds_by_bookmaker:
        continue
    print('-------------------------------------------------------------------')
    print('Match Name:', odds_by_bookmaker[0]['match_name'])
    #print('scraped')
    #  print('Link:', link)
    #  for odds in odds_by_bookmaker:
    #      print('Bookmaker:', odds['bookmaker'])
    #      odds_str = ' - '.join(odds['odds']).replace('\n', '  ')
    #      print('Odds:', odds_str)
     
    print()
    print('Max Odds:')
    procent = 0
    for k, v in max_odds.items():
        print(k, '- ', v['bookmaker'], '- Odd:', v['odd'])
        procent += 1/v['odd']
    arbitrage = 100 - 100*procent
    print()
    if arbitrage>5:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('ARBITRAGE=', arbitrage, '%')
    elif arbitrage<0:
        print("No Arbitrage -", arbitrage, "%")
    else:
        print("Arbitrage - ", arbitrage, "%")
    arbitrage_list.append((odds_by_bookmaker[0]['match_name'], arbitrage))

# Print top 5 matches with the highest arbitrage value
arbitrage_list.sort(key=lambda x: x[1], reverse=True)
print('\nTop Matches with the highest Arbitrage:')
for match in arbitrage_list[:7]:
    print(f"{match[0]} - {match[1]}%")
