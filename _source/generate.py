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
copyfile(source_directory + "style.css", dest_directory+"style.css")

link_matcher = re.compile(r'\[([^\]]+)\]\(([^)]+)\)') # markdown link matcher

custom_word_matcher = re.compile(r'\$\{([^}]+)\}') # Mark 

copied_resources = set([])

def format_post(post_id):
	post = all_posts[post_id]
	post_date = post[1]
	post_title = post[0]
	target_dest = dest_directory
	post_link = post_id+".html"

	# Copy used files
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

	dest = open(target_dest+post_link, "wt")
	post_template = open(source_directory + "post_page.html", "rt")

	def word_changer(m): # Simply remove / for now
		w = m.group(1)
		if w == "POST_DATE": return post_date
		if w == "POST_TITLE": return post_title
		raise Exception("Invalid variable " + w + " in post_page.html")

	my_locals = {}
	my_globals = {}

	for line in post_template:
		if line != "<<content>>\n":
			line = custom_word_matcher.sub(word_changer, line)
			dest.write(line)
			continue

		tags = post[2]
		if len(tags) != 0:
			dest.write("tags: ")
			first = True
			for tag in sorted(tags):
				if not first: dest.write(", ")
			dest.write(tag)
			dest.write("\n\n")

		lines = post[3]
		in_python = False
		block = ""

		old_stdout = sys.stdout
		sys.stdout = dest

		for line in lines:
			if line == "{{python}}\n":
				if len(block)>=0:
					exec(block, my_locals, my_globals)
					block = ""
				in_python = False if in_python else True
			else:
				if in_python:
					block = block + line[1:]
				else:
					print(line[:-1])
			dest.flush()

	if len(block)>=0:
		exec(block, my_locals, my_globals)
	block = ""
	sys.stdout = old_stdout

	dest.close()
	post_template.close()


def parse_posts():
	filenames = next(os.walk(post_directory))[2]
	for post in filenames:
		if not post[-3:] == ".md":
			continue

		print("Processing " + post)

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
				#if line.startswith("#"): # TODO: This might intefer with python comments in python blocks.. oops
				#	num = len(line.split(" ")[0])+1
				#	line = "(" + ("#"*num) + ") " + line[num:]

				def link_patcher(m): # Simply remove / for now
					print("  Matched link " + m.group(0))
					link = m.group(2)
					if link.startswith("code/") or link.startswith("images/"):
						images.add(link)
						return m.group(0)

					if link[0] == '/':
						return "[" + m.group(1) + "](" + m.group(2)[1:] + ".html)" # TODO: Remove space here

					print("    External, not modifying")
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
