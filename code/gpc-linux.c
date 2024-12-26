#include <stdio.h>
#include <stdlib.h>
#include <string.h>


// --- Command Execution --- //
void RunCommand(const char *exec) {
	char *cmd = (char *)malloc(strlen(exec)+1);

	strcpy(cmd, exec);
	system(cmd);

	free(cmd);
}

int main(void) {
	RunCommand("echo Hello World");
	return 0;
}
