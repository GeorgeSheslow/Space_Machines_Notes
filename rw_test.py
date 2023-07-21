#!/usr/bin/env python

import can

# msg = can.Message(arbitration_id=0xc0ffee, data=[id, i, 0, 1, 3, 1, 4, 1], is_extended_id=False)
# bus.send(msg)

#make checksum function
def checksum(data_1,data_2,data_3,data_4,data_5):
    checksum_result = 0
    for i in data_1:
        checksum_result = (checksum_result + i) & 0xff
    for i in data_2:
        checksum_result = (checksum_result + i) & 0xff
    for i in data_3:
        checksum_result = (checksum_result + i) & 0xff
    for i in data_4:
        checksum_result = (checksum_result + i) & 0xff
    for i in data_5:
        checksum_result = (checksum_result + i) & 0xff
    
    return checksum_result

def main():

    bus = can.interface.Bus(bustype="socketcan", channel="vcan0", bitrate=1000000)

    while True:
        try:
            # Receive request
            can_msg = bus.recv()
            
            # version info
            if can_msg.arbitration_id == 0x330 and can_msg.data[0] == 0x0A and can_msg.data[1] == 0xD2:
                print("Sending Version Info request response")
                # return message
                msg = can.Message(arbitration_id=0x730, is_extended_id=False,dlc=8, data=[0x0A,0xD2,0x00,0x02,0x00,0x04,0x00,0x00])
                bus.send(msg)

            # telemetry request
            if can_msg.arbitration_id == 0x330 and can_msg.data[1] == 0xFF:
                print("Sending Telemetry request response") 
                # 5 can frames to return
                first_frame = can.Message(arbitration_id=0x731, is_extended_id=False,dlc=8,data=[0x00,0x25,0x00,0xFF,0x02,0x05,0x03,0x01])
                second_frame = can.Message(arbitration_id=0x732, is_extended_id=False,dlc=8,data=[0x04, 0x00,0x00,0x00,0x00,0x00,0x00,0x00])
                third_frame = can.Message(arbitration_id=0x732, is_extended_id=False,dlc=8,data=[0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00])
                fourth_frame = can.Message(arbitration_id=0x732, is_extended_id=False,dlc=8,data=[0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00])
                fifth_frame = can.Message(arbitration_id=0x733, is_extended_id=False,dlc=8,data=[0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00])

                # add checksum
                fifth_frame.data[7] = checksum(first_frame.data, second_frame.data, third_frame.data, fourth_frame.data, fifth_frame.data)

                # send all the data

                bus.send(first_frame)
                bus.send(second_frame)
                bus.send(third_frame)
                bus.send(fourth_frame)
                bus.send(fifth_frame)

        except can.CanError as e:
            print(e)

if __name__ == "__main__":
    main()