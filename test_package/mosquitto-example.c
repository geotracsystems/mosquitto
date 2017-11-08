#include <stdio.h>

#include "mosquitto.h"

int main()
{
	struct mosquitto* client;
	const char* CLIENT_ID = "test_mqtt";

	mosquitto_lib_init();

	client = mosquitto_new(CLIENT_ID, true, NULL);

	mosquitto_destroy(client);

	mosquitto_lib_cleanup();

	printf("It worked\n");

	return 0;
}
