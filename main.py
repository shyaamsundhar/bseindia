import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS, cross_origin
import json
import urllib.request
# from IPython.display import display, HTML

dtf = pd.DataFrame()
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
  return 'Hello, Azure!'


@app.route('/equity',methods=['POST'])
def getequity():
    global dtf
    a=[]
    link=[]
    b=[]
    c=[]
    cnt=1
    while(cnt<10):
        urlink="https://www.bseindia.com/corporates/ann.aspx?curpg="+str(cnt)+"&annflag=1&dt=&dur=D&dtto=&cat=&scrip=&anntype=C"
        # linkz = '<a href="'+urlink+'" target = "_blank">link</a>'
        page = requests.get(urlink)
        soup = BeautifulSoup(page.content, 'html.parser')
        if(len(soup.findAll("td", class_="TTHeadergrey")) != 0):
            count = 0
            for i in soup.findAll("td", class_="TTHeadergrey"):
                while(count<4):
                    if(count == 0):
                        a.append(i.text)
                        link.append(urlink)
                    elif(count == 3):
                        count=-1
                    count =count+1
                    break
            for i in soup.findAll("td", class_="TTRow_leftnotices"):
                if(i.text != "" and i.text != " \xa0"):
                    b.append(i.text)
        else:
            print("Done")
            break
        cnt = cnt+20
    for i in range(0,len(a)):
        c.append([a[i]+'\\n'+b[i]])
    dtf = pd.DataFrame({'Company details':c})
    pd.set_option('display.max_colwidth', -4)
    HTML_file = open("http://127.0.0.1/templates/displaypage.html","w")
    HTML_file.write(''' <html> <head> <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"> </script> 
    <script>
    $(function() {
        $("#submitaction").click(function(){
             $.ajax({
                    url: "http://127.0.0.1:5000/search",
                    type: 'POST',
                    data : $('form').serialize(),
                    dataType :'json',
                    crossDomain : true,
                    success: function (data) {
                            window.location.href = "C:/Users/lenovo/Desktop/ASP .NET CORE 2/bse/templates/displaypage.html"
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
            });
            $("#reload").click(function(){
             $.ajax({
                    url: "http://127.0.0.1:5000/reload",
                    type: 'POST',
                    data : $('form').serialize(),
                    dataType :'json',
                    crossDomain : true,
                    success: function (data) {
                            window.location.href = "C:/Users/lenovo/Desktop/ASP .NET CORE 2/bse/templates/displaypage.html"
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
            });
        });
    </script>
<style>
    input[type=text] {
    width: 40%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 20px;
    text-align: center;
}
input[type=submit] {
    width: 8%;
    padding: 8px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 20px;
}
button[type=button] {
    width: 8%;
    padding: 8px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 20px;
}
        .dataframe {
            font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
            border-collapse: collapse;
            width: 100%;
            overflow: hidden;
        }

        .dataframe th {
            border: 1px solid #ddd;
            padding: 8px;
        }
        .dataframe tr{
        max-width : 50px; 
        white-space : nowrap;
        }

        .dataframe tr:nth-child(even) {
            background-color: #f2f2f2;
            overflow : hidden;
        }


        .dataframe tr:hover {
            background-color: #ddd;
        }

        .dataframe th {
            padding-top: -1px;
            padding-bottom: 0px;
            text-align: left;
            background-color: #ff4525;
            color: white;
        }

        .dataframe td {
            height: 60px;
        }

            .dataframe td > div {
                width: 100%;
                height: 100%;
                overflow: hidden;
            }
    </style> 
    </head> <body> <center><form><input type="text" id="cmpname" name="cmpname" placeholder="company name" /><input type="submit" id="submitaction" /></form></center><div class="table"> ''')
    HTML_file.write(dtf.to_html().replace("\\n","<br>"))
    HTML_file.write('''</div><center><button type="button" id="reload">View All</button><center></body></html> ''')
    HTML_file.close()
    return json.dumps({"result":"success"})

@app.route('/metf',methods=['POST'])
def getmetf():
    global dtf
    a=[]
    link=[]
    b=[]
    c=[]
    cnt=1
    while(cnt<10000):
        urlink="https://www.bseindia.com/corporates/ann.aspx?curpg="+str(cnt)+"&annflag=1&dt=&dur=D&dtto=&cat=&scrip=&anntype=M"
        # linkz = '<a href="'+urlink+'" target = "_blank">link</a>'
        page = requests.get(urlink)
        soup = BeautifulSoup(page.content, 'html.parser')
        if(len(soup.findAll("td", class_="TTHeadergrey")) != 0):
            count = 0
            for i in soup.findAll("td", class_="TTHeadergrey"):
                while(count<4):
                    if(count == 0):
                        a.append(i.text)
                        link.append(urlink)
                    elif(count == 3):
                        count=-1
                    count =count+1
                    break
            for i in soup.findAll("td", class_="TTRow_leftnotices"):
                if(i.text != "" and i.text != " \xa0"):
                    b.append(i.text)
        else:
            print("Done")
            break
        cnt = cnt+20
    for i in range(0,len(a)):
        c.append(a[i]+"\\n"+b[i])
    dtf = pd.DataFrame({'Company details':c})
    pd.set_option('display.max_colwidth', -4)
    HTML_file = open("C:/Users/lenovo/Desktop/ASP .NET CORE 2/bse/templates/displaypage.html","w")
    HTML_file.write(''' <html> <head> <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"> </script> 
    <script>
    $(function() {
        $("#submitaction").click(function(){
             $.ajax({
                    url: "http://127.0.0.1:5000/search",
                    type: 'POST',
                    data : $('form').serialize(),
                    dataType :'json',
                    crossDomain : true,
                    success: function (data) {
                            window.location.href = "C:/Users/lenovo/Desktop/ASP .NET CORE 2/bse/templates/displaypage.html"
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
            });
            $("#reload").click(function(){
             $.ajax({
                    url: "http://127.0.0.1:5000/reload",
                    type: 'POST',
                    data : $('form').serialize(),
                    dataType :'json',
                    crossDomain : true,
                    success: function (data) {
                            window.location.href = "C:/Users/lenovo/Desktop/ASP .NET CORE 2/bse/templates/displaypage.html"
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
            });
        });
    </script>
    
<style>
    input[type=text] {
    width: 40%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 20px;
    text-align: center;
}
input[type=submit] {
    width: 8%;
    padding: 8px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 20px;
}
button[type=button] {
    width: 8%;
    padding: 8px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 20px;
}
        .dataframe {
            font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
            border-collapse: collapse;
            width: 100%;
            overflow: hidden;
        }

        .dataframe th {
            border: 1px solid #ddd;
            padding: 8px;
        }
        .dataframe tr{
        max-width : 50px; 
        white-space : nowrap;
        }

        .dataframe tr:nth-child(even) {
            background-color: #f2f2f2;
            overflow : hidden;
        }


        .dataframe tr:hover {
            background-color: #ddd;
        }

        .dataframe th {
            padding-top: -1px;
            padding-bottom: 0px;
            text-align: left;
            background-color: #ff4525;
            color: white;
        }

        .dataframe td {
            height: 60px;
        }

            .dataframe td > div {
                width: 100%;
                height: 100%;
                overflow: hidden;
            }
    </style> 
    </head> <body> <center><form><input type="text" id="cmpname" name="cmpname" placeholder="company name" /><input type="submit" id="submitaction" /></form></center><div class="table"> ''')
    HTML_file.write(dtf.to_html().replace("\\n","<br>"))
    HTML_file.write('''</div><center><button type="button" id="reload">View All</button><center></body></html> ''')
    HTML_file.close()
    return json.dumps({"result":"success"})

@app.route('/debt',methods=['POST'])
def getdebt():
    global dtf
    a=[]
    link=[]
    b=[]
    c=[]
    cnt=1
    while(cnt<10000):
        urlink="https://www.bseindia.com/corporates/ann.aspx?curpg="+str(cnt)+"&annflag=1&dt=&dur=D&dtto=&cat=&scrip=&anntype=D"
        # linkz = '<a href="'+urlink+'" target = "_blank">link</a>'
        page = requests.get(urlink)
        soup = BeautifulSoup(page.content, 'html.parser')
        if(len(soup.findAll("td", class_="TTHeadergrey")) != 0):
            count = 0
            for i in soup.findAll("td", class_="TTHeadergrey"):
                while(count<4):
                    if(count == 0):
                        a.append(i.text)
                        link.append(urlink)
                    elif(count == 3):
                        count=-1
                    count =count+1
                    break
            for i in soup.findAll("td", class_="TTRow_leftnotices"):
                if(i.text != "" and i.text != " \xa0"):
                    b.append(i.text)
        else:
            print("Done")
            break
        cnt = cnt+20
    for i in range(0,len(a)):
        c.append(a[i]+"\\n"+b[i])
    dtf = pd.DataFrame({'Company details':c})
    pd.set_option('display.max_colwidth', -4)
    HTML_file = open("C:/Users/lenovo/Desktop/ASP .NET CORE 2/bse/templates/displaypage.html","w")
    HTML_file.write(''' <html> <head> <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"> </script> 
    <script>
    $(function() {
        $("#submitaction").click(function(){
             $.ajax({
                    url: "http://127.0.0.1:5000/search",
                    type: 'POST',
                    data : $('form').serialize(),
                    dataType :'json',
                    crossDomain : true,
                    success: function (data) {
                            window.location.href = "C:/Users/lenovo/Desktop/ASP .NET CORE 2/bse/templates/displaypage.html"
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
            });
            $("#reload").click(function(){
             $.ajax({
                    url: "http://127.0.0.1:5000/reload",
                    type: 'POST',
                    data : $('form').serialize(),
                    dataType :'json',
                    crossDomain : true,
                    success: function (data) {
                            window.location.href = "C:/Users/lenovo/Desktop/ASP .NET CORE 2/bse/templates/displaypage.html"
                    },
                    error: function (error) {
                        console.log(error);
                    }
                });
            });
        });
    </script>
    
<style>
    input[type=text] {
    width: 40%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 20px;
    text-align: center;
}
input[type=submit] {
    width: 8%;
    padding: 8px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 20px;
}
button[type=button] {
    width: 8%;
    padding: 8px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 20px;
}
        .dataframe {
            font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
            border-collapse: collapse;
            width: 100%;
            overflow: hidden;
        }

        .dataframe th {
            border: 1px solid #ddd;
            padding: 8px;
        }
        .dataframe tr{
        max-width : 50px; 
        white-space : nowrap;
        }

        .dataframe tr:nth-child(even) {
            background-color: #f2f2f2;
            overflow : hidden;
        }


        .dataframe tr:hover {
            background-color: #ddd;
        }

        .dataframe th {
            padding-top: -1px;
            padding-bottom: 0px;
            text-align: left;
            background-color: #ff4525;
            color: white;
        }

        .dataframe td {
            height: 60px;
        }

            .dataframe td > div {
                width: 100%;
                height: 100%;
                overflow: hidden;
            }
    </style> 
    </head> <body> <center><form><input type="text" id="cmpname" name="cmpname" placeholder="company name" /><input type="submit" id="submitaction" /></form></center><div class="table"> ''')
    HTML_file.write(dtf.to_html().replace("\\n","<br>"))
    HTML_file.write('''</div><center><button type="button" id="reload">View All</button><center></body></html> ''')
    HTML_file.close()
    return json.dumps({"result":"success"})


@app.route('/manda',methods=['POST'])
def getmanda():
    global dtf
    a=[]
    b=[]
    c=[]
    d=[]
    cnt=1
    while(cnt<10000):
        urlink="https://www.bseindia.com/corporates/ann.aspx?curpg="+str(cnt)+"&annflag=1&dt=&dur=D&dtto=&cat=&scrip=&anntype=C"
        print(urlink)
        page = requests.get(urlink)
        soup = BeautifulSoup(page.content, 'html.parser')
        if(len(soup.findAll("td", class_="TTHeadergrey")) != 0):
            count = 0
            for i in soup.findAll("td", class_="TTHeadergrey"):
                while(count<4):
                    if(count == 0):
                        a.append(i.text)
                    elif(count == 3):
                        count=-1
                    count =count+1
                    break
            for i in soup.findAll("td", class_="TTRow_leftnotices"):
                if(i.text != "" and i.text != " \xa0"):
                    b.append(i.text)
        else:
            print("Done")
            break
        cnt = cnt+20
    for i in range(0,len(a)):
        c.append(a[i]+"\\n"+b[i])
    dtfn = pd.DataFrame({'Company details':c})
    for i in dtfn['Company details']:
        if("SAST" in i or "Acquisition" in i):
            d.append(i)
    dtf = pd.DataFrame({'Company details': d})
    pd.set_option('display.max_colwidth', -1)
    HTML_file = open("C:/Users/lenovo/Desktop/ASP .NET CORE 2/bse/templates/displaypage.html","w")
    HTML_file.write(''' <html> <head> <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"> </script> 
    <script>
    $(function() {
         $("#submitaction").click(function(){
             $.ajax({
                    url: "http://127.0.0.1:5000/search",
                    type: 'POST',
                    data : $('form').serialize(),
                    dataType :'json',
                    crossDomain : true,
                    success: function (data) {
                            window.location.href = "C:/Users/lenovo/Desktop/ASP .NET CORE 2/bse/templates/displaypage.html"
                    },
                    error: function (error) {
                        // $('#errormsg').css('color','red')
                        // $('#errormsg').text("Connection error")
                        console.log(error);
                    }
                });
            });
            $("#reload").click(function(){
             $.ajax({
                    url: "http://127.0.0.1:5000/reload",
                    type: 'POST',
                    data : $('form').serialize(),
                    dataType :'json',
                    crossDomain : true,
                    success: function (data) {
                            window.location.href = "C:/Users/lenovo/Desktop/ASP .NET CORE 2/bse/templates/displaypage.html"
                    },
                    error: function (error) {
                        // $('#errormsg').css('color','red')
                        // $('#errormsg').text("Connection error")
                        console.log(error);
                    }
                });
            });
    });
    </script>
    
   <style>
    input[type=text] {
    width: 40%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 20px;
    text-align: center;
}
input[type=submit] {
    width: 8%;
    padding: 8px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 20px;
}
button[type=button] {
    width: 8%;
    padding: 8px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 20px;
}
        .dataframe {
            font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
            border-collapse: collapse;
            width: 100%;
            overflow: hidden;
        }

        .dataframe th {
            border: 1px solid #ddd;
            padding: 8px;
        }
        .dataframe tr{
        max-width : 50px; 
        white-space : nowrap;
        }

        .dataframe tr:nth-child(even) {
            background-color: #f2f2f2;
            overflow : hidden;
        }


        .dataframe tr:hover {
            background-color: #ddd;
        }

        .dataframe th {
            padding-top: -1px;
            padding-bottom: 0px;
            text-align: left;
            background-color: #ff4525;
            color: white;
        }

        .dataframe td {
            height: 60px;
        }

            .dataframe td > div {
                width: 100%;
                height: 100%;
                overflow: hidden;
            }
    </style>
     </head> <body> <center><form><input type="text" id="cmpname" name="cmpname" placeholder="company name" /><button type="button" id="submitaction">Search</button></form></center> ''')
    HTML_file.write(dtf.to_html().replace("\\n","<br>"))
    HTML_file.write('''<center><button type="button" id="reload">View All</button><center></body></html> ''')
    HTML_file.close()
    return json.dumps({"result":"success"})


@app.route('/search',methods=['POST'])
def getsearch():
    d =[]
    _cmpname = request.form['cmpname']
    for i in dtf['Company details']:
        print(i)
        if(_cmpname.lower() in i[0] or _cmpname.upper() in i[0] or _cmpname.title() in i[0] or _cmpname in i[0]):
            d.append(i)
    newdf = pd.DataFrame({'Company details':d})
    pd.set_option('display.max_colwidth', -1)
    HTML_file = open("C:/Users/lenovo/Desktop/ASP .NET CORE 2/bse/templates/displaypage.html","w")
    HTML_file.write(''' <html> <head> <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"> </script> 
    <script>
    $(function() {
        $("#submitaction").click(function(){
            $.ajax({
                        url: "http://127.0.0.1:5000/search",
                        type: 'POST',
                        data : $('form').serialize(),
                        dataType :'json',
                        crossDomain : true,
                        success: function (data) {
                                window.location.href = "C:/Users/lenovo/Desktop/ASP .NET CORE 2/bse/templates/displaypage.html"
                        },
                        error: function (error) {
                            // $('#errormsg').css('color','red')
                            // $('#errormsg').text("Connection error")
                            console.log(error);
                        }
                    });
                });
                $("#reload").click(function(){
                $.ajax({
                        url: "http://127.0.0.1:5000/reload",
                        type: 'POST',
                        data : $('form').serialize(),
                        dataType :'json',
                        crossDomain : true,
                        success: function (data) {
                                window.location.href = "C:/Users/lenovo/Desktop/ASP .NET CORE 2/bse/templates/displaypage.html"
                        },
                        error: function (error) {
                            // $('#errormsg').css('color','red')
                            // $('#errormsg').text("Connection error")
                            console.log(error);
                        }
                    });
                });
        });
        </script>
        <style>
        input[type=text] {
        width: 40%;
        padding: 12px 20px;
        margin: 8px 0;
        box-sizing: border-box;
        border-radius: 20px;
        text-align: center;
    }
    input[type=submit] {
        width: 8%;
        padding: 8px 20px;
        margin: 8px 0;
        box-sizing: border-box;
        border-radius: 20px;
    }
    button[type=button] {
        width: 8%;
        padding: 8px 20px;
        margin: 8px 0;
        box-sizing: border-box;
        border-radius: 20px;
    }
            .dataframe {
                font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
                border-collapse: collapse;
                width: 100%;
                overflow: hidden;
            }

            .dataframe th {
                border: 1px solid #ddd;
                padding: 8px;
            }
            .dataframe tr{
            max-width : 50px; 
            white-space : nowrap;
            }

            .dataframe tr:nth-child(even) {
                background-color: #f2f2f2;
                overflow : hidden;
            }


            .dataframe tr:hover {
                background-color: #ddd;
            }

            .dataframe th {
                padding-top: -1px;
                padding-bottom: 0px;
                text-align: left;
                background-color: #ff4525;
                color: white;
            }

            .dataframe td {
                height: 20px;
            }

                .dataframe td > div {
                    width: 100%;
                    height: 100%;
                    overflow: hidden;
                }
        </style>
        </head> <body> <center><form><input type="text" id="cmpname" name="cmpname" placeholder="company name" /><button type="button" id="submitaction">Search</button></form></center> ''')
    HTML_file.write(newdf.to_html().replace("\\n","<br>"))
    HTML_file.write('''<center><button type="button" id="reload">View All</button><center></body></html> ''')
    HTML_file.close()
    return json.dumps({"result":"success"})


@app.route('/reload',methods=['POST'])
def getreload():
    pd.set_option('display.max_colwidth', -1)
    HTML_file = open("C:/Users/lenovo/Desktop/ASP .NET CORE 2/bse/templates/displaypage.html","w")
    HTML_file.write(''' <html> <head> <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"> </script> 
    <script>
    $(function() {
         $("#submitaction").click(function(){
             $.ajax({
                    url: "http://127.0.0.1:5000/search",
                    type: 'POST',
                    data : $('form').serialize(),
                    dataType :'json',
                    crossDomain : true,
                    success: function (data) {
                            window.location.href = "C:/Users/lenovo/Desktop/ASP .NET CORE 2/bse/templates/displaypage.html"
                    },
                    error: function (error) {
                        // $('#errormsg').css('color','red')
                        // $('#errormsg').text("Connection error")
                        console.log(error);
                    }
                });
            });

            $("#reload").click(function(){
             $.ajax({
                    url: "http://127.0.0.1:5000/reload",
                    type: 'POST',
                    data : $('form').serialize(),
                    dataType :'json',
                    crossDomain : true,
                    success: function (data) {
                            window.location.href = "C:/Users/lenovo/Desktop/ASP .NET CORE 2/bse/templates/displaypage.html"
                    },
                    error: function (error) {
                        // $('#errormsg').css('color','red')
                        // $('#errormsg').text("Connection error")
                        console.log(error);
                    }
                });
            });
    });
    </script>
    <style>
    input[type=text] {
    width: 40%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 20px;
    text-align: center;
}
input[type=submit] {
    width: 8%;
    padding: 8px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 20px;
}
button[type=button] {
    width: 8%;
    padding: 8px 20px;
    margin: 8px 0;
    box-sizing: border-box;
    border-radius: 20px;
}
        .dataframe {
            font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
            border-collapse: collapse;
            width: 100%;
            overflow: hidden;
        }

        .dataframe th {
            border: 1px solid #ddd;
            padding: 8px;
        }
        .dataframe tr{
        max-width : 50px; 
        white-space : nowrap;
        }

        .dataframe tr:nth-child(even) {
            background-color: #f2f2f2;
            overflow : hidden;
        }


        .dataframe tr:hover {
            background-color: #ddd;
        }

        .dataframe th {
            padding-top: -1px;
            padding-bottom: 0px;
            text-align: left;
            background-color: #ff4525;
            color: white;
        }

        .dataframe td {
            height: 20px;
        }

            .dataframe td > div {
                width: 100%;
                height: 100%;
                overflow: hidden;
            }
    </style> </head> <body> <center><form><input type="text" id="cmpname" name="cmpname" placeholder="company name" /><button type="button" id="submitaction">Search</button></form></center> ''')
    HTML_file.write(dtf.to_html().replace("\\n","<br>"))
    HTML_file.write('''<center><button type="button" id="reload">View All</button><center></body></html> ''')
    HTML_file.close()
    return json.dumps({"result":"success"})


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='192.168.3.145')