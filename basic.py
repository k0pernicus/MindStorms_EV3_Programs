from ev3.ev3dev import Motor, Lcd, get_battery_percentage
from ev3.lego import InfraredSensor, TouchSensor
from PIL import Image,ImageDraw,ImageFont

d = TouchSensor()
b,c = Motor(port=Motor.PORT.B), Motor(port=Motor.PORT.C)
a = InfraredSensor()
lcd = Lcd()

def init_motors():
    b.setup_forever(500, speed_regulation=True)
    c.setup_forever(500, speed_regulation=True)    

def start_motors():
    b.start()
    c.start()

def stop_motors():
    b.stop()
    c.stop()

def check_infrared_sensor():
    return a.prox < 20

def battery_is_low():
    return get_battery_percentage() < 15

def display_battery_message():
    lcd.reset()
    lcd.draw.text((30, 30), "BATTERY LOW...", font=ImageFont.load_default())
    lcd.update()

def turn_right():
    b.setup_time_limited(500,-500)
    start_motors()

def turn_left():
    c.setup_time_limited(500,-500)
    start_motors()

def main():
    search_about_good_conditions = False
    init_motors()
    start_motors()
    while True:
        if battery_is_low():
            display_battery_message()
        if check_infrared_sensor():
            stop_motors()
            search_about_good_conditions = True
            turn_right()
        else:
            if search_about_good_conditions:
                search_about_good_conditions = False
                init_motors()
                start_motors()
        if d.is_pushed:
            break           

if __name__=="__main__":
    main()


