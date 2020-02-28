import csv
import json
import logging
import sys
import time
from datetime import datetime
from collections import deque

import geohash
import mgrs
from tqdm import tqdm
from elasticsearch import Elasticsearch, helpers

import constants

log = logging.getLogger(__name__)

csv.field_size_limit(sys.maxsize)
m = mgrs.MGRS()
todays_date = datetime.today().strftime("%Y-%m-%d")


def parse_row(counter, row):
    coords = row[4] + "," + row[5]
    doc = {
        "geonameid" : row[0],
        "name" : row[1],
        "asciiname" : row[2],
        "alternativenames" : row[3],
        "coordinates" : coords,  # 4, 5
        "lat": float(row[4]),
        "lng": float(row[5]),
        "feature_class" : row[6],
        "feature_code" : row[7],
        "country_code" : row[8],
        "cc2" : row[9],
        "admin1" : row[10],
        "admin2" : row[11],
        "admin3" : row[12],
        "admin4" : row[13],
        "population" : row[14],
        "elevation" : row[15],
        "dem" : row[16],
        "geohash" : "",
        "precision" : 5,
        "mgrs" : m.toMGRS(float(row[4]), float(row[5])).decode("utf-8"),
        "timezone" :  row[17],
        "modification_date" : todays_date
    }

    try:
        doc["geohash"] = geohash.encode(float(row[4]), float(row[5]), precision=5)
    except Exception as e:
        log.error(f"Exception caught - {e}")
        pass

    action = {
        "_index" : "geonames",
        # "_type" : "place",
        # "_id" : doc['geonameid'],
        "_source" : doc
    }
    return action

def main():
    es = Elasticsearch(urls=constants.ELASTICSEARCH_HOST,
                       scheme=constants.ELASTICSEARCH_SCHEME,
                       max_size=constants.ELASTICSEARCH_MAX_SIZE,
                       port=constants.ELASTICSEARCH_PORT)
    es.indices.delete(index=constants.ELASTICSEARCH_INDEX_NAME, ignore=[400, 404])
    with open(constants.ELASTICSEARCH_MAPPING, "rt", encoding="utf-8") as mapping:
        json_mapping = json.load(mapping)
        es.indices.create(index=constants.ELASTICSEARCH_INDEX_NAME, body=json_mapping, ignore=400)

    size = 0

    log.info("Generating index")
    t = time.time()
    with open(constants.GEONAMES_ALL_COUNTRIES, "rt") as handler:
        reader = csv.reader(handler, delimiter='\t')
        vals = []
        for c, row in enumerate(tqdm(reader, total=constants.GEONAMES_TOTAL)):
            vals.append(parse_row(c, row))
            size = sys.getsizeof(vals)
            if size >= constants.CHUNK_SIZE:
                deque(helpers.parallel_bulk(es, vals,
                                            max_chunk_bytes=constants.MAX_CHUNK_SIZE, 
                                            thread_count=constants.THREAD_COUNT, 
                                            queue_size=constants.QUEUE_SIZE), maxlen=0)
                size = 0
                del vals[:]

        deque(helpers.parallel_bulk(es, vals,
                                    max_chunk_bytes=constants.MAX_CHUNK_SIZE, 
                                    thread_count=constants.THREAD_COUNT, 
                                    queue_size=constants.QUEUE_SIZE), maxlen=0)
        handler.close()

    elapsed_time = (time.time() - t) / 60
    log.info("Elapsed minutes: ", elapsed_time)
    es.indices.put_settings(index=constants.ELASTICSEARCH_INDEX_NAME, body={"index": {"refresh_interval": "1s"}}, ignore=400)
    es.indices.refresh(index=constants.ELASTICSEARCH_INDEX_NAME)


if __name__ == "__main__":
	main()
