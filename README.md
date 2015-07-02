# qtrollolo

create customized json results from trello boards. We use [Trolly](https://github.com/plish/Trolly), a python wrapper to access the Trello API and fetch data.

## setup

* ```sudo pip install -r requirements.txt```
* create your configfile and run ```qtrollolo --config <config file> --output <path_to_outputfile>```

## config file

structure:

```
{
  "apikey" : "YOURKEY",
  "token" : "YOURTOKEN",
  "lists" : [
    "listId1",
    "listId2" : {
      "cardFields" : [
        "fieldA",
        "fieldB",
        "fieldC"
      ]
    },
    "listId3"
  ]
  "cardFields" : [
    "field1",
    "field2",
    "field3"
  ]
}
```

list IDs you can get via https://api.trello.com/1/board/<board id>?key=<your api dev key>&cards=none&lists=open&list_fields=name&token=<user token>. You can get cardfields per list or a default set. The board ID is available from public URL. More information, including field names on this API you can find on https://trello.com/docs/
