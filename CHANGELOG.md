# 0.5

+ Add page redirects (`[redirect:/Another]`)
+ Actually implement named page link (`[[Page Title|/Another/Page]]`)
+ Implement cache support and pymemcache backend
+ Improve/normalise paths (always starting uppercase)

# v0.4

+ Add `--host` and `--port` CLI arguments

# v0.3

First working version; fix missing templates in package.

+ Add proper error pages
+ Encode hashed passwords if `str` objects

# v0.1 / v0.2

Initial version! Features:

+ Markdown content
+ Inter-page linking (`[[/Another/Page]]`)
+ Index generation based on a path prefix (`[index:/Another]`)
+ Page histories / restore
+ Pluggable authentication backend
+ Custom template support
