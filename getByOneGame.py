from scrape1X2 import get_odds_by_bookmaker

link = f'https://www.flashscore.ro/meci/2uZhA6kg/#/comparare-cote/cote-1x2/final'

odds_by_bookmaker, max_odds = get_odds_by_bookmaker(link)
print('-------------------------------------------------------------------')

print('Match Name:', odds_by_bookmaker[0]['match_name'])
print('Link:', link)
for odds in odds_by_bookmaker:
    print('Bookmaker:', odds['bookmaker'])
    odds_str = ' - '.join(odds['odds']).replace('\n', '  ')
    print('Odds:', odds_str)
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
else:
    print('LOW ARBITRAGE - ', arbitrage, '%')