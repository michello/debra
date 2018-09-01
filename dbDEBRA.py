# Copyright 2015 Google Inc. All rights reserved.
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


from google.appengine.ext import ndb

import webapp2

class Give(ndb.Model):
    number = ndb.StringProperty()
    item = ndb.StringProperty()
    user_id = ndb.IntegerProperty()
    location = ndb.StringProperty()
    supply = ndb.BooleanProperty()

class Need(ndb.Model):
    number = ndb.StringProperty()
    item = ndb.StringProperty()
    user_id = ndb.IntegerProperty()
    location = ndb.StringProperty()
    completion = ndb.BooleanProperty()

def add_Giver(num, item, u_id, loc, sup):
    giver = Give(
        number=num, item=item, user_id=u_id, location=loc, supply=sup)
    giver.put()

def main():
    add_Giver('12341452', 'food', 1, '12345', True)

main()

