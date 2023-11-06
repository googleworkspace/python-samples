# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=E1102
# python3
"""Retrieves customer data from our companies "internal" customer data serivce.

This data service is meant to be illustrative for demo purposes, as its just
hard coded data. This can be any internal or on-premise data store.
"""


class CustomerDataService(object):
  _CUSTOMER_DATA = {
      "mars": {
          "customer_name": "Mars Inc.",
          "customer_logo": (
              "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/"
              + "OSIRIS_Mars_true_color.jpg/550px-OSIRIS_Mars_true_color.jpg"
          ),
          "curr_q": "Q2",
          "curr_q_total_sales": "$2,532,124",
          "curr_q_qoq": "0.054",
          "prev_q": "Q1",
          "prev_q_total_sales": "$2,413,584",
          "next_q": "Q3",
          "next_q_total_sales_proj": "$2,634,765",
          "next_q_qoq_proj": "0.041",
          "top1_sku": "Phobos",
          "top1_sales": "$334,384",
          "top2_sku": "Deimos",
          "top2_sales": "$315,718",
          "top3_sku": "Charon",
          "top3_sales": "$285,727",
          "top4_sku": "Nix",
          "top4_sales": "$264,023",
          "top5_sku": "Hydra",
          "top5_sales": "$212,361",
      },
      "jupiter": {
          "customer_name": "Jupiter LLC",
          "customer_logo": (
              "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/"
              + "Jupiter_and_its_shrunken_Great_Red_Spot.jpg/660px-Jupiter_"
              + "and_its_shrunken_Great_Red_Spot.jpg"
          ),
          "curr_q": "Q2",
          "curr_q_total_sales": "$1,532,124",
          "curr_q_qoq": "0.031",
          "prev_q": "Q1",
          "prev_q_total_sales": "$1,413,584",
          "next_q": "Q3",
          "next_q_total_sales_proj": "$1,634,765",
          "next_q_qoq_proj": "0.021",
          "top1_sku": "Io",
          "top1_sales": "$234,384",
          "top2_sku": "Europa",
          "top2_sales": "$215,718",
          "top3_sku": "Ganymede",
          "top3_sales": "$185,727",
          "top4_sku": "Callisto",
          "top4_sales": "$164,023",
          "top5_sku": "Amalthea",
          "top5_sales": "$112,361",
      },
      "saturn": {
          "customer_name": "Saturn",
          "customer_logo": (
              "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/"
              + "Saturn_during_Equinox.jpg/800px-Saturn_during_Equinox.jpg"
          ),
          "curr_q": "Q2",
          "curr_q_total_sales": "$2,532,124",
          "curr_q_qoq": "0.032",
          "prev_q": "Q1",
          "prev_q_total_sales": "$2,413,584",
          "next_q": "Q3",
          "next_q_total_sales_proj": "$2,634,765",
          "next_q_qoq_proj": "0.029",
          "top1_sku": "Mimas",
          "top1_sales": "$334,384",
          "top2_sku": "Enceladus",
          "top2_sales": "$315,718",
          "top3_sku": "Tethys",
          "top3_sales": "$285,727",
          "top4_sku": "Dione",
          "top4_sales": "$264,023",
          "top5_sku": "Rhea",
          "top5_sales": "$212,361",
      },
      "neptune": {
          "customer_name": "Neptune",
          "customer_logo": (
              "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/"
              + "Neptune_Full.jpg/600px-Neptune_Full.jpg"
          ),
          "curr_q": "Q2",
          "curr_q_total_sales": "$2,532,124",
          "curr_q_qoq": "0.027",
          "prev_q": "Q1",
          "prev_q_total_sales": "$2,413,584",
          "next_q": "Q3",
          "next_q_total_sales_proj": "$2,634,765",
          "next_q_qoq_proj": "0.039",
          "top1_sku": "Triton",
          "top1_sales": "$334,384",
          "top2_sku": "Nereid",
          "top2_sales": "$315,718",
          "top3_sku": "Naiad",
          "top3_sales": "$285,727",
          "top4_sku": "Thalassa",
          "top4_sales": "$264,023",
          "top5_sku": "Despina",
          "top5_sales": "$212,361",
      },
  }

  def GetCustomerData(self, customer_id, properties):
    customer_data = self._CUSTOMER_DATA[customer_id]
    return [customer_data[p.lower()] for p in properties]
