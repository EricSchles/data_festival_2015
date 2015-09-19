#Introduction

##About Me

* [My github](https://github.com/EricSchles)
* [My Linkedin](https://www.linkedin.com/pub/eric-schles/29/248/22)

###Life Goals:

* End Slavery
* Stop or slow climate change
* Ensure the rights and freedoms of all around the world

###Open collaborations and people who I think are awesome
* [heatseaknyc](https://github.com/heatseeknyc/heatseeknyc)
* [wikitongues](https://github.com/wikitongues)
* [demand abolition](http://www.demandabolition.org/)

##Outline

* GIS systems (for free)
	* [Leaflet.js](http://leafletjs.com/)
	* [geopy](https://geopy.readthedocs.org/en/1.10.0/)
	* [shapely](https://pypi.python.org/pypi/Shapely)

* Time Series Tools
	* Visualization
		* [c3.js](http://c3js.org/)		
	* Prediction
		* ARIMA Model

* Data Ingestion Piece
	* Currently
		* [investa_gator](https://github.com/EricSchles/investa_gator_v2)
		* [homelessness data](http://www.coalitionforthehomeless.org/the-catastrophe-of-homelessness/facts-about-homelessness/)
	* Future Plans
		* Economic Factors
		* Housing Factors
		* Political Factors
		* Service Factors (help for the underprivileged)
		* Law Enforcement Factors
		* Crime Factors

##Background on Human Trafficking

Human Trafficking is defined as five major types of slavery:
	* Sex Trafficking: Buying a person for sex

	* Child Sex Trafficking: Buying a child for sex

	* Labor Trafficking: Forcing someone to work for no money or other compensation against their will or without consent

	* Bondage: Classical definition of being a slave

	* Forced Servitude: forced to repay a debt without compensation, you are paying down your time instead of being paid

Human Trafficking is a deeply complex issue and these five major facities are occurring all over the world - sometimes where you'd least expect it.  With my time at the manhattan DA's office we saw a lot of sex trafficking (the most prevalent in america) but there was also some labor trafficking, with the assumption that we weren't able to find a lot of it.

So how do we stop this from happening?  

Human Trafficking __does__ __not__ happen in a vacuum.  It is the confluence of a number of contributing factors.  By understanding what those leading contributing factors are and controlling them, we will move towards a society where human trafficking is far less prodominant.  Then it will be the job of law enforcement to stamp out the small instances of it.  I don't think it's possible to ever completely get rid of the problem, but I believe reduction on the order of 80-90% is possible.  

In order to accomplish this, we'll need a systematic approach.  And so I've begun work on such a system, which I will present today.

To understand this system and it's intention, I'll speak high level about it's goals and then we'll go through the salient technical pieces.

The goals of this system are to provide policy makers and average person the tools they need to understand the largest contributing factors in their area.  And from there, to enact change at the policy level and at the local level.  Often times, people ask me how they can help.  And I can tell them things, but really the answer is sometimes none of us know what will be the best use of a persons time.  And this analysis is geared towards answering that question, with automation.  

The goal is to not need anyone to tell you what you should be doing, but for you to know what the largest way you can personally help stop or limit slavery where you live, in the way that will have the most impact.

At the end of the day, Human Trafficking is merely the product of the extremes in inequality of wealth.  

However certain types of inequality tend to contribute more than others.  For instance, typically a higher education means you'll be less likely to be sex trafficked or if you are sex trafficked it is more likely to not be a permanent staple of your life.  

[This article](http://www.cracked.com/personal-experiences-1440-5-things-i-learned-as-sex-slave-in-modern-america.html) details the journey of a young women who was sex trafficked as a child.  It's a very sad story, but she manages to get out.  And ends up leading a "normal" life.  One of the reasons for this is she did well in school - this means she had developed other skills and therefore was not forced to rely on prostitution for any meager form of survival.  Often times, when someone is forced into the world of sex trafficking at a young age, they cannot learn new skills, from years of mental abuse and have few options to make any money.  So even if they escape their trafficker, they are forced back into the world to survive, paid a meager salary, and constantly threatened with violence.  

Truly not an optimal path.  

This story and pattern suggest that it is possible to overcome slavery with proper services and educational resources.  However this is not the only required set of resources.  If you have no money to pursue further education or housing, then you are likely to continue to fall prey to these set of circumstances.  So instead what I propose is that a person who was trafficked or is suspectiable to to trafficking requires a basket of resources.  And depending on the area, different resources will be needed in different porportions.  

##An example system

In order to understand the contributing factors for slavery we'll need a lot of data.  Unfortunately, this data does not completely exist.  Sex trafficking has the most data available since commercial sex is advertised readily on the internet.  As a result we have the opportunity to combat this problem directly.  Determining how to address similar lines of reasoning for labor trafficking and child sex trafficking will be the subject of future talks.  

Note:  The primary user of this system is for a researcher working in a policy role with access to law enforcement data or a specialized law enforcement unit fighting sex trafficking.  

###Getting the data

In order to extract the important data and establish uniqueness of advertisers (and therefore size of the market) we'll look at hard attributes, specifically phone numbers and addresses.  Addresses will let us know how densely certain areas are affected.  And phone numbers will let us know how many unique players we have in a certain area.  In order to get these two attributes from backpage ads ( a major commercial sex website) I have written the following classes:

* ParsePhoneNumber
* ParseAddress

They can be found [here](https://github.com/EricSchles/data_festival_2015/blob/master/full_app/app/tools.py)

####Grabbing Phone Numbers

In order to make law enforcement's lives harder, traffickers have used various techniques to obfuscate phone numbers within backpage ads.

For 1 instance888 this 451 sent5ence has4 a 89 phone number in it.

Also, One Eighteighteight this 45OnE sentence 5 has 4 89 a phone number in it.

As you can see, these phone numbers are not easy to find.  Or see and so it loses them some business, but it also means law enforcement can't get to these numbers programmatically as easily.  ParsePhoneNumber addresses this obfuscation issue by making use of a sliding window to grab each of the numbers individually and append them to a list.  And once the list is long enough to be a valid phone number, it is appended to a list of possible phone numbers, which is verified against twilio's phone number verification api.  A wonderful and FREE tool.  (twilio costs money but the api doesn't)  Special thanks to Rob Spectre who gave me early access to this tool, helping me find instances of trafficking much more easily.  

So we'll attack these issues one at a time - First we need all the spelled words to be in either uppercase or lower case.  And we want all spelled numbers to be their numeric representation:

```
#text is a string
def _letter_to_number(self,text):
    text= text.upper()
    text = text.replace("ONE","1")
    text = text.replace("TWO","2")
    text = text.replace("THREE","3")
    text = text.replace("FOUR","4")
    text = text.replace("FIVE","5")
    text = text.replace("SIX","6")
    text = text.replace("SEVEN","7")
    text = text.replace("EIGHT","8")
    text = text.replace("NINE","9")
    text = text.replace("ZERO","0")
    return text
```

Next thing we do is set up this sliding window:

```
def phone_number_parse(self,values):
    phone_numbers = []
    text = self._letter_to_number(values["text_body"])
    phone = []
    counter = 0
    found = False
    possible_numbers = []
    for ind,letter in enumerate(text):
        if letter.isdigit():
            phone.append(letter)
            found = True
        else:
            if found:
                counter += 1
            if counter > 15 and found:
                phone = []
                counter = 0
                found = False
    #country codes can be two,three digits - not handled yet (due to only working nationally)
        if len(phone) == 10 and phone[0] != '1':
            possible_numbers.append(''.join(phone))
            phone = phone[1:] #sliding window happens here
        if len(phone) == 11 and phone[0] == '1':
            possible_numbers.append(''.join(phone))
            phone = phone[1:] #and here
    for number in possible_numbers:
        if self._verify_phone_number(number):
            phone_numbers.append(number)
    return phone_numbers
```

The final thing we want to do is verify our phone numbers:

```
#number is a string
#twilio creds is a tuple (auth_id,auth_key)
def _verify_phone_number(self,number):
    #I know this worked at some point...test this on other computer
    data = pickle.load(open("twilio.creds","r"))
    r = requests.get("http://lookups.twilio.com/v1/PhoneNumbers/"+number,auth=data)
    if "status_code" in json.loads(r.content).keys():
        return False
    else:
        return True
```

With this code we can get more or less a unique representation of all the people posting in our area overtime.  In the full tool, the valid phone numbers are sent to a database for further inquery and verification.

####Grabbing Addresses

Once we have a sense of uniqueness, we need to know where to step up enforcement, or what areas to target with different policy initiatives, be that more after school programs to keep kids interested in learning or providing more resources to those affected in the form of homeless shelters or other services or whether it be more stings and law enforcement - knowing where to put limited resources is critical.

For this, I wrote a parser that pulls out the addresses or cross streets from a backpage post and sends it to a lat/long representation via the google api or Nominatim api.  Since both of them have rate limits, I try to use both sparingly.

For dealing with addresses we must first categorize our addresses as either complete or cross streets.  If they are complete, then we can use Nominatim, which is more generous than google (and also completely free).  The check for this is surprisingly easy.  We look for a numerical number in our text.  If we find one we then simply use a library called usaddress.  Here's a quick example of it in action:

```
>>> import usaddress
>>> usaddress.parse("Hello there this is my address: 123 Main St. Suite 100 Great Neck, NY, 11024")
[(u'Hello', 'Recipient'), (u'there', 'Recipient'), (u'this', 'Recipient'), (u'is', 'Recipient'), (u'my', 'Recipient'), (u'address:', 'Recipient'), (u'123', 'AddressNumber'), (u'Main', 'StreetName'), (u'St.', 'StreetNamePostType'), (u'Suite', 'OccupancyType'), (u'100', 'OccupancyIdentifier'), (u'Great', 'PlaceName'), (u'Neck,', 'PlaceName'), (u'NY,', 'StateName'), (u'11024', 'ZipCode')]
```
Notice that there are a few 'Recipients' before the address starts.  Then usaddress is able to correctly identify other pieces of the text as actual address components.  So we simply remove any 'Recipients' we find when parsing with this address.

The full code on how to do that is below.

```
def preprocess(self,text):
    #this case is included because usaddress doesn't do a great job if there isn't a number at parsing semantic information
    #However if there is a number it tends to be better than streetaddress
    #Therefore usaddress is better at figuring out where the start of an address is, in say a very long body of text with an address in there at some point
    #It isn't that great at approximate locations
    nouns = ['NN','NNP','NNPS','NNS']
    if any([elem.isdigit() for elem in text.split(" ")]):
        addr = usaddress.parse(text)
        addr = [elem for elem in addr if elem[1] != 'Recipient']
        addr_dict = {}
        for value,key in addr:
            if key in addr_dict.keys():
                addr_dict[key] += " "+value
            else:
                addr_dict[key] = values
        return addr_dict,"complete"
    else:
        possible_streets = []
        for word,tag in tagger.tag(text.split()):
            if tag == 'LOCATION':
                possible_streets.append(word)
        parts = nltk.pos_tag(nltk.word_tokenize(text))
        for part in parts:
            if any([part[1]==noun for noun in nouns]):
                possible_streets.append(part[0])
        return possible_streets,"cross streets"
```

One of the great things about nltk is it has a lot of built-in functionality already.  Probably one of my favorite features is the ability to named entity recognition.  That is, to label nouns semantically.  One of the labels that comes with this named entity recognition engine is location!  Thus we can look for locations in our text, free form (assuming we are just looking for cross streets).  Of course, the strongest thing to do would be to just use a database of all the streets in an area - but those are surprisingly hard to come by.  After this talk, I will probably invest some time in that solution, but for now, this one works well enough.  

Assuming our NER engine isn't perfect, we also look for any nouns as possible cross streets which will be verified later.  (By google).  

Now we are ready to geocode our addresses (or approaximate addresses) into lat/longs.  The reason we do this is for visualization in a map (which we'll do next).

```
def parse(self,text,place="NYC"):
    addr,addr_type = self.preprocess(text)
    google_key = pickle.load(open("google_api_key.pickle","r"))
    g_coder = GoogleV3(google_key)
    if addr_type == 'complete':
        combined_addr = []
        keys = ["AddressNumber","StreetName","StreetNamePostType","PlaceName","StateName","ZipCode"]
        for key in keys:
            try:
                combined_addr += [addr[key]]
            except KeyError:
                continue
            addr = " ".join(combined_addr) 
        n_coder = Nominatim()
        lat_long = n_coder.geocode(addr)
        if lat_long: #means the request succeeded
            return lat_long
        else:
            lat_long = g_coder.geocode(addr)
            return lat_long
        #If None, means no address was recovered.
    if addr_type=='cross streets':
        cross_addr = " and ".join(addr) + place 
        try:
            lat_long = g_coder.geocode(cross_addr)
            return lat_long
        except geopy.geocoders.googlev3.GeocoderQueryError:
            return None
```

#Working with Leaflet

Leaflet is a wonderful library.  It allows you to visualize a whole bunch of information, geographically!  One of the things I've gotten into recently is making use of GIS maps to show my boss and other folks how their data looks.  Making use of leaflet allows us to make this super pretty.

With leaflet we can do things like, create polygons, add visual representations of data, add paths, create heat maps, and add various layers of control and interactivity.  

All and all, leaflet lets us visualy interogate a ton of data and do so in an easy and fun way!  With something very visually pleasing.  

So enough talk, let's look at how to make use of leaflet, with this basic example, [lifted directly from their docs](http://leafletjs.com/examples/quick-start.html):

http://leafletjs.com/examples/quick-start-example.html

Let's start by looking at the head of the html page:

```
<head>
	<title>Leaflet Quick Start Guide Example</title>
	<meta charset="utf-8" />

	<meta name="viewport" content="width=device-width, initial-scale=1.0">

	<link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.css" />
</head>
```

Here we include the necessary CSS via a CDN (content delivery network), note that the official documentation says to use 0.7.4 but when I tried it 0.7.3 is the one that worked.  I'm not sure how long this will be true for, but for now, please use 0.7.3.  

Now let's look at the body of the html, up to the script tag:

```
<body>
<div id="map" style="width: 600px; height: 400px"></div>
 <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js"></script>
 <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet-src.js"></script>
```

Here we see that we add our map in a div tag, with id "map".  Notice also that we set a width and height - this is super important otherwise our map won't appear.  Notice also that we load the leaflet javascript AFTER the map.  This may not matter on your system, but it did matter on mine.  

Now let's look at the map script, which comes after loading leaflet.js:

```
<script>
	var map = L.map('map').setView([51.505, -0.09], 13);

	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6IjZjNmRjNzk3ZmE2MTcwOTEwMGY0MzU3YjUzOWFmNWZhIn0.Y8bhBaUMqFiPrDRW9hieoQ', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
			'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="http://mapbox.com">Mapbox</a>',
		id: 'mapbox.streets'
	}).addTo(map);


	L.marker([51.5, -0.09]).addTo(map)
		.bindPopup("<b>Hello world!</b><br />I am a popup.").openPopup();

	L.circle([51.508, -0.11], 500, {
		color: 'red',
		fillColor: '#f03',
		fillOpacity: 0.5
	}).addTo(map).bindPopup("I am a circle.");

	L.polygon([
		[51.509, -0.08],
		[51.503, -0.06],
		[51.51, -0.047]
	]).addTo(map).bindPopup("I am a polygon.");


	var popup = L.popup();

	function onMapClick(e) {
		popup
			.setLatLng(e.latlng)
			.setContent("You clicked the map at " + e.latlng.toString())
			.openOn(map);
	}

	map.on('click', onMapClick);

	</script>
```

There is a lot to unpack here, so we'll go through it line by line:


`var map = L.map('map').setView([51.505, -0.09], 13);`

On this line we instantiate our map object and link it to the map id in our div tag.  To understand this constructor in more detail, check out [the reference](http://leafletjs.com/reference.html#map-constructor).  

Notice that we chain this object with a setView method - which sets the geographic coordinates that our map will start at and the zoom level.  [Here is the referenece for setView](http://leafletjs.com/reference.html#map-options)

Next we pull in a tiling.  This is how the map will look.  Leaflet's documentation recommends Mapbox's tiling system.  So we'll make use of it.  Head over to [mapbox](https://www.mapbox.com/) to get api access.


Here's how you add tiling:

```
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6IjZjNmRjNzk3ZmE2MTcwOTEwMGY0MzU3YjUzOWFmNWZhIn0.Y8bhBaUMqFiPrDRW9hieoQ', {
	maxZoom: 18,
	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
		'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
		'Imagery © <a href="http://mapbox.com">Mapbox</a>',
	id: 'mapbox.streets'
}).addTo(map);
```

Basically we are mapping a request to the mapbox api with a maximum zoom, attribution, and id preset.  Notice that we also pass in an access token in this case, the string: pk.eyJ1IjoibWFwYm94IiwiYSI6IjZjNmRjNzk3ZmE2MTcwOTEwMGY0MzU3YjUzOWFmNWZhIn0.Y8bhBaUMqFiPrDRW9hieoQ which clearly is randomly generated.  

Notice that we are creating a tileLayer object and then adding it to our map layer.  Essentially, we can think of these data structures as components of a map object is sort of like the base visual representation but it is ultimately an abstraction.  The tile layer is what gives it a visual form.  In this case we pull in the look of the tiling from the tile layer.  And then we can super impose other structures ontop of the tile layer.  

We see this pattern in the remaining objects we add to our map:

```
L.marker([51.5, -0.09]).addTo(map)
	.bindPopup("<b>Hello world!</b><br />I am a popup.").openPopup();

L.circle([51.508, -0.11], 500, {
	color: 'red',
	fillColor: '#f03',
	fillOpacity: 0.5
}).addTo(map).bindPopup("I am a circle.");

L.polygon([
	[51.509, -0.08],
	[51.503, -0.06],
	[51.51, -0.047]
]).addTo(map).bindPopup("I am a polygon.");
```

The marker, circle and polygon are all examples of objects that take up a discrete piece of the map:

* A marker takes up a single point in this case - (51.5, -0.09).  

* The circle has both a center and radius, in this case - [(51.508,-0.11), 500].

* The polygon has just a set of coordinates, connected by points: [51.509,-0.08], [51.503,-0.06], [51.51, -0.047]

Notice that we simply chain the various shapes to our map data structure, and then add bindPopups to each, identifying what the object's data is.  Notice of course that we could have had anything in the data since we can embed html.  

Now that we understand the objects that must be loaded from the server, let's understand the elements of the code that are dynamic from the front end:

```
var popup = L.popup();

function onMapClick(e) {
	popup
		.setLatLng(e.latlng)
		.setContent("You clicked the map at " + e.latlng.toString())
		.openOn(map);
}

map.on('click', onMapClick);
```

Here we create a popup object.  Notice that we make use of this popup object by wrapping it in a function that calls three of it's methods:

`setLatLng` - This method captures the latitude/longitude that was clicked and saves it to the popup object, binding the marker to the location you clicked.
`setContent` -  This method displays the latitude/longitude
`openOn` - opens the popup object and displays the associated content

Finnally we have - `map.on('click',onMapClick)`:

This method turns on the click action for the map, and sets it to the function we created.  Notice that we have one global popup object that gets changed as we click on different places in the map.

So now we understand a lot of what Leaflet.js can do, which is great.  Of course, all of this was static, as far as the data goes.  By making use of server, which can request different data points you can:

* filter by different data points, 
* bring in different data sets, 
* extrapolate data points,
* regroup the data elements dynamically, according to some clustering algorithm

Clearly this adds a whole layer of flexibility and dynamics that would otherwise be lost.  So how do we do that?

Let's start with the most basic server and templated html possible:

server.py:

```
import json
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    states = [{
        "type":"Feature",
        "properties": {"party": "Republican"},
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-104.05, 48.99],
                [-97.22,  48.98],
                [-96.58,  45.94],
                [-104.03, 45.94],
                [-104.05, 48.99]
            ]]
        }
    }, {
        "type": "Feature",
        "properties": {"party": "Democrat"},
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-109.05, 41.00],
                [-102.06, 40.99],
                [-102.03, 36.99],
                [-109.04, 36.99],
            [-109.05, 41.00]
            ]]
        }
    }]

    return render_template("index.html",states=json.dumps(states))
```

Here we have a simple flask app, the only difference is the static geojson - stored as a python dictionary.  Notice the necessary pieces - type, properties, geometry.  These are all the necessary keys. The geometry key is where the lat/long actually lives.  

We can also do realtime things just easily:

For that we'll need to pipe in our data from an api:

```
from flask import Flask, render_template, redirect, url_for
import random
import json
app = Flask(__name__)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

@app.route("/send_areas",methods=["GET","POST"])
def send_areas():
    areas = [{
        "type":"Feature",
        "properties": {"glob": "1st"},
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [[random.randint(100,106) + random.random(), random.randint(44,49) + random.random()] for i in xrange(4)]
            ]
        }
    }, {
        "type": "Feature",
        "properties": {"glob": "2nd"},
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [[random.randint(100,106) + random.random(), random.randint(44,49) + random.random()] for i in xrange(4)]
            ]
        }
    }]
    return json.dumps(areas)

app.run(debug=True,port=5001,threaded=True)
```

here is the javascript realtime-leaflet.js library to get us to do that:

```
var map = L.map('map'),
    realtime = L.realtime({
        url: 'http://localhost:5001/send_areas',/* 'https://wanderdrone.appspot.com/', - works for sure */
        crossOrigin: true,
        type: 'json'
    }, {
        interval: 3 * 1000
    }).addTo(map);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6IjZjNmRjNzk3ZmE2MTcwOTEwMGY0MzU3YjUzOWFmNWZhIn0.Y8bhBaUMqFiPrDRW9hieoQ', {
	maxZoom: 18,
	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
		'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
		'Imagery © <a href="http://mapbox.com">Mapbox</a>',
	id: 'mapbox.streets'
	}).addTo(map);

realtime.on('update', function() {
    map.fitBounds(realtime.getBounds(), {maxZoom: 3});
});

```

As you can see the only major difference is the use of real time.  In our html we simply include the realtime-leaflet.js library which can be found [here](https://github.com/perliedman/leaflet-realtime).

Here's the html:

```
<html>
<head>
    <title>Leaflet Realtime</title>
    <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css" />
    
</head>
<body>
    <div id="map" style="width: 600px; height: 400px"></div>

    <!-- source: https://github.com/perliedman/leaflet-realtime -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js"></script>
    <script src="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet-src.js"></script>
    <script src="{{ url_for('static', filename='js/leaflet-realtime.js') }}"></script>
    <script src=" {{ url_for('static', filename='js/index.js') }}"></script>
</body>
</html>
```

##Time series analysis

For this we'll make use of c3.js a wonderful library for doing time series data visualization.  And we'll also make use of ARIMA models to do some prediction.  Unfortunately I couldn't find any patterns before this talk, that led to actual prediction so I'll need to keep things fairly high level here.

