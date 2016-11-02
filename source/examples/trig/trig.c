#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#ifndef FUNC
#error FUNC must be defined on the command line
#endif
/* standard stringify trick */
#define ss(x) #x
#define s(x) ss(x)

int main(int argc, char *argv[])
{
	double x = 0.0, y;

	/* Error checking omitted. */
	if (argc > 1)
		x = strtod(argv[1], NULL);
	y = FUNC(x);
	printf("%s(%f) = %f\n", s(FUNC), x, y);
	return 0;
}
