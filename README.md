# Seamstress - Simple Configuration Management

Chef and Puppet are great, but what if you just want to easily manage a couple of servers?

Enter Seamstress

## Example

Seamstress is built on top of [Fabric](fabfile.org), and uses the `fabfile.py` to store configurations.

```python
from seamstress import user, directory

def configure():
    user("ubuntu")
    directory("/var/web/hello_world")
```

Configure a system using the `fab` command.

    $ fab -H 33.33.33.10 configure

### Resources

Currently, seamstress has support for the following resources

- Users
- Directories
- Documents

## Installation

    $ pip install seamstress

or, if you must

    $ easy_install seamstress

## Development

I use [Vagrant](www.vagrantup.com) to test `seamstress`. If you want to run the tests, you'll need to boot up a VM available at the address 33.33.33.10.

    $ pip install -r requirements.txt
    $ ./test


