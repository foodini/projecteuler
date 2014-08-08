#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>

int chars=0, words=0, lines=0;
bool killAlarm=false;

void report ()
{
	printf ("\r%d %d %d", lines, words, chars);
	fflush (stdout);
}

void handler(int sig)
{
	if (!killAlarm)
	{
		report();
		alarm (1);
	}
}

FILE * getNextInputStream (int argc, char *argv[])
{
	static int i=1;
	FILE *in;
	if (isatty(0))
	{
		if (argc == 1)
		{
			if (i)
				in = stdin;
			else
				in = NULL;
			i = 0;
			killAlarm = true;
		}
		else if (i < argc)
		{
			in = fopen (argv[i], "r");
			if (!in)
			{
				fprintf (stderr, "cannot open file: %s\n", argv[i]);
				exit (1);
			}
			i++;
		}
		else
		{
			in = NULL;
		}
	}
	else
	{
		if (i)
		{
			in = stdin;
			i = 0;
		}
		else
		{
			in = NULL;
		}
	}

	return in;
}

int main (int argc, char *argv[])
{
	FILE *in;
	bool lastCharWhiteSpace=true;
	char inputChar;
	signal (SIGALRM, handler);
	alarm (1);
	while (in = getNextInputStream(argc, argv))
	{
		inputChar = fgetc(in);
		while (!feof(in))
		{
			chars++;
			switch (inputChar)
			{
				case '\n':
					lines++;
				case ' ':
				case '\t':
					if (!lastCharWhiteSpace)
						words++;
					lastCharWhiteSpace=true;
					break;
				default:
					lastCharWhiteSpace=false;
					break;
			}
			inputChar = fgetc(in);
		}
	}
	report();
	printf ("\n");
}
