#include <sys/inotify.h>
#include <sys/epoll.h>
#include <errno.h>
#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>

#define ARGERROR -1
#define INOTERROR -2
#define WATCHERROR -3

int main(int argc, char* argv[]){
	
	int fd, nfd;
	int watch;
	char buf[4096] __attribute__ ((aligned(__alignof__(struct inotify_event))));
        const struct inotify_event *event;	
	size_t len;
	int length;
	FILE * fs;
	
	if(argc != 3){
	   printf("Usage ./inotify_docker <path to directory> <output file>\n");
	   while(1){}
	}

    	if (mkdir(argv[1], S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH) == -1 && errno != EEXIST) {
        	printf("Error: mkdir failed.\n");
        	return -1;
    	}


	fd = inotify_init1(0);
	if(fd == -1){
	   printf("Error: inotify failed.\n");
	   while(1){}
	}

	printf("inotify success\n");


	watch = inotify_add_watch(fd, argv[1], IN_ALL_EVENTS);


	fs = fopen(argv[2], "w");
	if(fs == NULL){
	   printf("could not open file. press crtl-c to exit\n");
	   while(1){}
	}

	printf("reading events\n");

	for(;;){

		len = read(fd, buf, sizeof(buf));
		if(len == -1 && errno != EAGAIN){
			perror("read");
		        while(1){}	
	  	}
		if(len <= 0){
			break;
		} 
		char * ptr = buf;
		while(ptr < buf + len) {
			event = (const struct inotify_event *)ptr;
			ptr += sizeof(struct inotify_event) + event->len;
            	
     	            /* Print the name of the file. */
					
			if (event->len && event->mask == IN_CREATE){ 		
				fs = fopen(argv[2], "a");
			        if(fs == NULL){
           				printf("could not open file. press crtl-c to exit\n");
           				while(1){}
			        }
				fprintf(fs, "%s was created \n", event->name);
				fflush(fs);
		    	}else if(event->len && event->mask == IN_DELETE){
				fs = fopen(argv[2], "a");
				if(fs == NULL){
				   printf("could not open file. press crtl-c to exit\n");
				   while(1){}
				}
				fprintf(fs,"%s was deleted \n", event->name);
				fflush(fs);
			}
		}

	}

	return 0;
}
