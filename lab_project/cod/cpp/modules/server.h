#include <iostream>
#include <fstream>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
using namespace std;

#define PORT 8080


class serverInterface
{
    public:
        virtual void send_message(string text) { }
        virtual string recieve_message() { }
};


class serverAbstraction : public serverInterface
{
    public:
        serverAbstraction(serverInterface* input_client_interface)
        {
            selected_interface = input_client_interface;
        }

        void send_message(string text) 
        {
            selected_interface->send_message(text);
        }

        string recieve_message() 
        {
            return selected_interface->recieve_message();
        }

    private:
        serverInterface* selected_interface;
};


class UDPServer : public serverInterface
{
    public:
        UDPServer()
        { 
            if ((serSockDes = socket(AF_INET, SOCK_DGRAM, 0)) < 0) std::cerr<<"socket creation error...\n";

            serAddr.sin_family = AF_INET;
            serAddr.sin_port = htons(PORT);
            serAddr.sin_addr.s_addr = INADDR_ANY;

            if ((bind(serSockDes, (struct sockaddr*)&serAddr, sizeof(serAddr))) < 0) 
            {
                cerr << "binding error...\n";
                close(serSockDes);
            }

            cliAddrLen = sizeof(cliAddr);

        }

        void send_message(string text)
        {
            strcpy(msg, text.c_str()); // conver str to char[]
            if (sendto(serSockDes, msg, strlen(msg), 0, (struct sockaddr*)&cliAddr, cliAddrLen) < 0) 
            { 
                perror("sending error...\n");
                close(serSockDes);
            }
        }

        string recieve_message()
        {
            readStatus = recvfrom(serSockDes, buff, 1024, 0, (struct sockaddr*)&cliAddr, &cliAddrLen);
            if (readStatus < 0)
            { 
                perror("reading error...\n");
                close(serSockDes);
            }

            return buff;
        }
    
    private:
        int serSockDes, readStatus;
        struct sockaddr_in serAddr, cliAddr;
        socklen_t cliAddrLen;
        char msg[1024];
        char buff[1024];
};
