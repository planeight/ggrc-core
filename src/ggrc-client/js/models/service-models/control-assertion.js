/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Cacheable from '../cacheable';

export default Cacheable('CMS.Models.ControlAssertion', {
  root_object: 'control_assertion',
  root_collection: 'control_assertions',
  findAll: 'GET /api/control_assertions',
  findOne: 'GET /api/control_assertions/{id}',
}, {});
