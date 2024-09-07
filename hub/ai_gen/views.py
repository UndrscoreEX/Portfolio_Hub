from django.shortcuts import render
from django.views import View
from .db_interactions import DB_interactions
import time
import random

import boto3
client = boto3.client('dynamodb', region_name='ap-northeast-1')

# check for/ create initial tokens
def check_submissions_or_create(req):
    
    # prev, using Cookies+ sessions+ DynamoDB. cookies and sessions break randomly 


    print('pre-check for sessionID')
    if not req.COOKIES.get('sessionid'):
        session_ID =  str(int(random.random() * 10000))
        req.COOKIES['sessionid'] = session_ID
        print("There was no sessionID from the start")    
    else:
        session_ID = req.COOKIES.get('sessionid')

    print(f"\n\n***************{session_ID}****************\n\n")

    try:
        check_session_exists = client.get_item(
            TableName = 'SessionData',
            Key={
                "SessionID": {'S': session_ID},
                },
        )

        if check_session_exists.get('Item'):
            cur_submissions = int(check_session_exists['Item']['Tokens']['N'])
            print('Session already exists in DB')
        else:
            # put_call = client.put_item(
            client.put_item(
                TableName = 'SessionData',
                Item = {
                    'SessionID': {'S': session_ID},
                    'Tokens': {'N': '5'},
                    'SessionTTL' : {'N':str(int(time.time()+86400))}
                    }
            )
            print('didnt find it, granting a new one')
            cur_submissions = 5
    except:
        client.put_item(
                    TableName = 'SessionData',
                    Item = {
                        'SessionID': {'S': session_ID},
                        'Tokens': {'N': '5'},
                        'SessionTTL' : {'N':str(int(time.time()+86400))}
                        }
                )
        print('didnt find it, granting a new one')
        cur_submissions = 5 

    # so we can check the DynamoDB table from the Websocket connection.
    # going to work without using this session below:
    try: 
        req.session['session_ID'] = session_ID
        print('added sessionID to session')
        req.session.save()
        print('saving')
    except:
        print('couldnt add or save ')

    return cur_submissions


    # old code
    # if not req.session.__contains__('submissions'):
    #     req.session['submissions'] = 5
    #     req.session.save()
    # return req.session.__getitem__('submissions')


class Home_page(View):
    def get(self,request):

        # getting the 5 random images for carousel.  
        images = DB_interactions.get_saved_images()

        all_theme_tags = [x.name for x in DB_interactions.tags.all()]

        submissions = check_submissions_or_create(req=request) 
        print("**************",submissions)

        # populating the initial set of themes under the search bar
        theme_tags_for_search = DB_interactions.tags.all()
        theme_tags_for_search = [x[0] for x in theme_tags_for_search.values_list("name")]


        print('just before the render is sent. It means it failed at the very end')
        # print('checking sessions after initial check: ',  request.session.session_key, request.session['submissions'] )
        # print(images, submissions, all_theme_tags, )
        return render(request,'ai_image_gen/index.html',{
            'theme_tag_results_raw':", ".join(theme_tags_for_search),
            'theme_tags_results_list': theme_tags_for_search,
            'sumbissions_so_far' : submissions,
            'carousel_images': images,
            'all_theme_tags' : all_theme_tags,

            })