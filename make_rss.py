import feedparser
from googletrans import Translator
import PyRSS2Gen
import json
import re
import spider_tools
from bs4 import BeautifulSoup
import datetime
import time

class AndroidReleasesRss:
    def cut_text(self,text, lenth):
        textArr = re.findall('.{'+str(lenth)+'}', text)
        textArr.append(text[(len(textArr)*lenth):])
        return textArr

    def make_android_studio_rss(self):
        rss_android_studio = feedparser.parse('https://androidstudio.googleblog.com/feeds/posts/default')
        old_rss_items={}
        rss_android_studio=feedparser.parse('./rss/android_studio_rss.xml')
        for item in rss_android_studio['entries']:
            old_rss_items[item['title']]=item
        rssItems = []
        for item in rss_android_studio['entries']:
            translate_content_str = ''
            if item['title'] in old_rss_items.keys():
                print("无需翻译:",item['title'])
                translate_content_str=old_rss_items[item['title']]['description']
            else:
                print("需翻译:",item['title'])
                translator = Translator(service_urls=['translate.google.com', ])
                content_str = item['content'][0]['value']
                if len(content_str) > 5000:
                    split_strs = self.cut_text(content_str, 4999)
                    for split_str in split_strs:
                        translate_content_str += translator.translate(split_str, src="en", dest="zh-CN").text
                else:
                    translate_content_str = translator.translate(content_str, src="en", dest="zh-CN").text
            rssItem = PyRSS2Gen.RSSItem(
                title=item['title'],
                link=item['link'],
                description=translate_content_str,
                pubDate=item['updated'],
                author=item['author']
            )
            rssItems.append(rssItem)
        rss = PyRSS2Gen.RSS2(
            title=rss_android_studio['feed']['title'],
            link=rss_android_studio['feed']['link'],
            description=rss_android_studio['feed']['subtitle'],
            lastBuildDate=rss_android_studio['feed']['updated'],
            items=rssItems)
        rss.write_xml(open('./rss/android_studio_rss.xml',"w", encoding='utf-8'), encoding='utf-8')


    def make_asp_rss(self):
        html = spider_tools.get_extranet_requests_data(
            'https://developer.android.com/studio/releases/gradle-plugin?hl=zh-cn')
        bs = BeautifulSoup(html.text, 'html.parser')
        releases = bs.find_all('h2')
        rssItems = []
        for item in releases:
            title=item.text
            if not title[0].isdigit():
                continue    
            findall = re.findall(r'[（](.*?)[）]', title)
            if len(findall)==0:
                continue      
            #转换成时间数组
            timeArray = time.strptime(findall[0], "%Y 年 %m 月")
            #转换成时间戳
            timestamp = time.mktime(timeArray)
            #转换为新的时间格式
            date_time = time.strftime(r"%Y-%m-%d %H:%M:%S",time.localtime(timestamp))
            desc='' 
            for sibling in item.next_siblings:
                if sibling in releases:
                    break
                desc+=str(sibling)
            rssItem = PyRSS2Gen.RSSItem(
                title=title,
                link='https://developer.android.com/studio/releases/gradle-plugin?hl=zh-cn',
                description=desc,
                pubDate=date_time,
                author='Google'
            )
            rssItems.append(rssItem)
        rss = PyRSS2Gen.RSS2(
            title='Android Studio Gradle Plugin',
            link='https://developer.android.com/studio/releases/gradle-plugin',
            description='Android Studio 构建系统以 Gradle 为基础，并且 Android Gradle 插件添加了几项专用于构建 Android 应用的功能。虽然 Android 插件通常会与 Android Studio 的更新步调保持一致，但插件（以及 Gradle 系统的其余部分）可独立于 Android Studio 运行并单独更新。',
            lastBuildDate=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
            items=rssItems)
        rss.write_xml(open('./rss/android_studio_gradle_plugin_rss.xml',
                      "w", encoding='utf-8'), encoding='utf-8')


class GithubReleasesRss:
    def __init__(self, url, title):
        self.url = url
        self.title = title
        self.description = title+'发布版本'

    def make_releases_rss(self):
        html = spider_tools.get_extranet_requests_data(self.url+'/releases')
        # print(html.text)
        bs = BeautifulSoup(html.text, 'html.parser')
        releases = bs.find_all('section', attrs={"aria-labelledby": True})
        rssItems = []
        for release in releases:
            # 标题
            title = release.find('h2', class_='sr-only').text.strip()
            # 发布时间
            time = release.find('relative-time')['datetime']
            # 标签链接
            href = release.find('a', class_='Link--primary')['href']
            # 内容
            desc = release.find('div')
            #作者
            author=release.find('a',class_='color-fg-muted wb-break-all').text.strip()            
            rssItem = PyRSS2Gen.RSSItem(
                title=title,
                link=href,
                description=str(desc),
                pubDate=time,
                author=author
                )
            rssItems.append(rssItem)            
        rss = PyRSS2Gen.RSS2(
            title=self.title,
            link=self.url,
            description=self.description,
            lastBuildDate=datetime.datetime.now(),
        #     image=PyRSS2Gen.Image('https://www.runoob.com/wp-content/uploads/2017/05/kotlin_250x250.png', '', 'https://www.runoob.com/wp-content/uploads/2017/05/kotlin_250x250.png')
        #    ,
            items=rssItems)
        rss.write_xml(open('./rss/{}.xml'.format(self.title.lower()+'_releases_rss'),
                      "w", encoding='utf-8'), encoding='utf-8')

    def make_tag_rss(self):
        html = spider_tools.get_extranet_requests_data(self.url+'/tags')
        bs = BeautifulSoup(html.text, 'html.parser')
        releases = bs.find_all('div', attrs={"data-test-selector": 'tag-info-container'})
        rssItems = []
        for release in releases:
            # 标题
            title = release.find('a', class_='Link--primary').text.strip()
            # 发布时间
            time = release.find('relative-time')['datetime']
            # 标签链接
            href = release.find('a', class_='Link--primary')['href']
            # 内容
            desc = release.find('div')
            #作者
            # author=release.find('a',class_='color-fg-muted wb-break-all').text.strip()            
            rssItem = PyRSS2Gen.RSSItem(
                title=title,
                link=href,
                description=str(desc),
                pubDate=time,
                # author=author
                )
            rssItems.append(rssItem)            
        rss = PyRSS2Gen.RSS2(
            title=self.title,
            link=self.url,
            description=self.description,
            lastBuildDate=datetime.datetime.now(),
        #     image=PyRSS2Gen.Image('https://www.runoob.com/wp-content/uploads/2017/05/kotlin_250x250.png', '', 'https://www.runoob.com/wp-content/uploads/2017/05/kotlin_250x250.png')
        #    ,
            items=rssItems)
        rss.write_xml(open('./rss/{}.xml'.format(self.title.lower()+'_tag_rss'),
                      "w", encoding='utf-8'), encoding='utf-8')



if __name__ == '__main__':
    GithubReleasesRss('https://github.com/JetBrains/kotlin','Kotlin').make_releases_rss()
    GithubReleasesRss('https://github.com/vuejs/vue','Vue').make_releases_rss()
    GithubReleasesRss('https://github.com/gradle/gradle','Gradle').make_releases_rss()
    GithubReleasesRss('https://github.com/nodejs/node','Node').make_releases_rss()
    GithubReleasesRss('https://github.com/torvalds/linux','Linux').make_tag_rss()
    GithubReleasesRss('https://github.com/flutter/flutter','Flutter').make_tag_rss()
    GithubReleasesRss('https://github.com/JetBrains/compose-jb','ComposeJb').make_releases_rss()
    GithubReleasesRss('https://github.com/microsoft/vscode/releases','Vscode').make_releases_rss()
    GithubReleasesRss('https://github.com/denoland/deno/releases','Deno').make_releases_rss()
    GithubReleasesRss('https://github.com/spring-projects/spring-boot','SpringBoot').make_releases_rss()

    androidRss=AndroidReleasesRss()
    androidRss.make_android_studio_rss()
    androidRss.make_asp_rss()
