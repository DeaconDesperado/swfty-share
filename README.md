# Swfty - Simple Geo story sharing

This app is currently a work in progress.

The browser frontend uses the HTML5 geolocation API to detect the client's location, and then finds "stories" (collections of text, audio and images) that are within a given radius of that point.  The user also has the opportunity to create their own stories (there isn't any authentication at present, but that could be easily added.)

Also included is a Twisted transfer protocol `protocols/transfer/transfer.py` This protocol is intended to receive asynchronous file uploads for stories via mobile devices.

Modules are as follows:

* `frontend` contains the Flask frontend that will render html to regular browsers and handle HTTP form posts for stories
* `protocols` define custom client and transfer protocols to be implemented by mobile devices to add files to stories
* `models` contains the core program models for stories and files built for MongoDB
* `search` will eventually contain a parallelized search to crawl through story descriptions, tags and files. 

The app is intended as a proof of concept

Obviously the application directory needs to be on the PYTHONPATH to run.
