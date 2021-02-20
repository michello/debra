# debra ⚠️
<p align="center">a disaster emergency bot for relief assistance<br>
  quickly connecting disaster victims to the aid they need and volunteers to those they can help</p>
<p align="center"><img src="https://i.gyazo.com/915d4c5ff8b1506686720f0865ee2bdc.png" height="200px;"/></p>


## inspiration
In our research, we have found that during times of natural disasters the top 3 communication methods are social media, mobile apps, and cellphones. However, the best way to keep the public safe is by informing them through a quick text alert, as studies have shown that texts are 10x quicker than other means of communication such as calling them via phone number. You can also reach out to more individuals simultaneously through SMS.

Thus, we came up with Debra as a way to connect disaster victims to the aid they need and volunteers to those they can help.

## what it does
<img src="https://i.gyazo.com/e751b527fdd517061084e892b1b067dc.png" width="200px;" height="350px;"><img src="https://github.com/michello/debra/blob/master/static/debratext2.png" width="200px;" height="350px;"><img src="https://github.com/michello/debra/blob/master/static/debratext3.png" width="200px;" height="350px;"><img src="https://github.com/michello/debra/blob/master/static/debratext4.png" width="200px;" height="350px;">

By texting 'Hi DEBRA' to our application number, Debra will allow you to share the address of where you are currently located and specify whether you are providing or in need of specified supplies. Once provided, this data is stored into our application's database and will be mapped out on our web view to easily detect where people are either in need or providing specific supplies.

<img src="https://github.com/michello/debra/blob/master/static/mapImage.png">

If someone has a supply of items that are requested or supply of items that are available, they receive a message with information on where it can be received or donated.

## what it's built with
We built the application with Twilio for SMS communication and Python/Flask for the backend server. In order to save the data being sent around, we stored the data in Google's Cloud Firestore.

## awards
<a href="https://devpost.com/software/debra">Best use of Google Cloud Platform</a>
