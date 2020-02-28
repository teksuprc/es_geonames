# Local Elasticsearch Geonames Database.

Taken from the [Mordecai project](https://github.com/openeventdata/mordecai). Which is based on the [ES-Geonames project](https://github.com/openeventdata/es-geonames).


- Table of Contents
  - [Automated Install](###automated-install)
  - [Manual Install](#manual-install)
  - [Install Kibana](#install-kibana)
  - [Issues](#issues)
  - [Testing](#testing)
  - [References](#references)
----

### Automated Install

***NOTE*** 
* The installation process can take up to 2 hours.
* Please stop any running docker containers.
* Please close any large applications.

To run the automated install run the following commands:

```bash
$ cd elasticsearch
$ make geonames
```

As apart of the automated install the following commands will run:
* docker-compose up -d
* curl http://download.geonames.org/export/dump/allCountries.zip --output allCountries.zip
* unzip allCountries.zip -d data/geonames
* python geonames_elasticsearch_loader.py


### Manual Install

This is a long running process and could take over an hour to complete.

```
$ cd elasticsearch
$ docker-compose up -d
$ curl http://download.geonames.org/export/dump/allCountries.zip --output allCountries.zip
$ unzip allCountries.zip -d data/geonames
$ python geonames_elasticsearch_loader.py
```


### Install Kibana

```
$ curl https://artifacts.elastic.co/downloads/kibana/kibana-oss-7.6.0-darwin-x86_64.tar.gz --output kibana-oss-7.6.0-darwin-x86_64.tar.gz
$ tar xzvf kibana-oss-7.6.0-darwin-x86_64.tar.gz
$ cd kibana-oss-7.6.0-darwin-x86_64/
$ ./bin/kibana
```


### Issues

If there are issues ingesting try the following, if the errors match:

* No _type defined: Uncomment out the ***_type*** in the ***action*** dictionary.


### Testing:

##### Web API

Count documents in the index: Approx 11,986,317 records

```
curl -X GET "localhost:9200/geonames/_count"
```


Keyword query:

```
curl -X GET "localhost:9200/geonames/_search?q=Tolyatti&pretty"
```


curl -X GET "localhost:9200/twitter/_search?q=user:kimchy&pretty"


Query with filter:

```
curl -X POST "http://localhost:9200/geonames/_search" -H 'Content-Type: application/json' -d '
{
  "query": { 
    "bool": { 
      "must": [
        {"match": {"alternativenames":"Tolyatti"}}
      ],
      "filter": [ 
        { "term":  { "feature_class": "P" }}
      ]
    }
  }
}'
```


### Refereneces:

Docker Compose Reference:
* [Compose file version 3 reference](https://docs.docker.com/compose/compose-file/)

Named Docker Volumes:
* [Define Named Volumes with Host Mount in Docker Compose File](http://blog.code4hire.com/2018/06/define-named-volume-with-host-mount-in-the-docker-compose-file)

Tune ElasticSearch Indexing Speed:
* [qbox.io.blog](https://qbox.io/blog/maximize-guide-elasticsearch-indexing-performance-part-1?utm_source=qbox.io&utm_medium=article&utm_campaign=maximize-guide-elasticsearch-indexing-performance-part-1)

* [Elastic.co - Tune for indexing speed](https://www.elastic.co/guide/en/elasticsearch/reference/master/tune-for-indexing-speed.html)
