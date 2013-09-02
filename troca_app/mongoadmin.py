# Import the MongoAdmin base class

from mongonaut.sites import MongoAdmin
 
# Import your custom models
from troca_app.models import GenericItem, Offer, Vote
 
 
class GenericItemMongoAdmin(MongoAdmin):
    search_fields = ('title',)
    list_fields = ('title',)

# Then attach the mongoadmin to your model 
GenericItem.mongoadmin = GenericItemMongoAdmin()


