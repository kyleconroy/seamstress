![Seamstress - Simple Configuration Management](https://github.com/kyleconroy/seamstress/raw/master/logo.jpg)

Chef and Puppet are great, but what if you just want to easily manage a couple of servers?

## Example

Seamstress is built on top of [Fabric](fabfile.org), and uses the `fabfile.py` to store configurations.

```python
from seamstress.core import * 

def configure():
    user("ubuntu")
    directory("/var/web/hello_world")
```

Configure a system using the `fab` command.

    $ fab -H 33.33.33.10 configure

### Resources

seamstress supports the following resources

* user
* directory 
* document 
* remote_file

## Installation

    $ pip install seamstress

or, if you must

    $ easy_install seamstress

## Development

I test on a t1.micro instance on EC2 running Ubuntu 10.04 64-bit.

    $ pip install -r requirements.txt
    $ fab --config tests/fabricrc functional


