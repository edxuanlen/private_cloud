import re
import application


class resolution:

    def resolute(self, pstr, args={}):

        # execute
        match = re.match('.*<% (.*) %>.*', pstr)
        if match:
            execute = match.groups()[0].strip()
            print (execute)
            exec(execute)
            pstr = ''

        # values
        match = re.match('.*<%= (.*) %>.*', pstr)
        if match:
            value = match.groups()[0].strip()
            pstr = re.sub('<%= (.*) %>', str(args[value]), pstr, 1)

        return pstr
