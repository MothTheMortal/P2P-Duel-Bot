import re


# Auxiliary Functions
def checkEmail(email):
    emailFormat = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(emailFormat, email):
        return True
    else:
        return False

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


# IPN Listener

ipnURL = ['https://ipnpb.sandbox.paypal.com/cgi-bin/webscr', "https://ipnpb.paypal.com/cgi-bin/webscr"][0]


# Color Codes
errorColor = 0xFF0000
successColor = 0x00FF00


access_token = "A21AALMUGvvou4QbtVvCmynp_KyvwVZff11xraXm06SEgAI8mmlVFE7ho79Ypp1y8TNcyCLSzkEgs-oMHqf7bGavw9UKtVbQw"