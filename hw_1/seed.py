import json

from models import Author, Quote


if __name__=="__main__":
    with open("authors.json", "r", encoding="utf-8") as fh:
        data = json.load(fh)
        for el in data:
            try:
                author = Author(fullname=el.get("fullname"), born_date=el.get("born_date"),
                                born_location=el.get("born_location"), description=el.get("description"))
                author.save()
            except Exception as e:
                print(e)
                
    with open("quotes.json", "r", encoding="utf-8") as fh:
        data = json.load(fh)
        for el in data:
            author, *_ = Author.objects(fullname=el.get("author"))
            quote = Quote(tags=el.get("tags"), author=author,
                            quote=el.get("quote"))
            quote.save()