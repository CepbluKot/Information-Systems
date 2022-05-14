#include <netdb.h>
#include <netinet/in.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <net/if.h>
#include <arpa/inet.h>
#include <rtl/stdbool.h>


#define DISCOVERING_IFACE_MAX   10
#define TIME_STEP_SEC           5


#define RECEIVE_BUF_SIZE        1024
#define EXAMPLE_PORT            1106
#define MAX_PENDING_CONNECTIONS 10

#define ANSI_COLOR_RED   "\x1b[31m"
#define ANSI_COLOR_RESET "\x1b[0m"


static const char LogPrefix[] = "[Client]";

static void printErrorMessage(const char *message)
{
    printf(ANSI_COLOR_RED);
    perror(message);
    printf(ANSI_COLOR_RESET);
}

int main (int argc, const char* argv[])
{
    // unsigned int      i;
    int               socketfd;
    struct            ifconf conf;
    struct            ifreq req[DISCOVERING_IFACE_MAX];
    // struct            ifreq *ifr;
    // struct sockaddr * sa;

    fprintf(stderr, "%s Opening socket...", LogPrefix);

    socketfd = socket(AF_ROUTE, SOCK_RAW, 0);
    if (socketfd < 0)
    {
        fprintf(stderr, "\n%s cannot create socket\n", LogPrefix);
        return EXIT_FAILURE;
    }

    fprintf(stderr, " OK\n");

    while (rtl_true)
    {


        struct sockaddr_in stSockAddr;

    /* Create receiving socket for incomming connection requests. */
    int serverSocketFD = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    /* Allow port reuse, otherwise it will be unavailable for 2xMSL after program finished. */
    if (setsockopt(serverSocketFD, SOL_SOCKET, SO_REUSEADDR, &(int) {1}, sizeof(int)) < 0)
    {
        printErrorMessage("setsockopt(SO_REUSEADDR) failed");
        return EXIT_FAILURE;
    }

    if (-1 == serverSocketFD)
    {
        printErrorMessage("Can not create socket");
        return EXIT_FAILURE;
    }

    /* Create and initialise socket`s address structure. */
    memset(&stSockAddr, 0, sizeof(stSockAddr));

    stSockAddr.sin_family = AF_INET;
    stSockAddr.sin_port = htons(EXAMPLE_PORT);
    stSockAddr.sin_addr.s_addr = htonl(INADDR_ANY);

    /* Bind socket with local address. */
    if (-1 == bind(serverSocketFD, (struct sockaddr *)&stSockAddr, sizeof(stSockAddr)))
    {
        printErrorMessage("Error bind failed");
        close(serverSocketFD);
        return EXIT_FAILURE;
    }

    /* Set socket to listening state. */
    if (-1 == listen(serverSocketFD, MAX_PENDING_CONNECTIONS))
    {
        printErrorMessage("Error listen failed");
        close(serverSocketFD);
        return EXIT_FAILURE;
    }
    {

        fd_set readset;

        FD_ZERO(&readset);
        FD_SET(serverSocketFD, &readset);
        
        while(1){
        /* Waiting for incoming connection request. */
        if (select(serverSocketFD + 1, &readset, NULL, NULL, NULL) == 1)
        {
            /* Receiving of incoming connection request. */
            int ConnectFD = accept(serverSocketFD, NULL, NULL);

            if (ConnectFD == -1)
            {
                printErrorMessage("Error accept failed");
                close(serverSocketFD);
                return EXIT_FAILURE;
            }

            char buf[RECEIVE_BUF_SIZE];

            /* Read data from incoming connection. */
            if (-1 == recv(ConnectFD, buf, sizeof(buf), 0))
            {
                printErrorMessage("recv failed");
                close(ConnectFD);
                close(serverSocketFD);
                return EXIT_FAILURE;
            }
            else
            {
                /* Print received data in terminal. */
                fprintf(stderr, "Server received: %s", buf);
            }

            /* Close incomming connection. */
            if (-1 == shutdown(ConnectFD, SHUT_RDWR))
            {
                printErrorMessage("Can not shutdown socket");
                close(ConnectFD);
                close(serverSocketFD);
                return EXIT_FAILURE;
            }

            /* Close accepted connection handler. */
            close(ConnectFD);
        }
        else
        {
            /* In case of error close receive socket. */
            close(serverSocketFD);
            return EXIT_FAILURE;
        }
    }
    }
    /* Stop processing of incoming connection requests. */
    shutdown(serverSocketFD, SHUT_RDWR);
    close(serverSocketFD);

        // fprintf(stderr, "%s Discovering interfaces...\n", LogPrefix);

        // for (i = 0; i < (unsigned int)conf.ifc_len / sizeof(req[0]); i ++)
        // {
        //     ifr = &conf.ifc_req[i];
        //     sa = (struct sockaddr *) &ifr->ifr_addr;

        //     if (sa->sa_family == AF_INET)
        //     {
        //         struct sockaddr_in *sin = (struct sockaddr_in*) &ifr->ifr_addr;

        //         fprintf(stderr, " i dunno %s  mb aipishnik %s\n",
        //                 ifr->ifr_name, inet_ntoa(sin->sin_addr));
        //     }
        // }

    sleep(TIME_STEP_SEC);
  }

  return EXIT_SUCCESS;
}
