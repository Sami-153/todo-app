import threading

BUFFER_SIZE = 100
bufferA = []
bufferB = []
active_buffer = bufferA
inactive_buffer = bufferB
lock = threading.Lock()
switch_flag = False  
stop_program = False

def fill_buffer(buffer):
    global switch_flag, stop_program 
    print("Enter program (q to quit):")
    while not stop_program:
        lock.acquire()
        

        if not switch_flag:
            user_input = input()

            if user_input == "q":
                stop_program = True
                lock.release()
                break

            buffer.append(user_input)

            if len(buffer) >= BUFFER_SIZE:
                switch_flag = True

        lock.release()

        
        
def process_data(buffer):
    global switch_flag, stop_program

    while not stop_program:
        lock.acquire()
        if switch_flag == True:
            data_string = ''.join(buffer)

            words = data_string.split()

            print("Processed words:", words)

            buffer.clear()
            switch_flag = False

        lock.release()

                
        
def main():
    global switch_flag, stop_program ,  active_buffer, inactive_buffer
    
    
    producer_thread = threading.Thread(target=fill_buffer, args=(active_buffer,))
    consumer_thread = threading.Thread(target=process_data, args=(active_buffer,))
    
    producer_thread.start()
    consumer_thread.start()
    
    while not stop_program:
        
        if switch_flag == True:
            
            if active_buffer == bufferA:
                active_buffer = bufferB
                inactive_buffer = bufferA
            else:
                active_buffer = bufferA
                inactive_buffer = bufferB
                
    producer_thread.join()
    consumer_thread.join()

    print("Program Exited")
                 
main()

