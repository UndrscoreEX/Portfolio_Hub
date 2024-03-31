from django.shortcuts import render
from django.views import View
from .db_interactions import DB_interactions

import boto3
client = boto3.client('dynamodb', region_name='ap-northeast-1')

# check for/ create initial tokens
def check_submissions_or_create(req):
    
    try:
        session_ID = req.COOKIES.get('sessionid')
        check_session_exists = client.get_item(
            TableName = 'SessionData',
            Key={
                "SessionID": {'S': session_ID},
                },
        )

        if check_session_exists.get('Item'):
            cur_submissions = int(check_session_exists['Item']['Tokens']['N'])
        else:
            client.put_item(
                TableName = 'SessionData',
                Item = {
                    'SessionID': {'S': session_ID},
                    'Tokens': {'N': '5'},
                    'SessionTTL' : {'N':str(int(time.time()+86400))}
                    }
            )
            cur_submissions = 5
            print('needed to restart a session token')

        # so we can check the DynamoDB table from the Websocket connection.
        req.session['session_ID'] = session_ID
        req.session.save()

        return cur_submissions
    except:
        print('cant get access to the sessionID of the browser cookies. You get Nothing')
        return 0
        


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

        # populating the initial set of themes under the search bar
        theme_tags_for_search = DB_interactions.tags.all()
        theme_tags_for_search = [x[0] for x in theme_tags_for_search.values_list("name")]

        # print('checking sessions after initial check: ',  request.session.session_key, request.session['submissions'] )
        # print(images, submissions, all_theme_tags, )
        return render(request,'ai_image_gen/index.html',{
            'theme_tag_results_raw':", ".join(theme_tags_for_search),
            'theme_tags_results_list': theme_tags_for_search,
            'sumbissions_so_far' : submissions,
            'carousel_images': images,
            'all_theme_tags' : all_theme_tags,

            })