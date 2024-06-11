from pynput import mouse

def start_mouse_listener(state, best_stats, capture_and_process_func):
    def on_click(x, y, button, pressed):
        if button == mouse.Button.middle and pressed and state['capturing']:
            capture_and_process_func(best_stats)

    listener = mouse.Listener(on_click=on_click)
    return listener
