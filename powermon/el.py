#!/usr/bin/env python
import requests
from elasticsearch import Elasticsearch
import json
# Eerste maand.
# Sit netnou in functions
es  = Elasticsearch()
res = es.search(index="nginx_json_elk_example", body={ 
      "query": {
    "filtered": {
      "query": {
        "query_string": {
          "query": "*",
          "analyze_wildcard": "true"
        }
      },
      "filter": {
        "bool": {
          "must": [
            {
              "range": {
                "@timestamp": {
                  "gte": "now-12M",
                  "lte": "now",
                  "format": "epoch_millis"
                }
              }
            }
          ],
          "must_not": []
        }
      }
    }
  },
  "size": 0,
  "aggs": {
    "blah": {
      "terms": {
        "field": "remote_ip.raw",
        "size": 1000,
        "order": {
          "_count": "desc"
       }
      }
    }
  } })
#re
print(res)
