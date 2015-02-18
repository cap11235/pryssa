# pryssa
When debugging a set of code which depends on expensive calculations, it is a pain to run repeatedly to test. This module allows easy caching of a given block of code in a function by adding two lines:

```
from pryssa import pryssa

inputs = ...
pryssa(inputs)
x, y = expensive_computation(inputs)
# PRYSSA x y
plot(x, y)
```

When `pryssa` is called with the inputs to the expensive computation (to differentiate caches), it checks if a cache exists. If so, it sets the local variables given in the PRYSSA line and jumps just after the comment. Otherwise, it runs the expensive computation, and saves the results.
