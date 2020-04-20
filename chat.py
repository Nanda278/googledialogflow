from flask import Flask, request, make_response
import json
import os
from flask_cors import cross_origin

from covidDetails.covidDetails import covidDetails
from logger.logger import Log

chat = Flask(__name__)




# geting and sending response to dialogflow
@chat.route('/webChat', methods=['POST'])
#@cross_origin()
def webChat():

    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)
    print(res)
    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r



# processing the request from dialogflow
def processRequest(req):
    log = Log()
    sessionid = req.get("session").split("/")[4]
    result = req.get("queryResult")
    userText = result.get("queryText")
    log.write_log_to_db(sessionid,userText)
    parameters = result.get("parameters")
    cov = covidDetails()

    intent = result.get("intent").get('displayName')
    fulfillmenttext = "Sorry I could not understand.. Could you be bit meaningful.."
    try:
        if(intent=="total_cases"):
            entity = parameters.get("geo-country")
            fulfillmenttext = cov.getTotalCountByCountry(entity, "All")
            log.write_log_to_db(sessionid, str(fulfillmenttext))
            return cov.formResponseValueTextAndImage(fulfillmenttext)
        elif(intent == "pincode_cases"):
            entity = str(round(parameters['number']))
            fulfillmenttext = cov.getCountryNameFromPincode(entity)
            log.write_log_to_db(sessionid, str(fulfillmenttext))
            return cov.formResponseValueTextAndImage(fulfillmenttext)
        elif (intent == "recovered_cases"):
            entity = parameters.get("geo-country")
            fulfillmenttext = cov.getTotalCountByCountry(entity, "recovered")
            log.write_log_to_db(sessionid, str(fulfillmenttext))
            return cov.formResponseValueTextAndImage(fulfillmenttext)
        elif (intent == "death_cases"):
            entity = parameters.get("geo-country")
            fulfillmenttext = cov.getTotalCountByCountry(entity, "deaths")
            log.write_log_to_db(sessionid, str(fulfillmenttext))
            return cov.formResponseValueTextAndImage(fulfillmenttext)
        elif (intent == "confirmed_cases"):
            entity = parameters.get("geo-country")
            fulfillmenttext = cov.getTotalCountByCountry(entity, "confirmed")
            log.write_log_to_db(sessionid, str(fulfillmenttext))
            return cov.formResponseValueTextAndImage(fulfillmenttext)
        elif (intent == "more_recovered_cases"):
            entity = str(1) if (not "count" in parameters) else str(parameters.get("count"))
            fulfillmenttext = cov.getTopCountyCases(entity,"DESC","most_recovered_cases")
            log.write_log_to_db(sessionid, str(fulfillmenttext))
            return cov.formResponseValueText(fulfillmenttext)
        elif (intent == "less_recovered_cases"):
            entity = str(1) if (not "count" in parameters) else str(round(parameters.get("count")))
            fulfillmenttext = cov.getTopCountyCases(entity,"ASC","less_recovered_cases")
            log.write_log_to_db(sessionid, str(fulfillmenttext))
            return cov.formResponseValueText(fulfillmenttext)
        elif (intent == "more_death_cases"):
            entity = str(1) if (not "count" in parameters) else str(round(parameters.get("count")))
            fulfillmenttext = cov.getTopCountyCases(entity,"DESC","most_death_cases")
            log.write_log_to_db(sessionid, str(fulfillmenttext))
            return cov.formResponseValueText(fulfillmenttext)
        elif (intent == "less_death_cases"):
            entity = str(1) if (not "count" in parameters) else str(round(parameters.get("count")))
            fulfillmenttext = cov.getTopCountyCases(entity,"ASC","less_death_cases")
            log.write_log_to_db(sessionid, str(fulfillmenttext))
            return cov.formResponseValueText(fulfillmenttext)
        elif (intent == "more_confirmed_cases"):
            entity = str(1) if (not "count" in parameters) else str(round(parameters.get("count")))
            fulfillmenttext = cov.getTopCountyCases(entity,"DESC","most_confirmed_cases")
            log.write_log_to_db(sessionid, str(fulfillmenttext))
            return cov.formResponseValueText(fulfillmenttext)
        elif (intent == "less_confirmed_cases"):
            entity = str(1) if (not "count" in parameters) else str(round(parameters.get("count")))
            fulfillmenttext = cov.getTopCountyCases(entity,"ASC","less_confirmed_cases")
            log.write_log_to_db(sessionid, str(fulfillmenttext))
            return cov.formResponseValueText(fulfillmenttext)
        elif (intent == "send_mail"):
            mailid = "" if (not "email" in parameters) else str(parameters.get("email"))
            name = "" if (not "name" in parameters) else str(parameters.get("name"))
            mobile = "" if (not "mobile" in parameters) else str(parameters.get("mobile"))
            fulfillmenttext = cov.sendMail(mailid,name,mobile)
            log.write_log_to_db(sessionid, str(fulfillmenttext))
            return cov.formResponseValueText(fulfillmenttext)
    except Exception as ex:
        log.write_log_to_db(sessionid, str(fulfillmenttext))
        return cov.formResponseValueText("Error in parameter vallue")

    else:
        log.write_log_to_db(sessionid, str(fulfillmenttext))
        fulfillmenttext = "Sorry..!! i Need more training."
        return cov.formResponseValueText(fulfillmenttext)



if __name__ == '__main__':
    port = int(os.getenv('PORT', 8085))
    print("Starting app on port %d" % port)
    chat.run(debug=False, port=port, host='0.0.0.0')
