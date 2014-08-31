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

int equal(char x, char y);

// minimum of two values
long min2(size_t a, size_t b)
{
	if (a < b)
	{
		return a;
	}
	return b;
}

// minimum of three values
long min3(size_t a, size_t b, size_t c)
{
	return min2(a, min2(b, c) ) ;
}

// fuzzy substring match
long substring_c(size_t needle_len, Py_UNICODE *needle_str,
		size_t haystack_len, Py_UNICODE *haystack_str)
{
	
	int **Matrix;
	int i, j;

	Matrix = (int **) malloc((needle_len+1)*sizeof(int*));
	for(i=0; i<=needle_len; i++)
		Matrix[i] = (int*) malloc((haystack_len+1)*sizeof(int));	

	for( i=0 ; i<=needle_len ; i++ )   Matrix[i][0] = i;
		
	for( j=0 ; j<=haystack_len ; j++ ) {
		if(j==0 || haystack_str[j-1] == ' ')		
			Matrix[0][j] = 0;
		else
			Matrix[0][j] = Matrix[0][j-1] + 1;
	}
	
	for( i=1 ; i<=needle_len ; i++ )
		for( j=1 ; j<=haystack_len ; j++ )
			Matrix[i][j] = min3(
				Matrix[i-1][j] + 1,
				Matrix[i][j-1] + 1,
				Matrix[i-1][j-1] + equal(haystack_str[j-1], needle_str[i-1]));


	// return min(row1)
	long min_cost = needle_len;
	for (i = 1; i <= haystack_len; ++i)
	{
		if (Matrix[needle_len][i] < min_cost)
		{
			min_cost = Matrix[needle_len][i];
		}
	}
	return min_cost;
}

int equal(char x, char y) {
	if(x==y)
		return 0;
	return 1;
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

	if (needle_len == 0) // avoid divide by zero errors
	{
		return PyFloat_FromDouble(0.0) ;
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

	double score = ((double)needle_len - (double)distance) / (double)needle_len ;
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
PyMODINIT_FUNC initmysubdist(void)
{
	PyObject *module = Py_InitModule3("mysubdist", 
                                      subdist_methods, 
                                      subdist_doc);
	PyModule_AddStringConstant(module, 
                              "__version__", 
                              SUBDIST_VERSION);
	PyModule_AddStringConstant(module,
                               "__author__",
                               AUTHOR);
}
