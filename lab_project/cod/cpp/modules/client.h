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
            if ((cliSockDes = socket(AF_INET, SOCK_DGRAM, 0)) < 0) std::cerr<<"socket creation error...\n";

            serAddr.sin_family = AF_INET;
            serAddr.sin_port = htons(PORT);
            serAddr.sin_addr.s_addr = inet_addr("127.0.0.1");
            serAddrLen = sizeof(serAddr);
        }

        void send_message(string text)
        {
            strcpy(msg, text.c_str()); // conver str to char[]
            if (sendto(cliSockDes, msg, strlen(msg), 0, (struct sockaddr*)&serAddr, sizeof(serAddr)) < 0) 
            {
                cerr << "sending error...\n";
                close(cliSockDes);
            }
        }

        string recieve_message()
        {
            readStatus = recvfrom(cliSockDes, buff, 1024, 0, (struct sockaddr*)&serAddr, &serAddrLen);

            if (readStatus < 0) 
            {
                cerr << "reading error...\n";
                close(cliSockDes);
            }
            return buff;
        }
    
    private:
        int cliSockDes, readStatus;
        struct sockaddr_in serAddr;
        socklen_t serAddrLen;
        char msg[1024];
        char buff[1024];
};
