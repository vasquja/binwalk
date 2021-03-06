import os
import gzip
import binwalk.core.plugin

class GzipExtractPlugin(binwalk.core.plugin.Plugin):
    '''
    Gzip extractor plugin.
    '''
    MODULES = ['Signature']
    BLOCK_SIZE = 10 * 1024

    def init(self):
        # If the extractor is enabled for the module we're currently loaded
        # into, then register self.extractor as a zlib extraction rule.
        if self.module.extractor.enabled:
            self.module.extractor.add_rule(txtrule=None,
                                           regex="^gzip compressed data",
                                           extension="gz",
                                           cmd=self.extractor)

    def extractor(self, fname):
        fname = os.path.abspath(fname)
        outfile = os.path.splitext(fname)[0]

        try:
            fpout = open(outfile, "wb")
            gz = gzip.GzipFile(fname, "rb")

            while True:
                data = gz.read(self.BLOCK_SIZE)
                if data:
                    fpout.write(data)
                else:
                    break

            gz.close()
            fpout.close()
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            return False

        return True
