from flask import Flask, request, make_response
import json
import os
from flask_cors import cross_origin

from covidDetails.covidDetails import covidDetails
from logger import logger

chat = Flask(__name__)




# geting and sending response to dialogflow
@chat.route('/webChat', methods=['POST'])
@cross_origin()
def webChat():

    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r



# processing the request from dialogflow
def processRequest(req):
    log = logger.Log()


    result = req.get("queryResult")
    parameters = result.get("parameters")
    entity = parameters.get("geo-country")

   #entity=result.get("intent").get('displayName')

    cov = covidDetails
    fulfillmenttext = cov.getTotalCountByCountry(entity, "All")
    return {
        "fulfillmentText": fulfillmenttext
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    chat.run(debug=False, port=port, host='0.0.0.0')
