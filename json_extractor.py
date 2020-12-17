from collections import deque
from babel.messages.jslexer import tokenize, unquote_string


# This helper is copied to all necessary files because once again python imports are being a pain
def reopen_normal_read(file_obj, encoding):
    """Re-open a file obj in plain read mode"""
    return open(file_obj.name, "r", encoding=encoding)


JSON_GETTEXT_KEYWORD = 'type'
JSON_GETTEXT_VALUE = 'gettext_string'
JSON_GETTEXT_KEY_CONTENT = 'content'
JSON_GETTEXT_KEY_ALT_CONTENT = 'alt_content'
JSON_GETTEXT_KEY_FUNCNAME = 'funcname'


class JsonExtractor(object):
    def __init__(self, data):
        self.state = 'start'
        self.data = data

        self.token_to_add = None
        self.is_value = False
        self.gettext_mode = False
        self.current_key = None
        self.in_array = False
        self.nested_in_array = []
        self.results = []
        self.token_params = {}

    # TODO: fix the duplicate name between this and the other add_result
    def add_result(self, token):
        value = unquote_string(token.value)
        if value not in self.results:
            self.results[value] = deque()
        self.results[value].append(token.lineno)

    def start_object(self):
        self.gettext_mode = False
        self.state = 'key'

        # Things will be incorrect if an object is contained in an array, so
        # we use a stack of states to return to like this in order to support
        # that kind of JSON structures
        self.nested_in_array.append(self.in_array)
        self.in_array = False

    def with_separator(self, token):
        self.state = 'value'

    def start_array(self):
        self.in_array = True

    def end_array(self):
        self.in_array = False
        self.end_pair()

    def end_pair(self, add_gettext_object=False):
        if self.token_to_add:
            if not self.gettext_mode or (self.gettext_mode and add_gettext_object):
                self.add_result(self.token_to_add)

        if not self.in_array:
            self.current_key = None
            self.state = 'key'

    def end_object(self):
        self.end_pair(add_gettext_object=True)
        self.gettext_mode = False
        self.state = 'end'

        self.in_array = self.nested_in_array.pop()

    def add_result(self, token):
        value = unquote_string(token.value)
        result = dict(
            line_number=token.lineno,
            content=value
        )
        for key, value in self.token_params.items():
            if key == 'alt_token':
                result['alt_content'] = unquote_string(value.value)
                result['alt_line_number'] = value.lineno
            else:
                result[key] = unquote_string(value)

        self.results.append(result)
        self.token_to_add = None
        self.token_params = {}

    def get_lines_data(self):
        """
        Returns string:line_numbers list
        Since all strings are unique it is OK to get line numbers this way.
        Since same string can occur several times inside single .json file the values should be popped(FIFO) from the list
        :rtype: list
        """

        for token in tokenize(self.data):
            if token.type == 'operator':
                if token.value == '{':
                    self.start_object()
                elif token.value == '[':
                    self.start_array()
                elif token.value == ':':
                    self.with_separator(token)
                elif token.value == '}':
                    self.end_object()
                elif token.value == ']':
                    self.end_array()
                elif token.value == ',':
                    self.end_pair()


            elif token.type == 'string':
                if self.state == 'key':
                    self.current_key = unquote_string(token.value)
                    if self.current_key == JSON_GETTEXT_KEYWORD:
                        self.gettext_mode = True
                else:
                    if self.current_key.lower() in (
                    "groupname", "displayname", "name", "messages", "lefttexts", "righttexts"):
                        self.token_to_add = token

        return self.results


def extract_json(file_obj, keywords, comment_tags, options):
    """
    Supports: gettext, ngettext. See package README or github ( https://github.com/tigrawap/pybabel-json ) for more usage info.
    """
    with reopen_normal_read(file_obj, options.get('encoding', 'utf-8')) as f:
        data = f.read()
    json_extractor = JsonExtractor(data)
    strings_data = json_extractor.get_lines_data()

    for item in strings_data:
        messages = [item['content']]
        if item.get('funcname') == 'ngettext':
            messages.append(item['alt_content'])
        yield item['line_number'], item.get('funcname', 'gettext'), tuple(messages), []
