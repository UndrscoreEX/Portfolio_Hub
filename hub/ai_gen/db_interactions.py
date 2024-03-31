import random
from .models import Theme_tags,Salt, Saved_images
import boto3

class DB_interactions:
    tags = Theme_tags.objects
    salt = Salt.objects

    @classmethod
    def get_image_tags(cls, theme_tags):
        img_tags = cls.tags.filter(name= theme_tags)[0]
        return img_tags
    
    @classmethod
    def get_salt(cls):
        salt = cls.salt.all()
        salt = random.choice(salt)
        return salt
    
    # from a time when I didn't know that Dall-E will invalidate the links after a while. 
    @classmethod
    def save_new_image(cls, quote, url, prompt_text):
        Saved_images.create_from_url(quote=quote,image_url=url, prompt=prompt_text)

    @classmethod
    def get_saved_images(cls):

        # 5 random numbers 
        pks =  list(Saved_images.objects.values_list('id',flat=True))
        random.shuffle(pks)
        rand_images = Saved_images.objects.filter(pk__in=pks[:5])
        saved_images_dict = [{
                'quote': img.quote.text,
                'image_url' : img.ai_img,
                'author' : img.quote.book.author,
                'book' : img.quote.book.name,
                'img_tags' : list(img.quote.theme_tag.values_list('name', flat=True),),
                'theme_tags' : list(img.quote.image_tag.values_list('name', flat=True))
            } for img in rand_images]
        
        return saved_images_dict



# This is here because I want to add a redis cache layer // turns out im adding dynamoDB cache layer instead. opps
def submissions_check(sess_id):
    client = boto3.client('dynamodb', region_name='ap-northeast-1')
    resp = client.get_item(
    TableName = 'SessionData',
    Key={
        "SessionID": {'S': sess_id},
        },
    ProjectionExpression = "Tokens"
    ) 

    print(resp)
    token = int(resp['Item']['Tokens']['N'])
    print(f'remaining tokens are : {token}')
    return token> 0, token