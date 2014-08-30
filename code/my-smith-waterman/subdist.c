/**
 * subdist.c
 *Copyright (C) Ryan Ginstrom <software@ginstrom.com>
 *
 * MIT License
 **/
#include <Python.h>

#define SUBDIST_VERSION "0.2.1"
#define AUTHOR "Ryan Ginstrom"

static char
		subdist_doc[] =
				"This module uses Levenshtein distance to find fuzzy\n\
	substring matches.\n\n\
	Usage:\n\
	from subdist import substring\n\
	print substring(u\"needle\", u\"Find the needle in the haystack\")\n\n\
	MIT License";

static char
		subdist_substring_doc[] =
				"substring(needle, haystack)\n\
	\n\
	Return the Levenshtein (edit) distance of needle in haystack.\n\
	needle and haystack must be Unicode strings.";

static char
		subdist_get_score_doc[] =
				"get_score(needle, haystack)\n\
	\n\
	Return the fuzzy match of needle in haystack as float\n\
	between 0.0 (no match) and 1.0 (perfect match), based\n\
	on Levenshtein (edit) distance.\n\
	needle and haystack must be Unicode strings.";

long equal(char, char);


long min2(int x, int y) {
	if(x<y)
		return x;
	return y;
}

// The maximum of 2 values
long max2(int x, int y) {
	if(x>y)
		return x;
	return y;
}

long max4(int a, int b, int c, int d) {
	return max2(max2(a,b), max2(c,d));
}

// fuzzy substring match
long substring_c(size_t len_str1, Py_UNICODE *str1,
		size_t len_str2, Py_UNICODE *str2)
{
	// keep static buffers around to avoid allocating memory each call
	int **Matrix;

	int i, j;
	Matrix = (int **) malloc((len_str1+1)*sizeof(int*));
	for(i=0; i<=len_str1; i++)
		Matrix[i] = (int*) malloc((len_str2+1)*sizeof(int));

	// populate the smith-waterman array with values
	for( i=0 ; i<=len_str1 ; i++ ) Matrix[i][0] = 0;
	for( j=0 ; j<=len_str2 ; j++ ) Matrix[0][j] = 0;
	
	for( i=1 ; i<=len_str1 ; i++ )
		for( j=1 ; j<=len_str2 ; j++ )
			Matrix[i][j] = max4(
				0,
				Matrix[i-1][j] - 1,
				Matrix[i][j-1] - 1,
				Matrix[i-1][j-1] + equal(str1[i-1], str2[j-1]));

	// find the max allignment value in the array
	int score = -1;
	
	for(i=0; i<=len_str1; i++) {
		for(j=0; j<=len_str2; j++) {
			score = max2(Matrix[i][j], score);
		}
	}

	return score;
}

long equal(char x, char y) {
	if(x == y)
		return 1;
	return -1;
}

// substring(needle, haystack)
static PyObject* substring_py(PyObject *self, PyObject *args)
{
	// Unpack our arguments
    Py_UNICODE *needle, *haystack;
    long needle_len, haystack_len ;
	if (!PyArg_ParseTuple(args, "u#u#", &needle, 
                                        &needle_len, 
                                        &haystack, 
                                        &haystack_len)) 
    {
		return NULL;
	}

	// Call the pure-C function with nice C data types
	long distance = substring_c(needle_len,
			needle,
            haystack_len,
			haystack) ;

	if (distance < 0)
	{
		return NULL;
	}
	return PyInt_FromLong(distance);
}

// get_score(needle, haystack) -> float[0.0, 1.0]
static PyObject* get_score_py(PyObject *self, PyObject *args)
{
	// Unpack our arguments
    Py_UNICODE *needle, *haystack;
    long needle_len, haystack_len ;
	if (!PyArg_ParseTuple(args, "u#u#", &needle, 
                                        &needle_len, 
                                        &haystack, 
                                        &haystack_len)) 
    {
		return NULL;
	}

	// avoid divide by zero errors
	if (needle_len == 0 || haystack_len == 0) 
	{
		return PyFloat_FromDouble(0.0) ;
	}

	// Call the pure-C function with nice C data types
	long distance = substring_c(needle_len,
			needle,
            haystack_len,
			haystack) ;

	if (distance < 0)
		return NULL;
	

	double score = (double) distance / min2(needle_len, haystack_len) ;
	return PyFloat_FromDouble(score);
}

// The module's methods
static PyMethodDef subdist_methods[] =
{
{ "get_score", get_score_py, METH_VARARGS, subdist_get_score_doc },
{ "substring", substring_py, METH_VARARGS, subdist_substring_doc },
{ NULL, NULL } /* sentinel */
};

// Initializes the module
PyMODINIT_FUNC initmysmithwaterman(void)
{
	PyObject *module = Py_InitModule3("mysmithwaterman", 
                                      subdist_methods, 
                                      subdist_doc);
	PyModule_AddStringConstant(module, 
                              "__version__", 
                              SUBDIST_VERSION);
	PyModule_AddStringConstant(module,
                               "__author__",
                               AUTHOR);
}
