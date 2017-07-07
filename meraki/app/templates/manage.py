# manage.py

from flask_script import Command, Manager, Option


class Hello(Command):

    option_list = (
        Option('--name', '-n', dest='name'),
    )

    def run(self, name):
        print("hello %s" % name)

