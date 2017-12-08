deep_merge filter
====

ansible filter which merges nested dictionaries/lists into the other one.

# usage

vars in below:
```
var_1:
  a:
    b: "varb"
    c: "varc"
    d:
      - vard1
      - vard2

var_2:
  a:
    c: "cvar"
    d:
      - vard3
```

and then, uses `deep_merge` filter:
```
- set_fact:
  var_result: "{{ var_1 | deep_merge(var_2) }}"
```

result:
```
var_result:
  a:
    b: "varb"
    c: "cvar"
    d:
      - vard1
      - vard2
      - vard3
```

