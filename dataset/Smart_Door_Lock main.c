/******************************************************************************/
/* Main
	Smart Door Lock Code
	Revised
	By Wilson Mach and Falcon Wong
	Built upon Wilson's code
	
															*/
/******************************************************************************/

/* Device header file */
#if defined(__XC16__)
    #include <xc.h>
#elif defined(__C30__)
    #if defined(__PIC24E__)
    	#include <p24Exxxx.h>
    #elif defined (__PIC24F__)||defined (__PIC24FK__)
	#include <p24Fxxxx.h>
    #elif defined(__PIC24H__)
	#include <p24Hxxxx.h>
    #endif
#endif

#include <stdint.h>        /* Includes uint16_t definition                    */
#include <stdbool.h>       /* Includes true/false definition                  */
#include <stdlib.h>
#include <stdio.h>

#include "system.h"        /* System funct/params, like osc/peripheral config */
#include "user.h"          /* User funct/params, such as InitApp              */

#include "database.h"
#include "debug.h"
#include "event.h"
#include "fingerPrintReader.h"
#include "miscHardware.h"
#include "wifi.h"

char debug[20];
uint8_t lockFlag = FALSE;			 //used to let the microcontroller know when to lock the door based on wether or not the door is open.

/******************************************************************************/
/* Main Program                                                               */
/******************************************************************************/

int16_t main(void)
{
    InitApp(); 
    while(1) {

        if (switchIsOn()){
            turnOnLED(3);
            lockFlag = FALSE;
        }
        else{
            turnOffLED(3);
        }

        if (buttonIsPressed()) { 		//basic button functions (identify when closed and server mode on when open)
            if (switchIsOn()){
                WifiStart(SERVER_MODE);
            }
            else {
                FPRStart();
                action = IDENTIFY;
                sendFPRCommand(FPR_IS_PRESSED, ZERO);
                
            }
        }

        switch (reqType) {
            case GET_PAGE:
                if (switchIsOn()) sendPage();
                else sendResponse("Error: Door is closed.");
                reqType = DEFAULT;
                reqParseState = DEFAULT;
                break;
            case POST_ENROLL:
                reqType = DEFAULT;
                action = ENROLL;
                if (wifiEnrollProgress != 0) break;
                pendingUserID = findEmptySpot();
                FPRStart();
                int newUser = (uint32_t)pendingUserID;
                sendFPRCommand(FPR_ENROLL_START, newUser);
                break;
            case POST_DELETE:
                reqType = DEFAULT;
                sendFPRCommand(FPR_DELETE_ALL, ZERO);
                deleteDatabase();
                break;
            case POST_SET_WIFI:
                saveWifiInfo();
delay(4000);								//This 4 seconds delay is for demonstrating purposes. I needed to have some time to turn on my hotspot before the program starts connecting to it. 
                WifiStart(CLIENT_MODE);
delay(1000);
                sendUpdate();
                updateFlag = TRUE;
                reqType = DEFAULT;
                break;
            default:
                if(lockFlag == FALSE){
                        if (!switchIsOn()) {
                            setTimeout(3);
                            action = TIMEOUT_LOCK;
                            FPRState = PARSE_FPR_MSG;
                            lockFlag = TRUE;
                        }
                    }
                if((minute % 30) == 0 && (updateFlag == FALSE)){
                        WifiStart(CLIENT_MODE);
delay(1000);
                        sendUpdate();
                        updateFlag = TRUE;
                        delay(500);
                        turnOnWifiChip(FALSE);
                    }
                break;
        }


        if (FPRState == PARSE_FPR_MSG) {  //used after a fingerprint response is returned

            int i = 0;
            switch (action) {
                case DOOR_IS_OPENED:
                    if (!switchIsOn()) {
                        setTimeout(5);
                        action = TIMEOUT_LOCK;
                    }
                    break;
                case IDENTIFY:
                    identify();
                    break;
                case ENROLL:
                    enroll();
                    break;
                case DELETE:
                    sendFPRCommand(FPR_DELETE_ALL, ZERO);
                    break;
                case DELETE_USER:
                    while(newDeleted[i] != 0xFF){
                        sendFPRCommand (FPR_DELETE_ID, newDeleted[i++]);
                        delay(200);
                    }
                    action = DEFAULT;
                    break;
                case OPEN_DOOR:
                   // WifiStart(SERVER_MODE);
                    turnAllLEDOff();
                    turnOnLED(1);
                    setTimeout(5);
                    action = TIMEOUT_LOCK;
                    lockDeadBolt(FALSE);
                    lockFlag = FALSE;
                    break;
                case TIMEOUT_LOCK:
                    if (switchIsOn()) {
                        action = DOOR_IS_OPENED;
                    } else if (isTimeout()) {
                        turnOnWifiChip(FALSE);
                        lockDeadBolt(TRUE);
                        lockFlag = TRUE;
                        action = DEFAULT;
                    }
                    break;
                case FINGER_NOT_FOUND:
                    turnAllLEDOff();
                    turnOnLED(0);
                    action = DEFAULT;
                    FPRState = DEFAULT;
                    break;

            }
        }
    }
}