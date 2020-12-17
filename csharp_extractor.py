from babel.messages.jslexer import tokenize, unquote_string


class CSharpExtractor(object):
    def __init__(self, data):
        self.state = 'start'
        self.data = data

        self.current_name = None
        self.current_value = None
        self.value_start_line = 0

        self.parenthesis_level = 0

        self.results = []

    def start_call(self):
        self.state = 'call'

    def end_call(self):
        self.state = 'skipping'

        if self.current_name and self.current_value:
            self.add_result()

    def add_result(self):
        result = dict(
            line_number=self.value_start_line,
            content=self.current_value,
            function_name=self.current_name
        )
        self.results.append(result)

        self.current_name = None
        self.current_value = None

    def get_lines_data(self, encoding):
        """
        Returns string:line_numbers list
        Since all strings are unique it is OK to get line numbers this way.
        :rtype: list
        """
        trigger_call_prime = False

        for token in tokenize(self.data.decode(encoding)):
            call_primed = trigger_call_prime
            trigger_call_prime = False

            if token.type == 'operator':
                if token.value == '(':
                    if self.state != 'call' and call_primed:
                        self.start_call()
                    else:
                        self.parenthesis_level += 1
                elif token.value == ')':
                    if self.parenthesis_level == 0:
                        self.end_call()
                    else:
                        self.parenthesis_level -= 1
            elif token.type == 'name' and self.state != 'call':
                trigger_call_prime = True
                self.current_name = token.value
            elif token.type == 'string' and self.state == 'call':
                string_value = unquote_string(token.value)

                if self.current_value is None:
                    self.current_value = string_value
                    self.value_start_line = token.lineno
                else:
                    self.current_value += string_value

        return self.results


def extract_csharp(file_obj, keywords, comment_tags, options):
    """
    Custom C# extract to fix line numbers for Windows
    """
    data = file_obj.read()
    extractor = CSharpExtractor(data)

    for item in extractor.get_lines_data(options.get('encoding', 'utf-8')):
        function = item['function_name']

        if function not in keywords:
            continue

        messages = [item['content']]
        yield item['line_number'], function, tuple(messages), []
