# Paypal
currency = "USD"

# Cogs
cogs = ["bets", "cog_manager", "currency", "tournament"]

# Database
database_name = "duelbot"

# Payouts
payoutEmailSubject = "P2P Duel Bot Withdrawal"
payoutEmailMessage = "{0} {1} deposited into {2}"
payoutNote = ""
tokenUrl = ["https://api.sandbox.paypal.com/v1/oauth2/token"][0]
payoutUrl = ['https://api-m.sandbox.paypal.com/v1/payments/payouts'][0]
payoutCurrency = currency
minimumPayout = 5

# Deposit
minimumDeposit = 5
depositLink = "https://paypal.me/MortalMoth/{0}{1}"
depositCurrency = currency