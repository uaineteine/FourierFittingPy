Execute test module to test otherwise just import ffit and punch in the order of the series form you want.

The default setup is a_i cos(2pi i (x-b_i) ) for an ith order series.

Run using ffit.attemptFit(numpy array of x data, numpy array of y data, int n order series you wish to fit, optional:interger of max iterations to attempt per variable)
*Default iterations per variable is 100
*Returns: numpy array of the fit values, float the RMS error, numpy array of the a terms, numpy array of the b terms.

Please modify this for your own use/model if required. Is simple enough to need only modifiy some functions and leave the rest alone.