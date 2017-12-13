# This blog generator is very naive but it is mine!
# https://regex101.com/

import os
from os import listdir
from os.path import isfile
from os.path import dirname
from os import makedirs
from shutil import copyfile
import sys
import re

all_posts = {}
all_landing_pages = { "index": [] }

dest_directory = "../"
source_directory = "./"
post_directory = source_directory

try:
	makedirs(dest_directory)
except:
	pass

copyfile(source_directory + "markdeep.min.js", dest_directory+"markdeep.min.js")

link_matcher = re.compile(r'\[([^\]]+)\]\(([^)]+)\)') # Links that starts with /

def start_markdown(dest, title, date):
	dest.write("<meta charset=\"utf-8\"><style class=\"fallback\">body{visibility:hidden;}</style>\n")
	dest.write("**" + title+"**\n")
	dest.write("\t\t\t\tAnders Lindqvist - " + date + " - [index](index.html)\n")

def stop_markdown(dest):
	dest.write("<!-- Markdeep: --><style class=\"fallback\">body{visibility:hidden;white-space:pre;font-family:monospace}</style><script src=\"markdeep.min.js\"></script><script src=\"https://casual-effects.com/markdeep/latest/markdeep.min.js\"></script><script>window.alreadyProcessedMarkdeep||(document.body.style.visibility=\"visible\")</script>")

copied_resources = set([])

def format_post(post_id):

	post = all_posts[post_id]
	post_date = post[1]
	post_title = post[0]
	target_dest = dest_directory
	post_link = post_id+".html"

	dest = open(target_dest+post_link, "wt")

	for img in post[4]:
		src = post_directory + img
		dst = target_dest + img

		if dst in copied_resources:
			continue
		copied_resources.add(dst)

		try:
			p = dirname(dst)
			if len(p)>0:
				makedirs(p)
		except:
			pass
		copyfile(src, dst)

	start_markdown(dest, post[0], post_date)

	tags = post[2]
	if len(tags) != 0:
		dest.write("tags: ")
		for tag in sorted(tags):
			dest.write(tag + ", ")
		dest.write("\n\n")

	lines = post[3]
	in_python = False
	block = ""

	old_stdout = sys.stdout
	sys.stdout = dest

	for line in lines:
		if line == "{{python}}\n":
			if len(block)>=0:
				exec(block)
				block = ""
			in_python = False if in_python else True
		else:
			if in_python:
				block = block + line[1:]
			else:
				print(line[:-1])
		dest.flush()

	if len(block)>=0:
		exec(block)
	block = ""
	sys.stdout = old_stdout

	stop_markdown(dest)

def parse_posts():
	filenames = next(os.walk(post_directory))[2]
	for post in filenames:
		if not post[-3:] == ".md":
			continue

		f = open(post_directory + post)

		identifier = post[:-3]

		state = 0
		images = set([])
		tags = set([])
		themes = set([])
		landings = set([])
		title = None
		date = None
		content = []

		for line in f:
			if state == 2:
				if line.startswith("#"): # TODO: This might intefer with python comments in python blocks.. oops
					num = len(line.split(" ")[0])+1
					line = "(" + ("#"*num) + ") " + line[num:]

				def link_patcher(m): # Simply remove / for now
					link = m.group(2)
					if link.startswith("code/") or link.startswith("images/"):
						images.add(link)
						return m.group(0)

					if link[0] == '/':
						print("\""+m.group(0)+"\"")
						return "[" + m.group(1) + "](" + m.group(2) + ".html)" # TODO: Remove space here
					return m.group(0)

				line = link_matcher.sub(link_patcher, line)

				content.append(line)

			elif state == 0:
				if line != "---\n":
					print("Post " + post + " does not have header!")
					return False
				state = 1
			elif state == 1:
				if line == "---\n":
					state = 2
				else:
					s = line.split(":")
					if s[0] == "title":
						title = line[7:-1]
					elif s[0] == "date":
						date = line[6:-1]
					elif s[0] == "tags":
						yo = line[6:-1].split(", ")
						for tag in yo:
							tags.add(tag)
					elif s[0] == "landing":
						yo = line[9:-1].split(", ")
						for landing in yo:
							landings.add(landing)
					elif s[0] == "theme":
						yo = line[7:-1].split(", ")
						for theme in yo:
							themes.add(theme)

		if len(landings)==0:
			landings.add("index")

		print(identifier + " " + str(landings))

		all_posts[identifier] = (title, date, tags, content, images, themes)

		for landing in landings:
			if not landing in all_landing_pages: all_landing_pages[landing]=[]
			all_landing_pages[landing].append(identifier)

		f.close()
	return True


if not parse_posts():
	print("Error")

print("---")

def write_post_index(dest, post_names, title):
	dest.write("# " + title + " (" + str(len(post_names)) + ")\n")
	dest.write("\n")

	by_dates = {}
	for post in post_names:
		date = all_posts[post][1]
		if post in by_dates:
			print("Date already found when adding post " + post + " at date "+ date)
		by_dates[date] = post
	for post_date in reversed(sorted(by_dates)):
		post_id = by_dates[post_date]
		post = all_posts[post_id]
		post_title = post[0]
		target_dest = dest_directory
		post_link = post_id+".html"
		dest.write("* [" + post_date + " - " + post_title + "]("+post_link+")\n")
	dest.write("\n")

def write_posts(post_names):
	for post_id in post_names:
		format_post(post_id)

for post in all_posts:
	format_post(post)

for landing in all_landing_pages:
	index = open(source_directory + "index_page.html")
	dest = open(dest_directory + landing + ".html", "wt")

	post_names = all_landing_pages[landing]

	theme_pages = {}

	for p in post_names:
		post = all_posts[p]
		themes = post[5]
		for theme in themes:
			if not theme in theme_pages: theme_pages[theme]=[]
			theme_pages[theme].append(p)

	for line in index:
		if line == "<<themes>>\n":
			for theme in theme_pages:
				theme_name = theme[0].upper() + theme[1:]
				write_post_index(dest, theme_pages[theme], theme_name)
		elif line == "<<posts>>\n":
			write_post_index(dest, post_names, "All Posts")
		else:
			dest.write(line)
