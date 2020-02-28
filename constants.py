
# for af.txt        use 130
# for allCountries  use 11986316
GEONAMES_ALL_COUNTRIES = "./data/geonames/allCountries.txt" # af.txt  allCountries.txt
GEONAMES_TOTAL = 11986316   # 130  11986316

NGA_GEONAMES_ALL_COUNTRIES = "./data/nga/geonames_20200217/Countries.txt"

ELASTICSEARCH_HOST = "localhost"
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_SCHEME = "http"
ELASTICSEARCH_TIMEOUT = 60
ELASTICSEARCH_MAX_RETRIES = 2
ELASTICSEARCH_INDEX_NAME = "geonames"
ELASTICSEARCH_MAPPING = "./geonames_mapping.json"
ELASTICSEARCH_MAX_SIZE = 50

CHUNK_SIZE = 20 * 1024 * 1024 # 2MB
MAX_CHUNK_SIZE = 35 * 1024 * 1024 # 3.5MB
THREAD_COUNT = 6
QUEUE_SIZE = 12