## Must set the following commented variables

# bitcoind RPC endpoint to query for fee estimate
#ESTIMATE_FEE_URL="http://127.0.0.1:8332/"

# user and password to connect to the above bitcoind RPC endpoint
#ESTIMATE_FEE_USER=""
#ESTIMATE_FEE_PASSWORD=""

# ID of your amboss offer to modify
#OFFER_ID=""

# your Amboss API key
#API_KEY=""


#########
# You may change the following, but the defaults should be reasonable

# tx size in vB to use to compute the total tx fee
TX_SIZE=170
# the amboss base_fee is only updated if the change is larger than this (in sats)
MIN_FEE_CHANGE=5
# in seconds; how long to wait between two successive attempts to update amboss fee
UPDATE_INTERVAL=60
# fee is estimated for tx to be included with delay of this many blocks
ESTIMATE_FEE_BLOCKS=2


