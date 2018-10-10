/**
 * Copyright Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
// [START classroom_quickstart]
/**
 * Lists all course names and ids. 
 */
function listCourses() {
  var courses = [];
  var page_token = null;
  var optionalArgs = {
    pageToken: page_token,
    pageSize: 100
  };
  while (true) {
    var response = Classroom.Courses.list(optionalArgs);
    var courses = response['courses'];
    if (! page_token) {
       break;
    }
  }
  if (courses.length == 0) {
    Logger.log("No courses found.");
  }
  else {
    Logger.log("Courses:");
    for (course in courses) {
      Logger.log('%s (%s)', courses[course].name, courses[course].id);
    }
  }
}