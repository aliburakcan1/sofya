# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.files.storage import default_storage

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.shortcuts import render, HttpResponse
from demo.models import UserTweets

from .forms import ContactForm, FilesForm, ContactFormSet
from threading import Thread
import tweepy
import pandas as pd
import numpy as np
import nltk
import demo.models
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk import ngrams
from collections import Counter
import time
import six

a = 0
tc = 1
yuzde = 0


# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, "dummy.txt")


class HomePageView(TemplateView):
    template_name = "app/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        import demo.models
        tw = demo.models.UserTweets()
        #tw.save_unified_tweets("1", "sdas")
        messages.info(self.request, tw.fetch_unified_tweets("1"))
        return context


class DefaultFormsetView(FormView):
    template_name = "app/formset.html"
    form_class = ContactFormSet


class DefaultFormView(FormView):
    template_name = "app/form.html"
    form_class = ContactForm



    # Define a function for the thread
    def get(self, request, *args, **kwargs):

        list_of_dicts = [
            {'pid': 0, 'name': 'System Process'},
            {'pid': 41, 'name': 'System123'},
            {'pid': 110, 'name': 'svchost.exe'},
            {'pid': 280, 'name': 'smss.exe'},
            {'pid': 336, 'name': 'WSE.exe'},
            {'pid': 424, 'name': 'csrss.exe'}
        ]
        list_of_dicts2 = [
            {'pid': 1, 'name': 'System Process'},
            {'pid': 4, 'name': 'System123'},
            {'pid': 110, 'name': 'svchost.exe'},
            {'pid': 20, 'name': 'smss.exe'},
            {'pid': 36, 'name': 'WSE.exe'},
            {'pid': 24, 'name': 'csrss.exe'}
        ]
        context = {
            "list_of_dicts": list_of_dicts,
            "list_of_dicts2": list_of_dicts2,
            "control": 'close',
            "name": 'bos.png'
        }
        return render(request, "app/form.html", context)

    def post(self, request, *args, **kwargs):

        def saveFig(list_of_dict, isim, col_width, font_size):

            def render_mpl_table(data, isim, col_width=3.0, row_height=0.625, font_size=14,
                                 header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                                 bbox=[0, 0, 1, 1], header_columns=0,
                                 ax=None, **kwargs):
                if ax is None:
                    size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
                    fig, ax = plt.subplots(figsize=size)
                    ax.axis('off')

                mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

                mpl_table.auto_set_font_size(False)
                mpl_table.set_fontsize(font_size)

                for k, cell in six.iteritems(mpl_table._cells):
                    cell.set_edgecolor(edge_color)
                    if k[0] == 0 or k[1] < header_columns:
                        cell.set_text_props(weight='bold', color='w')
                        cell.set_facecolor(header_color)
                    else:
                        cell.set_facecolor(row_colors[k[0] % len(row_colors)])
                plt.savefig(isim)

            def splitDataFrameIntoSmaller(df, chunkSize=10000):
                listOfDf = list()
                print('lendf:', len(df))
                print('cs:', chunkSize)
                numberChunks = len(df) // chunkSize + 1
                for i in range(numberChunks):
                    dd = df[i * chunkSize:(i + 1) * chunkSize]
                    if dd.empty:
                        break
                    listOfDf.append(df[i * chunkSize:(i + 1) * chunkSize])

                return listOfDf

            df = pd.DataFrame(list_of_dict)
            df = pd.DataFrame({'Phrase': df['phrase'], 'Count': df['count']})

            liste = splitDataFrameIntoSmaller(df, int(len(df) / 3))

            df1 = liste[0].reset_index(drop=True)
            df2 = liste[1].reset_index(drop=True)
            df3 = liste[2].reset_index(drop=True)

            df = pd.concat([df1, df2, df3], axis=1)
            render_mpl_table(df, isim, header_columns=0, col_width=col_width)

        global tc
        global yuzde

        ut = demo.models.UserTweets()
        print(UserTweets.objects.filter(username=request.POST.get('username')).exists())
        if UserTweets.objects.filter(username=request.POST.get('username')).exists():

            print("dene")

            yuzde = 100

            import re
            uzunstring = ut.fetch_unified_tweets(request.POST.get('username'))
            uzunstring = re.sub(r'http\S+', '', uzunstring)

            uzunstring = re.sub(r'@\S+', '', uzunstring)
            # nltk.download('stopwords')
            # nltk.download('punkt')
            stop_word_list = nltk.corpus.stopwords.words('turkish')
            stop_word_list.append('bi')
            stop_word_list.append('mi')
            stop_word_list.append('bir')
            stop_word_list.append('var')
            stop_word_list.append('bu')
            stop_word_list.append('yok')
            stop_word_list.append('.')
            stop_word_list.append('?')
            stop_word_list.append(':')
            stop_word_list.append('D')
            stop_word_list.append('#')
            stop_word_list.append(';')
            stop_word_list.append('')
            stop_word_list.append('-')
            stop_word_list.append(',')
            stop_word_list.append('/')
            # for stop_word in stop_word_list:
            # stop_word_list.append(stop_word.upper())

            # print(stop_word_list)
            ngram_counts2 = Counter(ngrams(uzunstring.upper().split(), 2))
            ngram_counts3 = Counter(ngrams(uzunstring.upper().split(), 3))
            list_of_dicts = []
            list_of_dicts2 = []
            list_of_dicts3 = []

            for tag in ngram_counts2:
                dict = {}
                key = ' '.join(tag)
                dict['phrase'] = key
                dict['count'] = ngram_counts2[tag]
                list_of_dicts2.append(dict)
            for tag in ngram_counts3:
                dict = {}
                key = ' '.join(tag)
                dict['phrase'] = key
                dict['count'] = ngram_counts3[tag]
                list_of_dicts3.append(dict)
            # print(ngram_counts2.most_common(100), '\n\n')
            # print(ngram_counts3.most_common(100), '\n\n')

            tokens = nltk.word_tokenize(uzunstring.lower())
            filtered_tokens = [token for token in tokens if token not in stop_word_list]
            uzunstring = ' '.join(filtered_tokens)
            ngram_counts = Counter(ngrams(uzunstring.upper().split(), 1))

            for tag in ngram_counts:
                dict = {}
                key = ' '.join(tag)
                dict['phrase'] = key
                dict['count'] = ngram_counts[tag]
                list_of_dicts.append(dict)
            # print(ngram_counts.most_common(100), '\n\n')

            # print(uzunstring)

            # print(uzunstring)
            wordcloud = WordCloud(mode='RGB', width=1800, height=900, background_color="white").generate(
                uzunstring.upper())
            plt.figure(figsize=(20, 10))
            plt.imshow(wordcloud, interpolation="nearest", aspect='equal')
            plt.axis("off")
            name = str(request.POST.get('username')) + 'Wordcloud.png'
            plt.savefig('demo/static/' + name)
            context = {
                "list_of_dicts": sorted(list_of_dicts, key=lambda k: k['count'], reverse=True)[:100],
                "list_of_dicts2": sorted(list_of_dicts2, key=lambda k: k['count'], reverse=True)[:100],
                "list_of_dicts3": sorted(list_of_dicts3, key=lambda k: k['count'], reverse=True)[:100],
                "control": 'open',
                "name": name,
                "table1": 'table1.png',
                "table2": 'table2.png',
                "table3": 'table3.png'
            }
            saveFig(sorted(list_of_dicts, key=lambda k: k['count'], reverse=True)[:100], 'demo/static/table1.png', 3.0, 14)
            saveFig(sorted(list_of_dicts2, key=lambda k: k['count'], reverse=True)[:100], 'demo/static/table2.png', 4.0, 12)
            saveFig(sorted(list_of_dicts3, key=lambda k: k['count'], reverse=True)[:100], 'demo/static/table3.png', 5.0, 10)
            yuzde = 0
            return render(request, 'app/form.html', context)


        #global tc
        #global yuzde
        APIKEY = "5iEFuuc6VpxIdhOAWxmAru2bf"
        APISECRETKEY = "S3PGe3Kof5UfCj0fWH1IzYdhwN0oig7QkotoEVsWjUwQWOjiL4"
        ACCESSTOKEN = "2976696615-Lb5t9LIvcsdx8jWaWEr0eJZSWWwpdEj1hj1h5mP"
        ACCESSTOKENSECRET = "kpUHw5UkLcPKXimhYMdrG8uVo5QXWrYvMDATnXICI1nGb"
        auth = tweepy.OAuthHandler(APIKEY, APISECRETKEY)
        auth.set_access_token(ACCESSTOKEN, ACCESSTOKENSECRET)
        api = tweepy.API(auth)
        tweets = []

        if request.is_ajax():

            if yuzde > 97:

                return HttpResponse('bitti')

            return HttpResponse(yuzde)
        try:
            tc = api.get_user(request.POST.get('username')).statuses_count
            if tc < 3:
                return render(request, 'app/form.html')
        except:
            return render(request, 'app/form.html')

        if tc > 3200:
            tc = 3200

        #global a
        try:
            for tweet in tweepy.Cursor(api.user_timeline, id=request.POST.get('username'), tweet_mode='extended').items():
                tweets.append(tweet.full_text)
                yuzde = 100 * len(tweets) / tc
        except:
            return render(request, 'app/form.html')

        print('döngü bitti len=', len(tweets))
        tc = len(tweets)

        df = pd.DataFrame({'tweets': tweets})
        df = df[~df['tweets'].str.contains('RT')]
        uzunstring = ' '.join(df['tweets'])

        ut.save_unified_tweets(request.POST.get('username'), uzunstring)
        import re

        uzunstring = re.sub(r'http\S+', '', uzunstring)
        uzunstring = re.sub(r'@\S+', '', uzunstring)
        # nltk.download('stopwords')
        # nltk.download('punkt')
        stop_word_list = nltk.corpus.stopwords.words('turkish')
        stop_word_list.append('bi')
        stop_word_list.append('mi')
        stop_word_list.append('bir')
        stop_word_list.append('var')
        stop_word_list.append('bu')
        stop_word_list.append('yok')
        stop_word_list.append('.')
        stop_word_list.append('?')
        stop_word_list.append(':')
        stop_word_list.append('D')
        stop_word_list.append('#')
        stop_word_list.append(';')
        stop_word_list.append('')
        stop_word_list.append('-')
        stop_word_list.append(',')
        stop_word_list.append('/')
        # for stop_word in stop_word_list:
        # stop_word_list.append(stop_word.upper())

        #print(stop_word_list)

        ngram_counts2 = Counter(ngrams(uzunstring.upper().split(), 2))
        ngram_counts3 = Counter(ngrams(uzunstring.upper().split(), 3))

        list_of_dicts = []
        list_of_dicts2 = []
        list_of_dicts3 = []

        for tag in ngram_counts2:
            dict = {}
            key = ' '.join(tag)
            dict['phrase'] = key
            dict['count'] = ngram_counts2[tag]
            list_of_dicts2.append(dict)
        for tag in ngram_counts3:
            dict = {}
            key = ' '.join(tag)
            dict['phrase'] = key
            dict['count'] = ngram_counts3[tag]
            list_of_dicts3.append(dict)
        # print(ngram_counts2.most_common(100), '\n\n')
        # print(ngram_counts3.most_common(100), '\n\n')

        tokens = nltk.word_tokenize(uzunstring.lower())
        filtered_tokens = [token for token in tokens if token not in stop_word_list]
        uzunstring = ' '.join(filtered_tokens)

        ngram_counts = Counter(ngrams(uzunstring.upper().split(), 1))

        for tag in ngram_counts:
            dict = {}
            key = ' '.join(tag)
            dict['phrase'] = key
            dict['count'] = ngram_counts[tag]
            list_of_dicts.append(dict)

        # print(ngram_counts.most_common(100), '\n\n')

        # print(uzunstring)

        # print(uzunstring)
        wordcloud = WordCloud(mode='RGB', width=1800, height=900, background_color="white").generate(uzunstring.upper())
        plt.figure(figsize=(20, 10))
        plt.imshow(wordcloud, interpolation="nearest", aspect='equal')
        plt.axis("off")
        name = str(request.POST.get('username')) + 'Wordcloud.png'
        plt.savefig('demo/static/' + name)

        context = {
            "list_of_dicts": sorted(list_of_dicts, key=lambda k: k['count'], reverse=True)[:100],
            "list_of_dicts2": sorted(list_of_dicts2, key=lambda k: k['count'], reverse=True)[:100],
            "list_of_dicts3": sorted(list_of_dicts3, key=lambda k: k['count'], reverse=True)[:100],
            "control": 'open',
            "name": name,
            "table1": 'table1.png',
            "table2": 'table2.png',
            "table3": 'table3.png'
        }
        saveFig(sorted(list_of_dicts, key=lambda k: k['count'], reverse=True)[:100], 'demo/static/table1.png', 3.0, 14)
        saveFig(sorted(list_of_dicts2, key=lambda k: k['count'], reverse=True)[:100], 'demo/static/table2.png', 4.0, 12)
        saveFig(sorted(list_of_dicts3, key=lambda k: k['count'], reverse=True)[:100], 'demo/static/table3.png', 5.0, 10)
        yuzde = 0

        return render(request, 'app/form.html', context)


class DefaultFormByFieldView(FormView):
    template_name = "app/form_by_field.html"
    form_class = ContactForm


class FormHorizontalView(FormView):
    template_name = "app/form_horizontal.html"
    form_class = ContactForm


class FormInlineView(FormView):
    template_name = "app/form_inline.html"
    form_class = ContactForm


class FormWithFilesView(FormView):
    template_name = "app/form_with_files.html"
    form_class = FilesForm

    def get_context_data(self, **kwargs):
        context = super(FormWithFilesView, self).get_context_data(**kwargs)
        context["layout"] = self.request.GET.get("layout", "vertical")
        return context

    def get_initial(self):
        return {"file4": fieldfile}


class PaginationView(TemplateView):
    template_name = "app/pagination.html"

    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
        lines = []
        for i in range(200):
            lines.append("Line %s" % (i + 1))
        paginator = Paginator(lines, 10)
        page = self.request.GET.get("page")
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_lines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_lines = paginator.page(paginator.num_pages)
        context["lines"] = show_lines
        return context


class MiscView(TemplateView):
    template_name = "app/misc.html"
