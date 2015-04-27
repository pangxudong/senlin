
HIGH PRIORITY
=============

ENGINE
------
  - cleanse scheduler module [Yanyan Hu]
  - add support to get node details from the profile layer, e.g. Nova server
    attributes or Heat stack outputs etc.

DRIVER
------
  - Handle Heat stack operation exception handling [Qiming]

POLICY
------
  - healthy policy[Liuh]
  - Formalize policy enforcement levels [Qiming]

TEST CASES
----------
  - Add test case the profile context can be saved and loaded correctly.

MIDDLE PRIORITY
===============

API
---
  - Revise the API for sorting, based on the following guideline:
    https://github.com/openstack/api-wg/blob/master/guidelines/pagination_filter_sort.rst
  - Add support to replace a cluster node with another node

DB
--
  - Add test cases for policy_delete with 'force' set to True[Liuh/ZhaiHF]

ENGINE
------
  - Cleanse common/exception module

  - Revise spec parser so that 'type' and 'version' are parts of the spec file
    This could be a client-only fix, or a client/server fix.

  - Design and implement dynamical plugin loading mechanism that allows 
    loading plugins from any paths

  - Provide support to oslo.notification and allow nodes to receive and react
    to those notifications accordingly.
    [https://ask.openstack.org/en/question/46495/heat-autoscaling-adaptation-actions-on-existing-servers/]

  - Allow actions to be paused and resumed.
    This is important for some background actions such as health checking

  - Add support to template_url for heat stack profile
    Note: if template and template_url are both specified, use template
    Need to refer to heat api test for testing heat profile

OSLO
----
  - Add support to oslo_versionedobjects
  - Check if pre-context middleware needs logging and add special supports.

POLICY
------
  - Scaling policy allowng a cluster to scale to existing nodes 

LOW PRIORITY
============

DRIVER
------
  - add Heat resource driver

TEST
----
  - Add test case to engine/parser
  - Add test case to engine/registry
  - Add test case to engine/environment

DOC
-----
  - Provide a sample conf file for customizing senlin options