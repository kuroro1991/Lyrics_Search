# coding: UTF-8
#import appex
from bs4 import BeautifulSoup
import console
import re
import requests
import sys
import ui

"""
歌詞検索サイト
www.uta-net.com
www.utamap.com
utaten.com
j-lyric.net
www.kget.jp
kashinavi.com
joysound.com
"""

def load_args(args):
	"""引数の読み込みんでURLを加工
URLに"="が含まれているとPythonista3にうまく引数が渡せない
ショートカットアプリで"="を"%20"に変換、この引数で"="に戻す
	
		Args:
			args: YouTube動画のURL
		Return:
			YoutubeのURL形式
	"""
	if 'youtube' not in args[1]:
		console.alert('エラー', 'YouTube以外のWebサイトには対応していません', 'OK', hide_cancel_button=True)
		sys.exit()
		
	return args[1] + '=' + args[2]


def scraping(url):
	"""引数のurl(YouTubeのURL)から動画タイトルを取得

		Args:
			url: YoutubeのURL
		Return:
			title: Youtubeの動画タイトル
	"""
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	# <meta property="og:title" content="*****">
	elements = soup.find_all('meta', attrs={'property': 'og:title', 'content': True})
	title = elements[0]['content']
	# print('title: ', title)
	return title


def set_tableview(view, urls=[]):
	"""引数urls(歌詞サイトのURL)をtableviewにappendして最前面表示する
	
		Args:
			view: tableview
			urls: 歌詞サイトのURL
	"""
	tableview = view
	# tableview.data_source.items = [{'title':'aaa'}, {'title':'bbb'}]
	tableview.data_source.items.clear()
	if urls:
		for url in urls:
			tableview.data_source.items.append(url)
			
		tableview.alpha = 1.0
		tableview_button.alpha = 1.0
		tableview.bring_to_front()
		tableview_button.bring_to_front()
		
		search_tableview.alpha = 0.0
		search_tableview_label.alpha = 0.0
		textfield.alpha = 0.0
		search_button.alpha = 0.0


def set_search_tableview(view, title):
	"""引数title(YouTubeの動画タイトル)を' '区切りにして再検索画面に
候補として表示する動画タイトル + 歌詞で歌詞サイトが見つからないときの対策

		Args:
			view: search_tableview
			title: Youtubeの動画タイトル
	"""
	search_tableview = view
	search_words = title.split(' ')
	
	search_tableview.data_source.items.clear()
	if search_words:
		for word in search_words:
			search_tableview.data_source.items.append(word)
			
		search_tableview.alpha = 1.0
		search_tableview_label.alpha = 1.0
		textfield.alpha = 1.0
		search_button.alpha = 1.0
		search_tableview.bring_to_front()
		search_tableview_label.bring_to_front()
		textfield.bring_to_front()
		search_button.bring_to_front()
		
		tableview.alpha = 0.0
		tableview_button.alpha = 0.0

def show_status():
	"""各UIのステータス表示"""
	print('--- common UI ---')
	print('segmentedcontrol: ', segmentedcontrol.selected_index)
	print('')
	print('--- tableview UI ---')
	print('tableview: ', tableview.alpha)
	print('tableview_button: ', tableview_button.alpha)
	print('temp: ', temp_tableview_alpha)
	print('')
	print('--- search_tableview UI ---')
	print('search_tableview: ', search_tableview.alpha)
	print('textfield: ', textfield.alpha)
	print('search_tableview_label', search_tableview_label.alpha)
	print('search_button', search_button.alpha)
	print('')
	print('--- webview UI ---')
	print('webview: ', webview.alpha)
	print('')
	print('')


def switch_webview(sender):
	"""webviewとtableview & search_tableviewの画面切替

		Args:
			sender: イベント取得
	"""
	global temp_tableview_alpha
	# tableview = sender.superview['tableview']
	# search_tableview = sender.superview['search_tableview']
	
	# idx [Search:0 / Lryic:1]
	idx = sender.selected_index
	#print('s: ', sender)
	
	if idx == 0:
		# webview -> tableview へ切替
		webview.alpha = 0.0
		
		if temp_tableview_alpha:
			tableview.alpha = temp_tableview_alpha
			tableview_button.alpha = 1.0
			search_tableview.alpha = 0.0
			search_tableview_label.alpha = 0.0
			textfield.alpha = 0.0
			search_button.alpha = 0.0
			tableview.bring_to_front()
			tableview_button.bring_to_front()
			
		else:
			tableview.alpha = temp_tableview_alpha
			tableview_button.alpha = 0.0
			search_tableview.alpha = 1.0
			search_tableview_label.alpha = 1.0
			textfield.alpha = 1.0
			search_button.alpha = 1.0
			search_tableview.bring_to_front()
			search_tableview_label.bring_to_front()
			textfield.bring_to_front()
			search_button.bring_to_front()
			
	else:
		# tableview -> webview へ切替
		temp_tableview_alpha = tableview.alpha		
		tableview.alpha = 0.0
		tableview_button.alpha = 0.0
		search_tableview.alpha = 0.0
		search_tableview_label.alpha = 0.0
		webview.alpha = 1.0
		webview.bring_to_front()
	
	# show_status()

def switch_tableview():
	"""tableview と search_tableviewの画面切替"""
	if tableview.alpha:
		tableview.alpha = 0.0
		tableview_button.alpha = 0.0
		search_tableview.alpha = 1.0
		search_tableview_label.alpha = 1.0
		textfield.alpha = 1.0
		search_button.alpha = 1.0
		search_tableview.bring_to_front()
		search_tableview_label.bring_to_front()
		textfield.bring_to_front()
		search_button.bring_to_front()
		
	else:
		tableview.alpha = 1.0
		tableview_button.alpha = 1.0
		search_tableview.alpha = 0.0
		search_tableview_label.alpha = 0.0
		textfield.alpha = 0.0
		search_button.alpha = 0.0
		tableview.bring_to_front()
		tableview_button.bring_to_front()
		
	#show_status()


def set_webview(view, url=''):
	"""webviewの最前面表示
	
		Args:
			view: webview
			url: webviewに表示するURL
	"""
	webview = view
	webview.load_url(url)
	webview.alpha = 1.0
	webview.bring_to_front()


def selected_item(sender):
	"""tableviewのアイテム選択時のアクション
	
		Args:
			sender: イベント取得
	"""
	global temp_tableview_alpha
	index = sender.selected_row
	#print('index: ', index)

	segmentedcontrol.selected_index = 1
	temp_tableview_alpha = tableview.alpha
	set_webview(webview, sender.items[index])
	#show_status()


def selected_search_item(sender):
	"""search_tableviewのアイテム選択時のアクション

		Args:
			sender: イベント取得
	"""
	index = sender.selected_row
	#print('item: ', sender.items[index])
	lryics_urls = search_google(sender.items[index])
	if lryics_urls:
		set_tableview(tableview, lryics_urls)
		#show_status()
	
	else:
		console.alert('歌詞が見つかりませんでした', '”再検索”ボタンを押して\n再検索してください', 'OK', hide_cancel_button=True)	
	
	
def pushed_button(sender):
	"""search_viewのsearch_button押下時のアクション
	
		Args:
			sender: イベント取得
	"""
	#print('pushed button')
	print('textfield: ', textfield.text)
	match_list = search_google(textfield.text)
	set_tableview(tableview, match_list)
	show_status()


def pushed_tableview_button(sender):
	"""tableview_buttonを押下時のアクション

		Args:
			sender: イベント取得
	"""
	switch_tableview()
	#show_status()


def search_google(title):
	"""引数title(YouTubeの動画タイトル)を基にGoogleで検索して歌詞サイトを返す
	
		Args:
			title: YouTubeの動画タイトル
		Return:
			matchlist: 検索結果に合致した歌詞サイト
	"""
	url = 'http://www.google.co.jp/search'
	param = {'q': title + ' 歌詞'}
	response = requests.get(url, params=param)
	soup = BeautifulSoup(response.text, 'html.parser')
	elems = soup.find_all('a')
	lyrics_sites = ['www.uta-net.com/', 'www.utamap.com', 'utaten.com/lyric/', 'j-lyric.net', 'www.kget.jp', 'kashinavi.com', 'joysound.com']
	match_list = []

	for elem in elems:
		for site in lyrics_sites:
			if site in elem.attrs['href']:
				match_list.append(elem.attrs['href'][7:].split('&')[0])

	return match_list
	

# global
temp_tableview_alpha = 0.0

# main
if __name__ == '__main__':
	args = sys.argv

	if len(args) < 2:
		console.alert('エラー', 'YouTubeの共有機能から起動して下さい', 'OK', hide_cancel_button=True)
		sys.exit()
		
	url = load_args(args)
	#url = appex.get_url()
	
	if not url:
		print('No URL')
		sys.exit()
	
	title = scraping(url)
	lryics_urls = search_google(title)
	
	view = ui.load_view('lyrics_search')
	#views = create_ui(view)
	
	# common UI
	segmentedcontrol = view['segmentedcontrol']
	# tableview UI
	tableview = view['tableview']
	tableview_button = view['tableview_button']
	# webview UI
	webview = view['webview']
	# search_tableview UI
	search_tableview = view['search_tableview']
	textfield = view['textfield']
	search_button =view['search_button']
	search_tableview_label = view['search_tableview_label']
	
	if lryics_urls:
		set_search_tableview(search_tableview, title)
		set_tableview(tableview, lryics_urls)
		#show_status()
	
	else:
		console.alert('歌詞が見つかりませんでした', '”再検索”ボタンを押して\n再検索してください', 'OK', hide_cancel_button=True)

		set_search_tableview(search_tableview, title)
		#show_status()
	
	view.present('sheet')


