from django.db import models


class UserTweets(models.Model):

    username = models.CharField(max_length=50)
    unified_tweets = models.TextField()

    def save_unified_tweets(self, username, longstring):
        self.username = username
        self.unified_tweets = longstring

        if not UserTweets.objects.filter(username=username).exists():
            self.save()

    def fetch_unified_tweets(self, username):

        asd = UserTweets.objects.get(username=username)

        return asd.unified_tweets
