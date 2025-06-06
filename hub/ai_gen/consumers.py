import json
from channels.generic.websocket import WebsocketConsumer
import random
from openai import OpenAI
import os
import boto3
import time
ssm = boto3.client('ssm',region_name='ap-northeast-1')
parameter = ssm.get_parameter(Name='OpAI_API_Key',WithDecryption=True).get('Parameter').get('Value')
openAI_client = OpenAI(api_key=parameter)
snsclient = boto3.client('sns',region_name='ap-northeast-1')
dynamoDB_client = boto3.client('dynamodb', region_name='ap-northeast-1')

class FeedConsumer(WebsocketConsumer):
    # if its a live test or dummy test.
    CALL_OPENAI = True
    
    def get_session_submissions(self, sess_id):
        resp = dynamoDB_client.get_item(
        TableName = 'SessionData',
        Key={
            "SessionID": {'S': sess_id},
            },
        ) 

        print('FEEDCONSUMER RESPONSE',resp)
        token = int(resp['Item']['Tokens']['N'])
        if resp['Item'].get('ImageCode'):
            img_arr = (resp['Item']['ImageCode']['SS'])
        else:
            img_arr = None
        return token, img_arr
    
    def set_session_submissions(self, sess_id, value, img):

        dynamoDB_client.update_item(
            TableName = 'SessionData',
            Key={
                 "SessionID": {'S': sess_id},
            },
            AttributeUpdates={
                'ImageCode' : {
                    'Value' : {
                        'SS': img
                        }
                    },
                'Tokens' : {
                    'Value' : {
                        'N': str(value)
                        }
                    },
                "SessionTTL": {
                    'Value' : {
                        'N' : str(int(time.time()+86400))
                    }
                }
                }    
            )
        print('proof that the images were loaded', img)
        
    def connect(self):
        self.accept()  

        # old stuff
        # session_ID = self.scope['session'].get('session_ID')
        # print(self.scope['session'].items())
        
        # new part:
        session = self.scope.get("session", None)
        print("Scope keys:", self.scope.keys())

        if session is None:
            self.close()
            return
        
        session_ID = session.session_key
        if session_ID is None:
            session.save()  # Force save to generate a session key
            session_ID = session.session_key
        # new part ends here

        print(f"Session ID: {session_ID}")  # for debugging
        session_submissions, prev_images = self.get_session_submissions(session_ID)


        try:
            # all_theme_tags = [x.name for x in DB_interactions.tags.all()]
            self.send(text_data=json.dumps({
                'type': 'DB_Success',
                'result' : 'initial DB setup',
                'submissions_left' : session_submissions,
                'prev_submissions' : prev_images
            }))
            gen_time = str(time.time())
            snsclient.publish(
                TopicArn='arn:aws:sns:ap-northeast-1:546197898501:OpenAI_Image_Generated',
                Subject=f'OpenAI Image Generated at {gen_time}',
                Message=json.dumps({'default': json.dumps({'mess':'someone send an Image Gen call'})}),
                MessageStructure='json'
            )
        except:
            self.send(text_data=json.dumps({
                'type': 'DB_fail',
            }))

    def receive(self, text_data):
        from .db_interactions import DB_interactions 

        # old part:
        # session_ID = self.scope['session'].get('session_ID')

        # new bootstrap solution to the sessionID not being saved
        session = self.scope.get("session", None)
        if session is None:
            self.close()
            return
        
        session_ID = session.session_key
        if session_ID is None:
            session.save()  # Force save to generate a session key
            session_ID = session.session_key

        # new part ends here

        session_submissions, prev_images = self.get_session_submissions(session_ID)

        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        salt = DB_interactions.get_salt()

        try:
            theme_tags = DB_interactions.get_image_tags(theme_tags=message)
            associated_quote_list= theme_tags.quotes_set.all()
            
            # Getting a random quote from the choices (I dont want to program another dynamic window to choose which quote to pull)
            random_option = random.choice(associated_quote_list)
            img_tags_to_focus_on = random_option.image_tag.all()

            book = random_option.book.name
            themes = ', '.join([x.name for x in random_option.theme_tag.all()])
            author = random_option.book.author
            quote = random_option.text
            img_tags = [x.name for x in img_tags_to_focus_on]
            joined_img_tags = ', '.join(img_tags)

            info_from_db = {
                'chosen_theme' : message,
                'all_themes' : themes,
                'book' : book,
                'author' : author,
                'img_tags' : joined_img_tags,
                'quote': quote,
            }
            print(info_from_db)
            # 　checks if there are enough tokens. 
            if session_submissions>0:  
                promt_for_dall_e = f'create an an scene that contains the themes of {joined_img_tags} {salt}'
                session_submissions -= 1
                print(promt_for_dall_e)
                # self.scope["session"]['submissions'] = session_submissions

                print("calling OpenAI")
                # Updates the new number of tokens 
                # to check whether I will do paid request or just test it. 
                if self.CALL_OPENAI:
                    # Dall-E api call 
                    response = openAI_client.images.generate(
                        prompt= promt_for_dall_e,
                        size="512x512",
                        response_format="url",
                        model="dall-e-2"
                    )

                    print("request completed")

                    dall_e_image = response.data[0].url
                    print('Image URL: ',dall_e_image)

                    if prev_images:
                        prev_images.append(dall_e_image)
                    else:
                        prev_images = [dall_e_image,]
                    self.set_session_submissions(session_ID, session_submissions, prev_images)

                    # print('simulated succesful request')
                    self.send(text_data=json.dumps({
                        'type' : 'search',
                        'message' : img_tags,
                        'result' : dall_e_image,
                        'submissions_left' : session_submissions,
                        'query_content' : info_from_db,
                        'prompt_used' : promt_for_dall_e,

                    }))


                    # :::: to save to db / not working as of yet.
                    # try:
                    #     DB_interactions.save_new_image(quote=random_option, url=dall_e_image, prompt_text=promt_for_dall_e)
                    # except Exception as e:
                    #     print('image didnt save because ',e)


                # if db search was successful but the api didn't give a successful image back 
                else:
                    print('simulated failed api request')
                    self.send(text_data=json.dumps({
                        'type' : 'API_fail',
                        'message' : [x.name for x in img_tags_to_focus_on],
                        'result' : 'API_fail',
                        'query_content' : info_from_db
                }))
                    
            # if db search was successful but the tokens are insufficient
            else:
                print('simulated failed request due to tokens')
                self.send(text_data=json.dumps({
                    'type' : 'insf_tokens',
                    'message' : [x.name for x in img_tags_to_focus_on],
                    'result' : 'insf_tokens',
                    'query_content' : info_from_db,

            }))
       
        # if db search was unsuccessful
        except Exception as e:
            print('error is :',e)
            print('DB query failure')
            self.send(text_data=json.dumps({
                'type' : 'search_fail',
                'result' : str(e),
            }))
            
        
    def disconnect(self, close_code):
        pass



