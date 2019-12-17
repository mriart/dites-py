#-*- coding: utf-8 -*-

# dites
# Catalan dites, V3
# Marc Riart, marc_riart@es.ibm.com
# January 2017


import random
import datetime
import os
import re
from bottle import Bottle, run, route, static_file, request

# Load file
f = open('dites.txt', 'r')
jan = []
feb = []
mar = []
apr = []
may = []
jun = []
jul = []
aug = []
sep = []
ocb = []
nov = []
dec = []
misc = []
today = []

# Fill the lists, one per month, the misc and today
for line in f:
        lowerline = line.lower()
        no_month = False
        no_season = False

        if 'gener' in lowerline: jan.append(line)
        elif 'febrer' in lowerline: feb.append(line)
        elif 'març' in lowerline: mar.append(line)
        elif 'abril' in lowerline: apr.append(line)
        elif 'maig' in lowerline: may.append(line)
        elif 'juny' in lowerline: jun.append(line)
        elif 'juliol' in lowerline: jul.append(line)
        elif 'agost' in lowerline: aug.append(line)
        elif 'setembre' in lowerline: sep.append(line)
        elif 'octubre' in lowerline: ocb.append(line)
        elif 'novembre' in lowerline: nov.append(line)
        elif 'desembre' in lowerline: dec.append(line)
        else: no_month = True

        if 'hivern' in lowerline:
                dec.append(line)
                jan.append(line)
                feb.append(line)
        elif 'primavera' in lowerline:
                mar.append(line)
                apr.append(line)
                may.append(line)
        elif 'estiu' in lowerline:
                jun.append(line)
                jul.append(line)
                aug.append(line)                
        elif 'tardor' in lowerline:
                sep.append(line)
                ocb.append(line)
                nov.append(line)
        else:
                no_season = True

        if no_month and no_season:
                misc.append(line)

        if re.search('sant jordi|sant joan|tots sants|nadal|\([0-9]', line, re.I):
                today.append(line)

# Function to return the name of the month in catalan
def month_in_cat(n):
        if n == 1: return 'gener'
        elif n == 2: return 'febrer'
        elif n == 3: return 'març'
        elif n == 4: return 'abril'
        elif n == 5: return 'maig'
        elif n == 6: return 'juny'
        elif n == 7: return 'juliol'
        elif n == 8: return 'agost'
        elif n == 9: return 'setembre'
        elif n == 10: return 'octubre'
        elif n == 11: return 'novembre'
        elif n == 12: return 'desembre'
        else: return 'mes-incorrecte' 

        

app = Bottle()

@app.route('/')
def show():
        ret = ''
        html_pre = '''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/png" href="/res/favicon.png?"/>
<link rel="apple-touch-icon" sizes="128x128" href="/res/and-dites.jpg">
<style>
p {
        font-family: sans-serif;
        font-size: 24px;
}
button {
	background-color: #4CAF50; /* Green */
	border: none;
	color: white;
	padding: 15px 32px;
	text-align: center;
	text-decoration: none;
	display: inline-block;
	font-size: 16px;
	margin: 4px 2px;
	cursor: pointer;
	border-radius: 4px;
	width: 250px;
}
input {
	font-size: 16px;
	width: 250px;
}
</style>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script>
$(document).ready(function(){
    $("#btn1").click(function(){
       $("#p1").load("today");
    });
    $("#btn2").click(function(){
       $("#p1").load("misc");       
    });
    $("#btn3").click(function(){
       //pattern_value = $("input:text").val();
       pattern_value = $("#in1").val();
       url = "search?pattern=" + escape(pattern_value);
       $("#p1").load(url);
    });
});
</script>
</head>
<body>
<p id="p1" align="center">
'''
        html_post = '''
</p><br>
<div align="center">
	<button id="btn1">Una altra dita del dia</button><br><br>
	<button id="btn2">Altres dites</button><br><br>
	<input id="in1" type="text" name="pattern" onkeydown='if (event.keyCode == 13) document.getElementById("btn3").click();'/><br>
        <button id="btn3">Cerca</button>
</div>
</body>
</html>
'''
       
        # If there is a dita for today, return it
        # First, build the pattern for today() based on the present day

        # Testing
        #day = 23
        #month = 4 
        day = datetime.date.today().day
        month = datetime.date.today().month
        
        if day == 23 and month == 4: today_is = 'sant jordi'
        elif day == 24 and month == 6: today_is = 'sant joan'
        elif day == 1 and month == 11: today_is = 'tots sants'
        elif day == 25 and month == 12: today_is = 'nadal'
        else: today_is = '(' + str(day) + ' ' + month_in_cat(month)
        
        for line in today:
                if today_is in line.lower():
                        ret = ret + line + '<br>'
        
        if not ret == '':
                return html_pre + ret + html_post


        # If there is not a dita for today, return a random one        
        if month == 1: dita_avui = jan
        elif month == 2: dita_avui = feb
        elif month == 3: dita_avui = mar
        elif month == 4: dita_avui = apr
        elif month == 5: dita_avui = may
        elif month == 6: dita_avui = jun
        elif month == 7: dita_avui = jul
        elif month == 8: dita_avui = aug
        elif month == 9: dita_avui = sep
        elif month == 10: dita_avui = ocb
        elif month == 11: dita_avui = nov
        elif month == 12: dita_avui = dec
        else: dita_avui = misc
        n = random.randint(0, len(dita_avui)-1)
        
        return html_pre + dita_avui[n] + html_post


@app.route('/res/<filename>')
def image(filename):
    return static_file(filename, root='./res')


@app.route('/today')
def showtoday():
        month = datetime.date.today().month
        if month == 1: dita_avui = jan
        elif month == 2: dita_avui = feb
        elif month == 3: dita_avui = mar
        elif month == 4: dita_avui = apr
        elif month == 5: dita_avui = may
        elif month == 6: dita_avui = jun
        elif month == 7: dita_avui = jul
        elif month == 8: dita_avui = aug
        elif month == 9: dita_avui = sep
        elif month == 10: dita_avui = ocb
        elif month == 11: dita_avui = nov
        elif month == 12: dita_avui = dec
        else: dita_avui = misc

        n = random.randint(0, len(dita_avui)-1)
        ret = dita_avui[n]

        return ret


@app.route('/misc')
def showmisc():
        m = random.randint(0, len(misc)-1)
        ret = misc[m]
        return ret


@app.route('/search')
def do_search():
        f = open("dites.txt", "r")
        text = request.query['pattern']
        strings = text.lower().split()
        ret = ''
        for line in f:
                if all(s in line.lower() for s in strings):
                        ret = ret + line + '<br>'
        
        return ret


# Run in Bluemix or local (BX mandates port != 80)
run(app, host='0.0.0.0', port=8080)
