from utils.get_info import today, yesterday, business_date


todays = today(format='%b %Y')
yesterdays = yesterday(format='%b %Y')
business_dates = business_date(format='%b %Y')

print(f'hoje: {todays} | ontem: {yesterdays} | data online: {business_dates}')