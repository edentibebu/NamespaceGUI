#include <stdio.h>
#include <stdlib.h>


#define LIST_NS "\
#/bin/bash \n\
FILE='list_ns.sh' \n\
chmod +x $FILE \n\
echo \"listing namespaces\" \n\
ip netns \n\
"

void list()
{
    system(LIST_NS);    //it will run the script inside the c code. 
}