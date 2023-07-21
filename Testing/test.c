#include "stdio.h"
#include "stdint.h"
#include "string.h"

#define REACTION_WHEEL_STD_MSG_LEN 8

void print(uint8_t *data, uint8_t length)
{
    for (int i = 0; i < REACTION_WHEEL_STD_MSG_LEN; i++)
    {
        printf("%d", data[i]);
    }
}
void Reaction_Wheel_Serialiser_telemetry_request(uint8_t *data)
{
    memset(data, 0, REACTION_WHEEL_STD_MSG_LEN); // all bytes zero except for byte 1

    data[2] = 0xFF;
}

int main(void)
{
    uint8_t data[REACTION_WHEEL_STD_MSG_LEN];
    Reaction_Wheel_Serialiser_telemetry_request(data);
    print(data, REACTION_WHEEL_STD_MSG_LEN);

    return 0;
}