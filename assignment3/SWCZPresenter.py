from SWCZ import SWCZ, ViewListener

class SWCZPresenter(ViewListener):
   
    def bind(self, view):
        self.view = view
        self.message_buffer = []
        self.debug_buffer = []

    def add_message(self, sendername, text):
        self.message_buffer.append((sendername, text))
        self.view.add_message("{:s}:{:s}\n".format(sendername, text))

    def update_list_views(self):
        message_text = ""
        for m in self.message_buffer:
            message_text += "{:s}:{:s}\n".format(m[0], m[1])
        self.view.messages.set(message_text)

    def on_mode_select(self):
            print("Selected " + str(self.view.mode.get()) + " mode")

    def on_connect_button_press(self):
            print("You pressed the connect button!")

    def on_continue_button_press(self):
            print("You pressed the continue button!")

    def on_send_button_press(self):
            print("You pressed the send button!")
            self.view.add_debug_message("pressed send!\n")
            self.add_message("Me", self.view.send_message.get())
