#SHOW_URL = 'http://services.tvrage.com/myfeeds/showinfo.php?key=P8q4BaUCuRJPYWys3RBV&sid=%s'
#EPISODES_URL = 'http://services.tvrage.com/myfeeds/episode_list.php?key=P8q4BaUCuRJPYWys3RBV&sid=%s'

####################################################################################################
def Start():

	HTTP.CacheTime = CACHE_1DAY

####################################################################################################
class TGCAgent(Agent.TV_Shows):

	name = 'TheGreatCourses'
	languages = [Locale.Language.English]
	primary_provider = True

	accepts_from = ['com.plexapp.agents.localmedia']

	def search(self, results, media, lang):
		pass

	def update(self, metadata, media, lang):
		pass
