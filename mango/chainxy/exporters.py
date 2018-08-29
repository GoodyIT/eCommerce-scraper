from scrapy.exporters import CsvItemExporter

class HeadlessCsvItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):

        # args[0] is (opened) file handler
        # if file is not empty then skip headers
        print('&&&&&&&& args', args[0], args[0].tell())
        if len(args[0].readlines()) > 0:
            kwargs['include_headers_line'] = False

        super(HeadlessCsvItemExporter, self).__init__(*args, **kwargs)