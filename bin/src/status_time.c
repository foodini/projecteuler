#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

char * prompt;
time_t startTime;

void handler(int unused) {
  int exitstatus;
  if (waitpid(-1, &exitstatus, WNOHANG | WUNTRACED)) {
    exit(exitstatus>>8);
  }
  exit(1);
}

int main(int argc, char *argv[]) {
  pid_t pid = fork();
  int i;
  if (pid != 0) { //parent
    char buf[80];
    buf[79] = 0;
    signal(SIGCHLD, handler);
    prompt = getenv("PROMPT_BNW");
    startTime = time(NULL);
    int elapsedTime;
    while (1) {
      elapsedTime = time(NULL) - startTime;
      int bufPos = 78;
      buf[bufPos--] = '0' + elapsedTime%10; elapsedTime /= 10;
      buf[bufPos--] = '0' + elapsedTime%6;  elapsedTime /= 6;
      buf[bufPos--] = ':';
      if (elapsedTime) {
        buf[bufPos--] = '0' + elapsedTime%10; elapsedTime /= 10;
        buf[bufPos--] = '0' + elapsedTime%6;  elapsedTime /= 6;
        buf[bufPos--] = ':';
      }
      while (elapsedTime) {
        buf[bufPos--] = '0' + elapsedTime%10;
        elapsedTime /= 10;
      }
      printf ("\033]0; %s %s", buf+bufPos+1, prompt);
      for (i=1; i<argc; ++i) 
        printf("%s ", argv[i]);
      printf("\a");
      fflush(stdout);
      sleep(1);
    }
  } else {
    execvp(argv[1], argv+1);
  }
}
