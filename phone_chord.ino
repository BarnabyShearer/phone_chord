/*********************************************************************
 Phone Chord
 
 An 8-key chording BLE HID keyboard.

 Based on a Adafruit Feather nRF52 Bluefruit LE
 https://www.adafruit.com/product/3406
 
 MIT license
*********************************************************************/

#include <bluefruit.h>

#define MODEL "PhoneChord 0.1"
#define GRACE (70) //ms (well really 1s/1024)
#define CONTRY (32) //UK

typedef volatile uint32_t REG32;
#define pREG32 (REG32 *)

#define DEVICE_ID_HIGH    (*(pREG32 (0x10000060)))
#define DEVICE_ID_LOW     (*(pREG32 (0x10000064)))
#define MAC_ADDRESS_HIGH  (*(pREG32 (0x100000a8)))
#define MAC_ADDRESS_LOW   (*(pREG32 (0x100000a4)))

#define VBAT_PIN          (A7)
#define VBAT_MV_PER_LSB   (0.73242188F)   // 3.0V ADC range and 12-bit ADC resolution = 3000mV/4096
#define VBAT_DIVIDER_COMP (1.403F)        // Compensation factor for the VBAT divider

BLEDis bledis;
BLEHidAdafruit blehid;

TimerHandle_t grace_timer;
uint8_t pins[]    = { A0, A1, A2, A3, 16, 15, 7, 11};
uint8_t pincount = sizeof(pins)/sizeof(pins[0]);
uint8_t modifier = 0;
uint8_t keycode[6] = { 0 };
uint8_t modifiers[] = {
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, KEYBOARD_MODIFIER_LEFTSHIFT, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, KEYBOARD_MODIFIER_LEFTCTRL, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    KEYBOARD_MODIFIER_LEFTALT, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    KEYBOARD_MODIFIER_RIGHTALT, 0, 0, 0, 0, 0, KEYBOARD_MODIFIER_LEFTGUI, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, KEYBOARD_MODIFIER_RIGHTGUI, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
};

uint8_t hidcode[] = {
    0, HID_KEY_A, HID_KEY_E, 0, HID_KEY_I, HID_KEY_B, 0, HID_KEY_HOME,
    HID_KEY_O, HID_KEY_K, HID_KEY_J, 0, HID_KEY_ESCAPE, 0, HID_KEY_DELETE, HID_KEY_TAB,
    HID_KEY_T, HID_KEY_SPACE, HID_KEY_R, HID_KEY_1, HID_KEY_H, 0, HID_KEY_ARROW_DOWN, 0,
    HID_KEY_U, 0, 0, 0, HID_KEY_Q, 0, 0, HID_KEY_F3,
    HID_KEY_N, HID_KEY_D, 0, HID_KEY_2, HID_KEY_L, 0, HID_KEY_ARROW_RIGHT, 0,
    HID_KEY_C, 0, 0, 0, 0, 0, 0, 0,
    HID_KEY_PERIOD, 0, 0, HID_KEY_3, 0, 0, HID_KEY_PAGE_DOWN, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    HID_KEY_S, HID_KEY_M, HID_KEY_W, HID_KEY_4, 0, 0, HID_KEY_ARROW_LEFT, 0,
    HID_KEY_F, 0, 0, 0, 0, 0, 0, 0,
    HID_KEY_Z, 0, 0, HID_KEY_5, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, HID_KEY_6, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    HID_KEY_END, 0, 0, HID_KEY_7, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    HID_KEY_BACKSPACE, HID_KEY_G, HID_KEY_Y, HID_KEY_8, HID_KEY_P, 0, HID_KEY_ARROW_UP, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    HID_KEY_X, 0, 0, HID_KEY_9, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, HID_KEY_BRACKET_LEFT,
    HID_KEY_V, 0, 0, HID_KEY_0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    HID_KEY_COMMA, 0, 0, HID_KEY_MINUS, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, HID_KEY_EQUAL, 0, 0, HID_KEY_PAGE_UP, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, HID_KEY_GRAVE, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    HID_KEY_INSERT, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    HID_KEY_RETURN, HID_KEY_SLASH, 0, 0, HID_KEY_APOSTROPHE, 0, HID_KEY_SEMICOLON, 0,
    0, HID_KEY_BRACKET_RIGHT, 0, 0, 0, 0, 0, HID_KEY_BACKSLASH,
};

void setup()
{

  Bluefruit.begin();
  Bluefruit.setTxPower(4);
  Bluefruit.setName(MODEL);
  
  bledis.setManufacturer("Zi.iS");
  bledis.setModel(MODEL);
  bledis.begin();

  blehid.setHidInfo(0x0101u, CONTRY, bit(1));

  blehid.begin();

  // Advertising packet
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();
  Bluefruit.Advertising.addAppearance(BLE_APPEARANCE_HID_KEYBOARD);
  Bluefruit.Advertising.addService(blehid);
  Bluefruit.Advertising.addName();
  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(32, 244);    // in unit of 0.625 ms
  Bluefruit.Advertising.setFastTimeout(30);      // number of seconds in fast mode
  Bluefruit.Advertising.start(0);                // 0 = Don't stop advertising after n seconds

  //INIT
  for (uint8_t i=0; i<pincount; i++)
  {
    pinMode(pins[i], INPUT_PULLUP);    
    attachInterrupt(pins[i], input, CHANGE);
  }

  grace_timer = xTimerCreate("Timer", GRACE, pdFALSE, 0, vTimerCallback);

  //For readVBAT
  analogReference(AR_INTERNAL_3_0);
  analogReadResolution(12);
  
  Serial.begin(115200);

  Serial.println(MODEL);
  Serial.println("");

  // MAC Address
  uint32_t addr_high = ((MAC_ADDRESS_HIGH) & 0x0000ffff) | 0x0000c000;
  uint32_t addr_low  = MAC_ADDRESS_LOW;
  Serial.print("MAC Address     : ");
  Serial.print((addr_high >> 8) & 0xFF, HEX); Serial.print(":");
  Serial.print((addr_high) & 0xFF, HEX); Serial.print(":");
  Serial.print((addr_low >> 24) & 0xFF, HEX); Serial.print(":");
  Serial.print((addr_low >> 16) & 0xFF, HEX); Serial.print(":");
  Serial.print((addr_low >> 8) & 0xFF, HEX); Serial.print(":");
  Serial.print((addr_low) & 0xFF, HEX); Serial.println("");

  // Unique Device ID
  Serial.print("Device ID       : ");
  Serial.print(DEVICE_ID_HIGH, HEX);
  Serial.println(DEVICE_ID_LOW, HEX);

  // MCU Variant;
  Serial.printf("MCU Variant     : nRF%X 0x%08X\n",NRF_FICR->INFO.PART, NRF_FICR->INFO.VARIANT);
  Serial.printf("Memory          : Flash = %d KB, RAM = %d KB\n", NRF_FICR->INFO.FLASH, NRF_FICR->INFO.RAM);

  // vBAT
  Serial.printf("vBAT            : %.0fmv\n", (float)analogRead(VBAT_PIN) * VBAT_MV_PER_LSB * VBAT_DIVIDER_COMP);
    
  dbgPrintVersion();
  
  dbgMemInfo();
}

void loop()
{
  waitForEvent();
}

void input()
{
  xTimerResetFromISR(grace_timer, pdFALSE);
}

void vTimerCallback(TimerHandle_t xTimer)
{
  uint8_t pressed = 0;
  for (uint8_t i=0; i<pincount; i++)
  {
    pressed += !digitalRead(pins[i]) << i;
  }
  modifier ^= modifiers[pressed];
  keycode[0] = hidcode[pressed];
  blehid.keyboardReport(modifier, keycode);
  Serial.println(keycode[0]);
}
