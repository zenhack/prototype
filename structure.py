
from types import GeneratorType

OBJ_MODE = 0
LIST_MODE = 1


class Structure(object):
    """Generates a UI structure from a definitions file"""
    def __init__(self, ui_file):
        self.ui = ui_file
        # Load structure here.

    def generate_list(self, context):
        for x in context:
            for i in self.generate(x):
                yield i

    def generate(self, context, mode=None):
    	if self.target:
    		context = getattr(context, self.target)

    	if callable(context):
    		context = context()

    	if (type(context) is in (list, tuple, GeneratorType) and not mode) or mode == LIST_MODE:
    		return self.generate_list(context)

    	if self.widget == 'ref':
    		return self.generate(context, self.find(self.to))

    	widget = EflWidget(self.widget) #{ 'widget', 'id?', 'class?', 'mode?' 'target?', ref_only:'to?' }

    	for child in self:
    		widget.append( self.generate(context, child, mode=child.mode) )

    	return [widget]

    def __iter__(self):
        pass
        # Loop through widgets

