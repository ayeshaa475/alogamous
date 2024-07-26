from alogamous import analyzer, log_line_parser


class FormatAnalyzer(analyzer.Analyzer):
    def __init__(self, line_parser):
        self.parser = line_parser
        self.startup_block = False
        self.un_formated_lines = []

    def read_log_line(self, line):
        line_type = self.parser.parse(line)["type"]
        if self.startup_block is False:
            if line_type == log_line_parser.LineType.UNSTRUCTURED_LINE:
                self.un_formated_lines.append(line)
            elif line_type == log_line_parser.LineType.HEADER_LINE:
                self.startup_block = True
        elif self.startup_block is True and line_type == log_line_parser.LineType.HEADER_LINE:
            self.startup_block = False

    def report(self, out_stream):
        out_stream.write("\nLines that do not conform to log format:\n- ")
        out_stream.write("\n- ".join(self.un_formated_lines))