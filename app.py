from flask import Flask, request, make_response
import json
import os
from flask_cors import cross_origin
from SendEmail.sendEmail import EmailSender
from logger import logger
from email_templates import template_reader

app = Flask(__name__)



# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():

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

    sessionID=req.get('responseId')

    result = req.get("queryResult")
    user_says=result.get("queryText")
    log.write_log(sessionID, "User Says: "+user_says)
    parameters = result.get("parameters")
    cust_name=parameters.get("cust_name")
    #print(cust_name)
    cust_contact = parameters.get("cust_contact")
    cust_email=parameters.get("cust_email")
    course_name= parameters.get("course_name")
    intent = result.get("intent").get('displayName')
    if (intent=='course_selection'):

        email_sender=EmailSender()
        template= template_reader.TemplateReader()
        email_message=template.read_course_template(course_name)
        email_sender.send_email_to_student(cust_email,email_message)
        email_file_support = open("email_templates/support_team_Template.html", "r")
        email_message_support = email_file_support.read()
        email_sender.send_email_to_support(cust_name=cust_name,cust_contact=cust_contact,cust_email=cust_email,course_name=course_name,body=email_message_support)
        fulfillmentText="We have sent the course syllabus and other relevant details to you via email. An email has been sent to the Support Team with your contact information, you'll be contacted soon. Do you have further queries?"
        log.write_log(sessionID, "Bot Says: "+fulfillmentText)
        return {
            "fulfillmentText": fulfillmentText
        }
    else:
        log.write_log(sessionID, "Bot Says: " + result.fulfillmentText)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
