import time
import pickle
import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.core.window import Window
Window.size = (Window.width*1, Window.height*2)

kivy.require('1.9.1')
FONT_SIZE = 11



def convert_seconds_to_text(total_seconds=0):
    days = int(total_seconds // 86400)
    if days == 1:
        word_days = ' day '
    else:
        word_days = ' days '
    days = str(days) + word_days

    hours = int(total_seconds // 3600 % 24)
    if hours == 1:
        word_hours = ' hour '
    else:
        word_hours = ' hours '
    hours = str(hours) + word_hours

    minutes = int(total_seconds // 60 % 60)
    if minutes == 1:
        word_minutes = ' minute '
    else:
        word_minutes = ' minutes '
    minutes = str(minutes) + word_minutes

    seconds = total_seconds % 60
    return '{}{}{}{:.1f} s'.format(days, hours, minutes, seconds)

def load_data():
    try:
        with open('saved_data', 'rb') as fp:
            data = pickle.load(fp)
    except Exception as e:
        print("Exception when loading saved data. Oh Man, Oh Jeez!: {}".format(e))
        return {}

    return data


class LimitedInput(TextInput):

    def insert_text(self, substring, from_undo=False):
        if len(self.text) > 25:
            substring = ''
        return super(LimitedInput, self).insert_text(substring, from_undo=from_undo)


class Timer(StackLayout):
    def __init__(self, **kwargs):
        super(Timer, self).__init__(**kwargs)
        self.size_hint_y = None

        self.timer_name = LimitedInput(hint_text='Keterangan Stopwatch', size_hint=(.25, .5),
                                       font_size=FONT_SIZE, allow_copy=False)
        self.visible_time = Label(text=convert_seconds_to_text(), size_hint=(.75, .5), font_size=FONT_SIZE)

        self.start_btn = Button(text='Start', size_hint=(.8, .5), font_size=FONT_SIZE)
        self.start_btn.bind(on_release=self.clk_start_btn)

        self.reset_timer_btn = Button(text='Reset', size_hint=(.15, .5), font_size=FONT_SIZE)
        self.reset_timer_btn.bind(on_release=self.clk_reset_timer_btn)

        self.remove_timer_btn = Button(text='X', size_hint=(.05, .5), font_size=FONT_SIZE, background_color=[0.9, 0, 0, 1])
        self.remove_timer_btn.bind(on_release=self.clk_remove_timer_btn)

        self.add_widget(self.timer_name)
        self.add_widget(self.visible_time)
        self.add_widget(self.start_btn)
        self.add_widget(self.reset_timer_btn)
        self.add_widget(self.remove_timer_btn)
        self.total_seconds = 0
        self.stop_time = 0

        self.running = False

    def update(self, *args):
        self.total_seconds = time.time() - self.stop_time

        self.visible_time.text = convert_seconds_to_text(self.total_seconds)

    def clk_start_btn(self, obj):
        if self.running:
            self.running = False
            Clock.unschedule(self.update)
            self.start_btn.text = "Start"
        else:
            self.running = True
            self.stop_time = time.time() - self.total_seconds
            Clock.schedule_interval(self.update, 0.1)
            self.start_btn.text = "Stop"

    def clk_reset_timer_btn(self, obj):
        if self.running:
            self.running = False
            Clock.unschedule(self.update)
            self.start_btn.text = "Start"

        self.total_seconds = 0
        self.visible_time.text = convert_seconds_to_text(self.total_seconds)

    def clk_remove_timer_btn(self, obj):
        self.parent.remove_widget(self)
        MainScreen.timers.remove(self)


class MainScroll(ScrollView):

    def __init__(self, **kwargs):
        super(MainScroll, self).__init__(**kwargs)
        self.size_hint = (1, None)
        self.size = (Window.width, Window.height)
        self.scroll_timeout = 60
        self.add_widget(MainScreen())


class MainScreen(StackLayout):
    timers = []

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))

        self.add_timer_btn = Button(text="Add New Timer", size_hint=(.5, None), height=Window.height//12,
                                    font_size=FONT_SIZE)
        self.add_timer_btn.bind(on_release=self.clk_add_timer_btn)

        self.save_and_quit_btn = Button(text='Save and Quit', size_hint=(.5, None), height=Window.height//12,
                                        font_size=FONT_SIZE)
        self.save_and_quit_btn.bind(on_release=self.clk_save_and_quit)

        self.add_widget(self.add_timer_btn)
        self.add_widget(self.save_and_quit_btn)

        # load saved data
        for timer_data in load_data().values():
            self.create_timer(total_seconds=timer_data['total_seconds'], timer_name=timer_data['timer_name'])

        # auto save
        Clock.schedule_interval(self.save, 1)

    def clk_add_timer_btn(self, obj):
        self.create_timer()

    def create_timer(self, total_seconds=0, timer_name=''):
        timer = Timer(height=Window.height//6.5)
        timer.total_seconds = total_seconds
        timer.timer_name.text = timer_name
        timer.visible_time.text = convert_seconds_to_text(total_seconds)

        self.add_widget(timer)
        self.timers.append(timer)

    def clk_save_and_quit(self, *args):
        if self.save():
            TimeYourselfApp().stop()

    def save(self, *args):
        timers_dic = {}
        for t in self.timers:
            timers_dic[self.timers.index(t)] = {"total_seconds": t.total_seconds, "timer_name": t.timer_name.text}
        try:
            with open('saved_data', 'wb') as fp:
                pickle.dump(timers_dic, fp)
        except Exception as e:
            print("Exception when saving data. Oh Man, Oh Jeez!: {}".format(e))
        else:
            # Oh Man, Oh Jeez! People looked trough my code till the end
            return True


class TimeYourselfApp(App):
    def build(self):
        self.title = 'Stopwatch Kita'
        return MainScroll()


TimeYourselfApp().run()
