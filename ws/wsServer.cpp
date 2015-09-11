#include <libwebsockets.h>

#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <thread>
#include <algorithm>

using namespace std;

//Global Vector to hold Clients (Sorry)
vector<libwebsocket*> clients;

//HTTP Callback, Does Nothing
int callback_http(struct libwebsocket_context *context,
                  struct libwebsocket *wsi,
                  enum libwebsocket_callback_reasons reason, 
                  void *user, void *in, size_t len)
{
    return 0;
}

//Handles clients connecting and disconnecting
int callback_robot_protocol(struct libwebsocket_context *context,
                            struct libwebsocket *wsi,
                            enum libwebsocket_callback_reasons reason, 
                            void *user, void *in, size_t len)
{
    switch (reason) {
        case LWS_CALLBACK_ESTABLISHED:
            clients.emplace_back(wsi);
            break;
        case LWS_CALLBACK_CLIENT_CONNECTION_ERROR:
        case LWS_CALLBACK_CLOSED:
            clients.erase(std::remove(clients.begin(), clients.end(), wsi), clients.end());
            break;
        default:
            break;
    }

    return 0;
}

static struct libwebsocket_protocols protocols[] = {
    /* first protocol must always be HTTP handler */
    {
        "http-only",   //protocol name
        callback_http, //callback
        0              //per_session_data_size
    },
    {
        "robot-protocol",        //protocol name
        callback_robot_protocol, //callback
        0                        //we don't use any per session data
    },
    {
        NULL, NULL, 0   /* End of list */
    }
};

//Read from STDIN, Send message over Websockets
void read_send() {
    string input;


    //Read the line from STDIN
    while (getline(cin, input)) {
        unsigned char *buf = (unsigned char*) malloc(LWS_SEND_BUFFER_PRE_PADDING
                                    + input.size() + LWS_SEND_BUFFER_POST_PADDING);

        strcpy((char*)&buf[LWS_SEND_BUFFER_PRE_PADDING], input.c_str());

        for (auto& client : clients) {
            libwebsocket_write(client, &buf[LWS_SEND_BUFFER_PRE_PADDING], 
                               input.size(), LWS_WRITE_TEXT);
        }

        free(buf);
    }
}

int main(int argc, char** argv)
{
    int port = 9000;
    if (argc == 2)
        port = atoi(argv[1]);
    else if (argc > 2){
        cerr << "usage: wsServer [port=9000]" << endl;
        cerr << "                 port must be >= 1024" << endl;
        exit(1);
    }
    if (port == 0 || port < 1024) {
        cerr << "usage: wsServer [port=9000]" << endl;
        cerr << "                 port must be >= 1024" << endl;
        exit(1);
    }

    struct libwebsocket_context *context;
    lws_set_log_level(0, NULL);

    //Create context info
    struct lws_context_creation_info context_info;
    context_info.port = port;
    context_info.iface = NULL;
    context_info.protocols = protocols;
    context_info.extensions = NULL;
    context_info.ssl_cert_filepath = NULL;
    context_info.ssl_private_key_filepath = NULL;
    context_info.ssl_ca_filepath = NULL;
    context_info.ssl_cipher_list = NULL;
    context_info.gid = -1;
    context_info.uid = -1;
    context_info.options = 0;
    context_info.user = NULL;
    context_info.ka_time = 0;
    context_info.ka_probes = 0;
    context_info.ka_interval = 0;

    //Create libwebsocket context representing this server
    context = libwebsocket_create_context(&context_info);

    if (context == NULL) {
        fprintf(stderr, "libwebsocket init failed\n");
        return -1;
    }

    //Make and start the thread to read and send STDIN to WS
    std::thread t1(read_send);

    //Infinite loop, to end this server send SIGTERM. (CTRL+C)
    while (1) {
        libwebsocket_service(context, 50);
    }

    libwebsocket_context_destroy(context);

    return 0;
}
