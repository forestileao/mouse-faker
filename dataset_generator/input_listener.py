from pynput import mouse
from os import path
from datetime import datetime
import json


class Generator:
    samples: list
    current_sample: dict
    is_loop_running: bool

    def __init__(self):
        self.samples = []
        self.reset_current_sample()

    def start_loop(self):
        with mouse.Listener(on_click=self.on_click, on_move=self.on_move) as listener:
            listener.join()

    def reset_current_sample(self):
        self.current_sample = {
            'target_position': (0, 0),
            'mouse_trace': []
        }

    def on_move(self, x, y):
        self.current_sample['mouse_trace'].append((x, y))

    def on_click(self, x, y, button, pressed):
        if pressed:
            if button == mouse.Button.left:
                self.save_current_sample(x, y)
            elif button == mouse.Button.right:
                self.save_all_samples()
                exit(1)

    def save_current_sample(self, x, y):
        self.current_sample['target_position'] = (x, y)
        self.samples.append(self.current_sample)
        self.reset_current_sample()

    def save_all_samples(self):
        dir_name = path.dirname(path.realpath(__file__))
        new_file_path = path.join(dir_name, '..', 'dataset', f'dataset_{datetime.now()}.json')

        with open(new_file_path, 'w', encoding='utf-8') as file:
            json.dump(self.samples, file)
