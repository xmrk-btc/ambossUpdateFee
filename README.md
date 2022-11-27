# Intro

This script sets the fixed fee of your amboss magma offer according to currently estimated fee. In effect, the buyer pays your on-chain fees, so you as a seller may stop worrying about losing either money or reputation when you get an offer while the on-chain fee are too high. (But see the limitations below.)

# Setup

Install python requests. Copy example_config.py to config.py and set the commented variables.
ESTIMATE_FEE_URL - should point to your bitcoind's RPC endpoint, and ESTIMATE_FEE_USER and ESTIMATE_FEE_PASSWORD are used to authenticate.
OFFER_ID - ID of your offer, which is going to have its fixed fee modified
API_KEY - you need to generate it on amboss web page

Run:
```
python3 ambossUpdateFee.py
```


# Limitations

Your UTXOs are not taken into account. If you have many small UTXOs, consider raising TX_SIZE option in the config.py - this is what you expect to be the size of your transaction when opening a channel. To get the tx size if you know number and types of inputs and outputs, you may use https://jlopp.github.io/bitcoin-transaction-size-calculator/ .

There is a race conditionn if you modify your offer with this script and manually on amboss webpage. In other words, one of the changes (yours or the script's) may be lost and not get applied. To avoid this, you may stop the script while modifying your offer manually.
