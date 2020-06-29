# News Aggregator

### How to Run

To run, use the following commands on command line:

```
pip install -r /requirements.txt
cd mysite
python manage.py runserver
```

The generic GET request has been given on http://localhost:8000/news/. For the search feature, go to http://localhost:8000/news/search and type the phrase you want to search for. A new page will load with the JSON results. To search again, you will have to go back.

There's another version with the information in the JSON objects on the HTML page but there are some formatting issues here. For this version, go to http://localhost:8000/news/together. The top 20 news from /r/news and News API have been given here along with a field to search for results. After searching, to get back to the top 20 news or to search for other news, click the Go Back button.