from gpio_status_reader import read_gpio_status
import threading

# Define GPIO pins to monitor
gpio_pins = [17, 18, 22]

def monitor_gpio_pins():
    threads = []
    for pin in gpio_pins:
        thread = threading.Thread(target=read_gpio_status, args=(pin,))
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    monitor_gpio_pins()
