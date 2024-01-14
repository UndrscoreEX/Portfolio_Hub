from django.shortcuts import render
from django.views import View
from .db_interactions import DB_interactions

# check for/ create initial tokens
def check_submissions_or_create(req):
        
        if not req.session.__contains__('submissions'):
            req.session['submissions'] = 5
            req.session.save()

        return req.session.__getitem__('submissions')


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
        print(images, submissions, all_theme_tags, )
        return render(request,'ai_image_gen/index.html',{
            'theme_tag_results_raw':", ".join(theme_tags_for_search),
            'theme_tags_results_list': theme_tags_for_search,
            'sumbissions_so_far' : submissions,
            'carousel_images': images,
            'all_theme_tags' : all_theme_tags,

            })