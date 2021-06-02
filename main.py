import requests
import argparse
import datetime
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

def date_epoch(e):
	dt = datetime.datetime.fromtimestamp(e)
	return dt.strftime("%d %b %Y")

# api urls
codechefURL = 'https://www.codechef.com/api/list/contests/all?sort_by=END&sorting_order=desc&offset=0'
codeforcesURL = 'https://codeforces.com/api/contest.list/'
atcoderURL = "https://atcoder.jp/contests/"

#platforms
platforms = {
	1: "codechef",
	2: "codeforces",
	3: "atcoder"
}

#decss
TITLE = 'Contest Lister CLI'
DESC = '''Simple CLI tool thats lists out all the upcoming coding challanges from different platforms.\n
'''
EPILOG = '''
More platforms will be added soon.
(Developer: Namah Jain,\n
Github: nanorex\n)
'''
P_HELP = 'list by specific platform id, by default it lists all the available platforms'
PT_HELP = "list all the platforms with id's."

#list platforms 
def list_platforms():
	print( Fore.YELLOW + "Currently available platforms with ids")
	for i in platforms:
		print ( Fore.GREEN + Style.BRIGHT + str(i)+": " + Style.RESET_ALL + platforms[i])

#get all atcoder contests
def d_atcoder():
	response = requests.get(atcoderURL)
	soup = BeautifulSoup(response.text, "html.parser")
	div = soup.find("div", id="contest-table-upcoming")
	data = []
	for tr in div.find_all("tr")[1:]:
		d = {}
		tds = tr.find_all("td")
		d["time"] = tds[0].a.time.text[0:10]
		d["name"] = tds[1].a.text
		d["duration"] = tds[2].text
		d["url"] = atcoderURL+tds[1].a["href"][10:]
		d["id"] = tds[1].a["href"][10:]
		data.append(d)
	return data

# get all the upcoming codechef contests
def d_codechef():
	response = requests.get(codechefURL)
	j = response.json()
	return j['future_contests']

# get all upcoming codeforces contests
def d_codeforces():
	response = requests.get(codeforcesURL)
	r = []
	data = response.json()
	for contest in data['result']:
		if contest["phase"] == 'FINISHED':
			break
		r.append(contest)
	return r


#blit codechef contests
def blit_codechef(data):
	if len(data)==0:
		print(Fore.RED + "\n[ - ] CodeChef - "+"https://www.codechef.com")
		print("\tNo upcoming contests")
		print(Style.RESET_ALL)
		return
	print(Fore.GREEN + Style.BRIGHT+"\n[ + ]"+Style.RESET_ALL+" CodeChef - "+"https://www.codechef.com")
	for contest in data:
		print(Fore.CYAN+" [*] "+contest["contest_code"])
		print(Fore.YELLOW+"\tName:  "+Style.RESET_ALL+contest["contest_name"])
		print(Fore.YELLOW+"\tStart: "+Style.RESET_ALL+contest["contest_start_date"])
		print(Fore.YELLOW+"\tEnd:   "+Style.RESET_ALL+contest["contest_end_date"])
		print(Fore.YELLOW+"\tURL:   "+Style.RESET_ALL+"https://www.codechef.com/"+contest["contest_code"])

def blit_codeforces(data):
	if len(data)==0:
		print(Fore.RED + "\n[ - ] Codeforces - "+"https://www.codeforces.com")
		print("\tNo upcoming contests")
		print(Style.RESET_ALL)
		return
	print(Fore.GREEN + Style.BRIGHT+"\n[ + ]"+Style.RESET_ALL+" Codeforces - "+"https://www.codeforces.com")
	for contest in data:
		print(Fore.CYAN+" [*] " + str(contest["id"]))
		print(Fore.YELLOW+"\tName:     "+Style.RESET_ALL+contest["name"])
		print(Fore.YELLOW+"\tType:     "+Style.RESET_ALL+contest["type"])
		print(Fore.YELLOW+"\tDuration: "+Style.RESET_ALL+str(contest["durationSeconds"]/3600)+"hrs")
		print(Fore.YELLOW+"\tStart:    "+Style.RESET_ALL+date_epoch(contest["startTimeSeconds"]))
		print(Fore.YELLOW+"\tURL:      "+Style.RESET_ALL+"https://codeforces.com/contests/"+str(contest["id"]))

def blit_atcoder(data):
	if len(data)==0:
		print(Fore.RED + "\n[ - ] Atcoder - "+"https://www.atcoder.jp")
		print("\tNo upcoming contests")
		print(Style.RESET_ALL)
		return
	print(Fore.GREEN + Style.BRIGHT+"\n[ + ]"+Style.RESET_ALL+" Atcoder - "+"https://www.atcoder.jp")
	for contest in data:
		print(Fore.CYAN+" [*] " + str(contest["id"]))
		print(Fore.YELLOW+"\tName:    "+Style.RESET_ALL+contest["name"])
		print(Fore.YELLOW+"\tDuration:"+Style.RESET_ALL+contest["duration"]+"hrs")
		print(Fore.YELLOW+"\tStart:   "+Style.RESET_ALL+contest["time"])
		print(Fore.YELLOW+"\tURL:     "+Style.RESET_ALL+contest["url"])

def main():
	#initialize colorama escape codes
	init()
	parser = argparse.ArgumentParser(prog=TITLE, epilog=EPILOG)
	parser.add_argument('-p','-platforms',type=int,help=P_HELP,nargs="+",default=platforms.keys())
	parser.add_argument('-l','-list',action='store_true',help=PT_HELP)
	args = parser.parse_args()
	
	if args.l:
		list_platforms()
		return

	print(" [ ] Loading Data...")

	loader_data = {}
	for i in args.p:
		if platforms[i] == 'codechef':
			loader_data['codechef'] = d_codechef()
		elif platforms[i] == 'codeforces':
			loader_data['codeforces'] = d_codeforces()
		elif platforms[i] == 'atcoder':
			loader_data['atcoder'] = d_atcoder()

	print(Fore.GREEN+" [ ] Loaded")
	if 'codechef' in loader_data:
		blit_codechef(loader_data['codechef'])
	if 'codeforces' in loader_data:
		blit_codeforces(loader_data['codeforces'])
	if 'atcoder' in loader_data:
		blit_atcoder(loader_data['atcoder'])
		
if __name__ == '__main__':
	main()