This is a simple book information search engine.
The data is retrived from three fiction website: Qidian, Zongheng, Youdu.

Required Python packages:  
	json, os, sqlite3, requests, bs4, datetime, time, re
	from fontTools.ttLib import TTFont
	from flask import Flask, render_template, request

Running Instruction:
	RUN the Code. No any other special steps.

Interaction Description:
	1. Run the code, open the page with (localhost:5000 or http://127.0.0.1:5000).
	2. On the Welcome page, the user can select "Book Search" or "Trends Review".
	3. Book Search: user can search books with specified category and size requirements.
	4. Trends Review: user can review 3 different kinds of book trends.
		i. trends1: top 20 most popular books' information on each website;
	       ii. trends2: type distribution within some time period (here user can choose the time zone)
	      iii. trends3: size change among different types.
