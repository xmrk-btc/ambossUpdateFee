import requests
import time

from config import *


#####

URL="https://api.amboss.space/graphql"

GET_OFFER_JSON={
"query": """
   query GetOffer($getOfferId: String!) {
      getOffer(id: $getOfferId) {
    account
    amboss_fee_rate
    base_fee
    base_fee_cap
    fee_rate
    fee_rate_cap
    id
    max_size
    min_block_length
    min_size
    offer_type
    orders {
      locked_size
    }
    seller_score
    side
    status
    tags {
      name
    }
    total_size 
      }
   }""",
"variables": {"getOfferId": OFFER_ID}
}

UPDATE_OFFER_JSON = {
    "query": """
    mutation UpdateOffer($input: UpdateOffer!) {
      updateOffer(input: $input)
      }""",
    "variables": {
        "input": {
        }
    }
}

""" Returns estimated fee for ESTIMATE_FEE_BLOCKS, in sats/vB, as float"""
def estimateFee():
    data = '{"jsonrpc": "1.0", "id": "curltest", "method": "estimatesmartfee", "params": [%d, "ECONOMICAL"]}' % (ESTIMATE_FEE_BLOCKS,)
    auth = (ESTIMATE_FEE_USER, ESTIMATE_FEE_PASSWORD)
    r=requests.post(ESTIMATE_FEE_URL, data=data, auth=auth); 
    result = r.json()['result']['feerate']*1E8/1024
    return result
    



# example response to getoffer:
#  {"data":{"getOffer":{"account":"033878501f9a4ce97dba9a6bba4e540eca46cb129a322eb98ea1749ed18ab67735","amboss_fee_rate":1000,"base_fee":300,"base_fee_cap":0,"fee_rate":1500,"fee_rate_cap":25,"id":"2d251c3b-3b19-4224-ab18-9e513a3b8798","max_size":"8000000","min_block_length":8700,"min_size":"500000","offer_type":"CHANNEL","orders":{"locked_size":"22000000"},"seller_score":"82.92","side":"SELL","status":"DISABLED","tags":[{"name":"fastest"}],"total_size":"37000000"}}}


UPDATE_FIELDS=["base_fee", "base_fee_cap", "fee_rate", "max_size", "fee_rate_cap", "min_block_length", "min_size", "total_size" ]


def main():
    currentBaseFee = None

    while True:
        try:
            fee = estimateFee()
            print("Estimated fee in sat/vB: %f" % (fee, ))

            newBaseFee = TX_SIZE * fee
            if currentBaseFee is not None and abs(newBaseFee - currentBaseFee) < MIN_FEE_CHANGE:
                print("Not changing, fee change would be less than %d" % (MIN_FEE_CHANGE, ))
            else:
                headers = { "Content-Type": "application/json", "Authorization": "Bearer " + API_KEY}
                r = requests.post(URL, headers=headers, json = GET_OFFER_JSON)
                print(r.text)
                offerData = r.json()["data"]["getOffer"]

                offerData["base_fee"] = TX_SIZE * fee
                currentBaseFee = offerData["base_fee"]
              
                for field in UPDATE_FIELDS:
                    # only offer id is not int, so convert everything else to int
                    UPDATE_OFFER_JSON["variables"]["input"][field] = int(offerData[field])

                UPDATE_OFFER_JSON["variables"]["input"]["offer"] = OFFER_ID

                r = requests.post(URL, headers=headers, json = UPDATE_OFFER_JSON)
                print(r.text)
                print(r.request.body)
        except:
            pass

        time.sleep(UPDATE_INTERVAL)
        

if __name__ == "__main__":
    main()
