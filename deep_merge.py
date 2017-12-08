#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from ansible.errors import AnsibleError, AnsibleFilterError
# from functools import reduce  # uncomment this if this script runs on python 3

def merge_hash(a, b):
    """
    Recursively merges hash b into a so that keys from b take precedence over keys from a
    refs: https://github.com/ansible/ansible/blob/stable-2.2/lib/ansible/plugins/filter/core.py#L282
    refs: https://github.com/ansible/ansible/blob/stable-2.2/lib/ansible/utils/vars.py#L73
    """

    # if a is empty or equal to b, return b
    if a == {} or a == b:
        return b.copy()

    # if b is empty the below unfolds quickly
    result = a.copy()

    # next, iterate over b keys and values
    for k, v in b.iteritems():
        # if there's already such key in a
        # and that key contains a dictionary
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            # merge those dicts recursively
            result[k] = merge_hash(result[k], v)
        elif k in result and isinstance(result[k], list) and isinstance(v, list):
            # merge lists
            result[k] = result[k] + v
        elif v is None:
            # not update
            continue
        else:
            # otherwise, just copy the value from b to a
            result[k] = v

    return result

def deep_merge(*terms):

    terms = [x for x in terms if x is not None and not isinstance(x,unicode)]
    for t in terms:
        if not isinstance(t, dict):
            raise AnsibleFilterError("|deep_merge expects dictionaries, got " + repr(t))

    return reduce(merge_hash, terms)

class FilterModule(object):
    def filters(self):
        return {'deep_merge': deep_merge}
