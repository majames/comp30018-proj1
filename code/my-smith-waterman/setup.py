from distutils.core import setup, Extension

subdist_module = Extension('mysmithwaterman',
                    sources = ['subdist.c'])

description = """A C extension that uses a Smith Waterman
 to calculate fuzzy matches for substrings.

Usage:
import mysmithwaterman

MIT License
"""

setup (name = 'mysmithwaterman',
       version = '0.2.1',
       description = 'Substring edit distance',
       long_description = description,
        author = "Michael James",
        author_email = "majames91@gmail.com",
        download_url = "http://learnerxp.com",
        url="http://learnerxp.com",
        license="MIT",
       ext_modules = [subdist_module])
      
