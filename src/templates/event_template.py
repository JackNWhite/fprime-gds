'''
@brief Event Template class

Instances of this class describe a specific event type. For example: AF_ASSERT_0
or cmdSeq_CS_CmdStarted

@date Created July 2, 2018
@author R. Joseph Paetz

@bug No known bugs
'''

from enum import Enum

import data_template


#TODO Move to enums file
EventSeverity = Enum('Severity', 'COMMAND ACTIVITY_LO ACTIVITY_HI WARNING_LO WARNING_HI DIAGNOSTIC FATAL')

class EventTemplate(data_template.DataTemplate):
    '''Class to create event templates to describe specific event types'''

    def __init__(self, event_id, name, severity, format_str, description, args):
        '''
        Constructor

        Args:
            event_id: The ID of the event being described
            name: event name as a string
            severity: event severity as an EventSeverity Enum
            format_str: Format string for the event's arguments
            description: Event Description
            args: List of arguments in tuple form. Each tuple should be:
                  (arg name, arg description, arg type). Where arg type is a
                  class derived from the class BaseType
        '''

        # Make sure correct types are passed
        # TODO Is this necessary? It isn't anywhere else?
        if not type(event_id) == type(int()):
            raise TypeMismatchException(type(int()),type(event_id))

        if not type(name) == type(str()):
            raise TypeMismatchException(type(str()), type(name))

        if not type(format_str) == type(str()):
            raise TypeMismatchException(type(str()), type(format_str))

        if not type(description) == type(str()):
            raise TypeMismatchException(type(str()), type(description))

        if not type(args) == type(list()):
            raise TypeMismatchException(type(list()),type(args))

        for (arg_name, arg_desc, arg_type) in args:
            if not type(arg_name) == type(str()):
                raise TypeMismatchException(type(str()),type(arg_name))

            if not type(arg_desc) == type(str()):
                raise TypeMismatchException(type(str()),type(arg_desc))

            if not issubclass(type(arg_type), type(BaseType())):
                raise TypeMismatchException(type(BaseType()),type(arg_type))

        # Initialize event internal variables
        self.id       = event_id
        self.name     = name
        self.severity = severity
        self.format_str = format_str
        self.description = description
        self.args = args


    def get_severity(self):
        return self.severity

    def get_format_string(self):
        return self.format_string

    def get_description(self):
        self.event_description

    def get_args(self):
        return self.arguments


if __name__ == '__main__':
    pass