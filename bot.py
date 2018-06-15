import os
import sys
import json

import requests
from flask import Flask, request

app = Flask(__name__)

page_token = "EAAEZAZB8ZAmhE0BAEG7SFnSxThqCydCy0434HXp3S6W5fOSxtpjvGYPauThI13QvQOUoZB3jjN4W3vLpmXkZBFZAFP1f2gqMPcRVFcIIax2Sc0bFqeAmo4IJg6g7o7f8Mikhq4iGcyeJN0GtF2sxuvx0j7MJAIZCUZBkiuo3iU2ZAFwZDZD"
verify_token = 'yoinfinity'
PAGE_ACCESS_TOKEN = page_token

@app.route('/webhook', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == verify_token:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

def logg(mess,meta='log',symbol='#'):
  print '%s\n%s\n%s'%(symbol*20,mess,symbol*20)

@app.route('/webhook', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events
    #set_persistent_menu()

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                #print messaging_event

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    print sender_id

                    send_message(sender_id, "roger that!")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    print "postback detected"
                    sender_id = messaging_event["sender"]["id"] 
                    handle_postback(sender_id,messaging_event['postback']['payload'])

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": page_token
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def set_persistent_menu():
    post_message_url = "https://graph.facebook.com/v2.6/me/thread_settings?access_token=%s"%PAGE_ACCESS_TOKEN
    
    menu_object = {
            "setting_type" : "call_to_actions",
            "thread_state" : "existing_thread",
            "call_to_actions":[
                {
                    "type":"postback",
                    "title":"Counselling Session",
                    "payload":"MENT"
                },
                {
                    "type":"postback",
                    "title":"Events & News",
                    "payload":"PNEW"
                },
                {
                    "type":"postback",
                    "title":"Get Skilled",
                    "payload":"JOBO"
                },
                {
                    "type":"postback",
                    "title":"Call for help",
                    "payload":"CALLF"
                },
                {
                    "type":"postback",
                    "title":"Donate",
                    "payload":"DONA"
                }

            ]
    }
    menu_object = json.dumps(menu_object)
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=menu_object)
    logg(status.json(),symbol='---**---')
    pprint(status.json())

def handle_postback(fbid,payload):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    
    logg(payload,symbol='*')
    
    response_text = ''
    response_object = ''
    
    if payload == 'MENT':

        response_object = {

                "recipient":{
                    "id":fbid
                  },
                  "message":{
                    "attachment":{
                      "type":"template",
                      "payload":{
                        "template_type":"generic",
                        "elements":[
                          {
                            "title":'Nouman Ali Khan',
                            "image_url":'http://www.eiis.org.uk/wp-content/uploads/2016/08/WhatsApp-Image-2016-08-29-at-1.54.11-PM.jpeg',
                            "subtitle":"Pakistani-American Muslim speaker and founder, CEO and lead instructor at Bayyinah, the Institute for Arabic and Qur'anic Studies",
                            "buttons":[
                              {
                                "type":"web_url",
                                "url":'https://www.facebook.com/noumanbayyinah',
                                "title":"Book a session"
                              }    
                            ]
                          },
                          {
                            "title":'Sadhguru',
                            "image_url":'http://www.ishafoundation.org/templates/isha/homeslider/About-us-Sadhguru.jpg',
                            "subtitle":"Indian yogi, mystic, poet and bestselling author. He founded the Isha Foundation, a not for profit organization which offers yoga programs around the world",
                            "buttons":[
                              {
                                "type":"web_url",
                                "url":'http://isha.sadhguru.org/',
                                "title":"Book a session"
                              }         
                            ]
                          },
                          {
                            "title":'Ellen DeGeneres',
                            "image_url":'https://pmcdeadline2.files.wordpress.com/2011/03/ellen_20110322192422.jpg',
                            "subtitle":"American comedian, television host, actress, writer, and producer.",
                            "buttons":[
                              {
                                "type":"web_url",
                                "url":'https://www.ellentube.com/',
                                "title":"Book a session"
                              }         
                            ]
                          }
                        ]
                      }
                    }
                  }

        }

    elif payload == 'CALLF':
         
        response_object={
                          "recipient":{
                            "id":fbid
                          },
                          "message":{
                            "attachment":{
                              "type":"template",
                              "payload":{
                                "template_type":"button",
                                "text":"Need immediate assistance ? Call our toll-free number",
                                "buttons":[
                                  {
                                            "type":"phone_number",
                                            "title":"Call Us",
                                            "payload":"+918447789937"
                                  }
                                ]
                              }
                            }
                          }
                        }

    elif payload == 'DONA':
        response_text = 'Follow this link to give financial help to those in need https://1mp.me/donate'


    elif payload == 'LEAR':
        response_text = 'Our mission is to help people suffereng from violent extremism practices online.'


    elif payload == 'PNEW':
        #response_text = 'Our mission is to help people suffereng from violent extremism practices online.'

        response_object = {

                "recipient":{
                    "id":fbid
                  },
                  "message":{
                    "attachment":{
                      "type":"template",
                      "payload":{
                        "template_type":"generic",
                        "elements":[
                          {
                            "title":'Sikhs come to aid of Rohingya Muslim',
                            "image_url":'https://static.independent.co.uk/s3fs-public/styles/story_large/public/thumbnails/image/2017/09/13/15/khalsa-aid.jpg',
                            "subtitle":"Khalsa Aid says volunteers handing out food and water in Cox's Bazar area",
                            "buttons":[
                              {
                                "type":"web_url",
                                "url":'http://www.independent.co.uk/news/world/asia/rohingya-muslims-burma-flee-sikhs-help-bangladesh-khalsa-aid-food-water-ethnic-cleansing-a7945111.html',
                                "title":"View"
                              }    
                            ]
                          },
                          {
                            "title":'Cooks Lake Road community helping each other',
                            "image_url":'http://static-40.sinclairstoryline.com/resources/media/b51a71d6-9165-4cca-8d00-cea858e7e5ce-large16x9_0913_helpingharveyvictims2.JPG',
                            "subtitle":"A woman opened up her front yard that is full of donations that flood victims can use.",
                            "buttons":[
                              {
                                "type":"web_url",
                                "url":'http://kfdm.com/news/local/cooks-lake-road-community-helping-each-other',
                                "title":"View"
                              }         
                            ]
                          },
                          {
                            "title":'American trip for Telangana tribals',
                            "image_url":'http://www.theweekendleader.com/tamil/backend/web/article/images/feb26-16-LEAD1.jpg',
                            "subtitle":"Innovative tribal farmers from Telangana will fly to the US, Israel, Germany and other countries to understand the best agricultural practices",
                            "buttons":[
                              {
                                "type":"web_url",
                                "url":'http://timesofindia.indiatimes.com/city/hyderabad/crop-study-american-junket-for-telangana-tribals/articleshow/60455873.cms',
                                "title":"View"
                              }         
                            ]
                          }
                        ]
                      }
                    }
                  }

        }

    elif payload == 'JOBO':
        #response_text = 'Our mission is to help people suffereng from violent extremism practices online.'

        response_object = {

                "recipient":{
                    "id":fbid
                  },
                  "message":{
                    "attachment":{
                      "type":"template",
                      "payload":{
                        "template_type":"generic",
                        "elements":[
                          {
                            "title":'Coders Trust',
                            "image_url":'http://dailyasianage.com/library/1495834611_2.jpg',
                            "subtitle":"BECOME A ROCKSTAR FREELANCER, Learn a skill. Make a living ANYTIME ANYWHERE",
                            "buttons":[
                              {
                                "type":"web_url",
                                "url":'http://coderstrustbd.com/',
                                "title":"View"
                              }    
                            ]
                          },
                          {
                            "title":'The coding school',
                            "image_url":'http://www.thehackingschool.com/home/images/logo-header.png',
                            "subtitle":"13 Week Fullstack JavaScript programming - and a hacker is born!",
                            "buttons":[
                              {
                                "type":"web_url",
                                "url":'http://www.thehackingschool.com/home/index.html',
                                "title":"View"
                              }         
                            ]
                          }
                        ]
                      }
                    }
                  }

        }


    if response_text:
        if response_object:
            response_object1 = json.dumps({"recipient":{"id":fbid}, "message":{"text":response_text}})
            response_object2 = json.dumps(response_object)
            requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_object1)
            requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_object2)
            return
        else:
            response_object = json.dumps({"recipient":{"id":fbid}, "message":{"text":response_text}})
    else:
        response_object = json.dumps(response_object)

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_object)
    logg(status.json(),symbol='---297---')
    return



def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)


